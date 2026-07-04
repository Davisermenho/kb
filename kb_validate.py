#!/usr/bin/env python3
"""Orquestra gates independentes do Fluxo V2.

Uso: python3 kb_validate.py [diretorio] [--json] [--publish] [--run-id ID]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

import check_kb_consistency as checker


SCORE_FIELDS = {
    "IDENTIFICAÇÃO_COMPLETA (0 a 2)": 2,
    "RELEVÂNCIA_TAREFA (0 a 3)": 3,
    "FORÇA_FONTE (0 a 3)": 3,
    "ATUALIDADE (0 a 2)": 2,
    "RASTREABILIDADE (0 a 3)": 3,
    "EXTRAÇÃO_ÚTIL (0 a 3)": 3,
    "LIMITAÇÕES_REGISTRADAS (0 a 2)": 2,
    "APLICAÇÃO_PARA_IA (0 a 3)": 3,
}
CONFIDENCE_RANK = {"Fonte rejeitada": 0, "Fonte fraca": 1, "Fonte média": 2, "Fonte forte": 3}
CAUSAL_WORDS = re.compile(r"\b(motivou|originou|causou|inspirou|modelo direto)\b", re.IGNORECASE)


@dataclass(frozen=True)
class Finding:
    code: str
    message: str
    path: str = ""
    line: int = 1
    severity: str = "error"


@dataclass
class Gate:
    name: str
    status: str = "PASS"
    findings: list[Finding] = field(default_factory=list)
    not_validated: list[str] = field(default_factory=list)

    def add(self, finding: Finding) -> None:
        self.findings.append(finding)
        if finding.severity == "error":
            self.status = "FAIL"
        elif self.status == "PASS":
            self.status = "WARN"


@dataclass
class ValidationReport:
    directory: str
    mode: str
    run_id: str | None
    gates: list[Gate]

    @property
    def blocked(self) -> bool:
        if any(gate.status == "FAIL" for gate in self.gates):
            return True
        if self.mode == "publish" and any(gate.status in {"WARN", "SKIPPED"} for gate in self.gates):
            return True
        return False

    def to_dict(self) -> dict:
        return {
            "directory": self.directory,
            "mode": self.mode,
            "run_id": self.run_id,
            "result": "BLOQUEADO" if self.blocked else "APROVADO",
            "gates": [asdict(gate) for gate in self.gates],
            "not_validated_by_automation": [
                "verdade factual externa integral",
                "fidelidade semântica integral",
                "julgamento humano de conflitos",
            ],
        }


def git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=root, text=True, capture_output=True)


def parse_ledger(root: Path, issues: list[checker.Issue] | None = None) -> list[checker.Entry]:
    path = root / "FONTES_REGISTRADAS.md"
    local_issues = issues if issues is not None else []
    return checker.parse_entries(checker.read_utf8(path), path, root, local_issues, ledger=True)


def gate_preflight(root: Path, publish: bool, run_id: str | None) -> Gate:
    gate = Gate("PREFLIGHT")
    for name in ("PROTOCOLO.md", "REGISTRO_FONTES.md", "TEMPLATE.md", "FONTES_REGISTRADAS.md"):
        if not (root / name).is_file():
            gate.add(Finding("PREFLIGHT-MISSING-FILE", f"arquivo obrigatório ausente: {name}", name))
    git_check = git(root, "rev-parse", "--is-inside-work-tree")
    if git_check.returncode != 0:
        severity = "error" if publish else "warning"
        gate.add(Finding("PREFLIGHT-NO-GIT", "baseline Git ainda não foi inicializado e aprovado", severity=severity))
    if publish and not run_id:
        gate.add(Finding("PREFLIGHT-MISSING-RUN", "modo de publicação exige --run-id"))
    if run_id and not (root / ".kb" / "runs" / run_id / "manifest.json").is_file():
        gate.add(Finding("PREFLIGHT-MISSING-MANIFEST", f"manifesto do RUN_ID '{run_id}' não encontrado"))
    return gate


def structural_gates(root: Path) -> list[Gate]:
    report = checker.validate(root)
    mapping = {
        "structure": "SCHEMA",
        "consistency": "LEDGER_KB",
    }
    gates = {name: Gate(name) for name in ("SCHEMA", "DUPLICIDADE", "ROTEAMENTO", "LEDGER_KB")}
    for issue in report.issues:
        if "DUPLICATE" in issue.code:
            target = "DUPLICIDADE"
        elif issue.code.startswith("ROUTING"):
            target = "ROTEAMENTO"
        else:
            target = mapping.get(issue.category, "LEDGER_KB")
        gates[target].add(Finding(issue.code, issue.message, issue.path, issue.line))
    return list(gates.values())


def expected_confidence(score: int) -> int:
    if score >= 17:
        return 3
    if score >= 11:
        return 2
    if score >= 6:
        return 1
    return 0


def gate_score_status(root: Path) -> Gate:
    gate = Gate("SCORE_STATUS")
    for entry in parse_ledger(root):
        values: list[int] = []
        for field_name, maximum in SCORE_FIELDS.items():
            raw = entry.fields.get(field_name)
            if raw is None:
                gate.add(Finding("SCORE-MISSING", f"'{entry.heading_id}': campo '{field_name}' ausente", entry.path.name, entry.line))
                continue
            match = re.fullmatch(r"\s*(\d+)\s*", raw)
            if not match:
                gate.add(Finding("SCORE-NOT-INTEGER", f"'{entry.heading_id}': '{field_name}' não é inteiro", entry.path.name, entry.field_lines.get(field_name, entry.line)))
                continue
            value = int(match.group(1))
            if value < 0 or value > maximum:
                gate.add(Finding("SCORE-OUT-OF-RANGE", f"'{entry.heading_id}': '{field_name}'={value}, máximo={maximum}", entry.path.name, entry.field_lines.get(field_name, entry.line)))
            values.append(value)
        raw_total = entry.fields.get("PONTUAÇÃO_TOTAL (0 a 21)")
        if raw_total and raw_total.isdigit() and len(values) == len(SCORE_FIELDS):
            total = int(raw_total)
            if total != sum(values):
                gate.add(Finding("SCORE-TOTAL-MISMATCH", f"'{entry.heading_id}': total {total}, soma calculada {sum(values)}", entry.path.name, entry.field_lines.get("PONTUAÇÃO_TOTAL (0 a 21)", entry.line)))
            confidence = entry.fields.get("NÍVEL_CONFIANÇA") or ""
            canonical_confidence = next((item for item in CONFIDENCE_RANK if confidence.startswith(item)), "")
            rank = CONFIDENCE_RANK.get(canonical_confidence)
            if rank is None:
                gate.add(Finding("STATUS-INVALID-CONFIDENCE", f"'{entry.heading_id}': NÍVEL_CONFIANÇA inválido ou ausente", entry.path.name, entry.field_lines.get("NÍVEL_CONFIANÇA", entry.line)))
            elif rank > expected_confidence(total):
                gate.add(Finding("STATUS-OVERSTATED-CONFIDENCE", f"'{entry.heading_id}': confiança é superior à faixa da pontuação", entry.path.name, entry.field_lines.get("NÍVEL_CONFIANÇA", entry.line)))
        else:
            gate.add(Finding("SCORE-MISSING-TOTAL", f"'{entry.heading_id}': PONTUAÇÃO_TOTAL ausente ou inválida", entry.path.name, entry.line))
    return gate


def gate_references(root: Path) -> Gate:
    gate = Gate("REFERENCIAS_INTERNAS")
    files = [root / name for name in ("PROTOCOLO.md", "REGISTRO_FONTES.md", "TEMPLATE.md", "FONTES_REGISTRADAS.md")]
    pattern = re.compile(r"`([^`\n]+\.md)`")
    for path in files:
        if not path.exists():
            continue
        for line_number, line in enumerate(checker.read_utf8(path).splitlines(), 1):
            for match in pattern.finditer(line):
                value = match.group(1)
                # Paths com subdiretórios dentro de conteúdo extraído normalmente
                # pertencem à fonte externa. Referências internas canônicas são
                # arquivos Markdown no diretório raiz desta base.
                if "/" not in value and (value.startswith("KB-") or value.isupper() or value in {p.name for p in root.glob("*.md")}):
                    target = root / value
                    if not target.exists():
                        gate.add(Finding("REFERENCE-MISSING-FILE", f"referência interna não resolve: {value}", path.name, line_number))
    return gate


def gate_pending(root: Path) -> Gate:
    gate = Gate("PENDENCIAS")
    architecture = checker.read_utf8(root / "REGISTRO_FONTES.md")
    for entry in parse_ledger(root):
        routing = entry.fields.get("STATUS_DE_ROTEAMENTO")
        status = entry.fields.get("STATUS")
        needs_pending = routing in {"Revisar", "Bloqueado"} or status == "Revisar"
        if needs_pending and entry.heading_id not in architecture:
            gate.add(Finding("PENDING-MISSING", f"'{entry.heading_id}' exige pendência, mas não aparece em REGISTRO_FONTES.md", entry.path.name, entry.line))
    return gate


def load_manifest(root: Path, run_id: str) -> dict:
    path = root / ".kb" / "runs" / run_id / "manifest.json"
    return json.loads(path.read_text(encoding="utf-8"))


def gate_scope(root: Path, run_id: str | None) -> Gate:
    gate = Gate("ESCOPO_DIFF")
    if not run_id:
        gate.status = "SKIPPED"
        gate.not_validated.append("nenhum RUN_ID informado; gate aplicável à publicação")
        return gate
    try:
        manifest = load_manifest(root, run_id)
    except (OSError, ValueError) as exc:
        gate.add(Finding("SCOPE-INVALID-MANIFEST", str(exc)))
        return gate
    base = manifest.get("estado_inicial_commit")
    if not base:
        gate.add(Finding("SCOPE-MISSING-BASE", "manifesto não possui estado_inicial_commit"))
        return gate
    result = git(root, "diff", "--name-status", base, "--")
    if result.returncode != 0:
        gate.add(Finding("SCOPE-GIT-ERROR", result.stderr.strip() or "git diff falhou"))
        return gate
    allowed = set(manifest.get("arquivos_permitidos", []))
    operations = set(manifest.get("operacoes_permitidas", []))
    preexisting = manifest.get("snapshot_preexistente", {})
    operation_by_status = {"A": "criar", "M": "editar", "D": "excluir", "R": "renomear"}
    for line in result.stdout.splitlines():
        parts = line.split("\t")
        status = parts[0][0]
        paths = parts[1:]
        operation = operation_by_status.get(status, "editar")
        for path in paths:
            initial_hash = preexisting.get(path, "__not_preexisting__")
            if initial_hash != "__not_preexisting__":
                current_path = root / path
                current_hash = hashlib.sha256(current_path.read_bytes()).hexdigest() if current_path.is_file() else None
                if current_hash == initial_hash:
                    continue
            if path not in allowed:
                gate.add(Finding("SCOPE-UNAUTHORIZED-FILE", f"arquivo fora do manifesto: {path}", path))
            if operation not in operations:
                gate.add(Finding("SCOPE-UNAUTHORIZED-OPERATION", f"operação '{operation}' não autorizada para {path}", path))
    return gate


def gate_causality(root: Path, run_id: str | None) -> Gate:
    gate = Gate("CAUSALIDADE")
    target = root / "KB-PROJ-05_Arquitetura_da_Base_de_Conhecimento.md"
    if not target.exists():
        return gate
    if not run_id:
        for number, line in enumerate(checker.read_utf8(target).splitlines(), 1):
            if CAUSAL_WORDS.search(line) and "Correção" not in line:
                gate.add(Finding("CAUSALITY-LEGACY-REVIEW", "alegação causal legada inventariada; migração pendente", target.name, number, severity="warning"))
        return gate
    try:
        manifest = load_manifest(root, run_id)
    except (OSError, ValueError) as exc:
        gate.add(Finding("CAUSALITY-MANIFEST-ERROR", str(exc)))
        return gate
    base = manifest.get("estado_inicial_commit")
    if not base:
        gate.add(Finding("CAUSALITY-MISSING-BASE", "não é possível validar causalidade sem commit inicial"))
        return gate
    diff = git(root, "diff", "--unified=0", base, "--", target.name)
    if diff.returncode != 0:
        gate.add(Finding("CAUSALITY-GIT-ERROR", diff.stderr.strip() or "git diff falhou"))
        return gate
    added_causal = [line[1:] for line in diff.stdout.splitlines() if line.startswith("+") and not line.startswith("+++") and CAUSAL_WORDS.search(line[1:])]
    records = manifest.get("causalidade", [])
    for line in added_causal:
        valid = any(
            record.get("change_id")
            and record.get("decisao_referencia")
            and record.get("diff_referencia")
            and record.get("tipo") == "mudanca_comprovadamente_motivada"
            for record in records
        )
        if not valid:
            gate.add(Finding("CAUSALITY-UNVERIFIED", "linha causal nova exige registro completo no manifesto", target.name))
    return gate


def gate_review(root: Path, run_id: str | None) -> Gate:
    gate = Gate("REVISAO")
    if not run_id:
        gate.status = "SKIPPED"
        gate.not_validated.append("nenhum RUN_ID informado")
        return gate
    run_dir = root / ".kb" / "runs" / run_id
    try:
        manifest = load_manifest(root, run_id)
    except (OSError, ValueError) as exc:
        gate.add(Finding("REVIEW-MANIFEST-ERROR", str(exc)))
        return gate
    risk = manifest.get("risco", "medio")
    review_path = run_dir / "review.json"
    if risk == "baixo":
        return gate
    if not review_path.exists():
        gate.add(Finding("REVIEW-MISSING", f"risco '{risk}' exige review.json", str(review_path.relative_to(root))))
        return gate
    try:
        review = json.loads(review_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        gate.add(Finding("REVIEW-INVALID", str(exc), str(review_path.relative_to(root))))
        return gate
    if review.get("decisao") not in {"APROVADO", "APROVADO_COM_RESSALVAS"}:
        gate.add(Finding("REVIEW-NOT-APPROVED", "revisão não aprovou o diff", str(review_path.relative_to(root))))
    if risk in {"alto", "critico"} and review.get("tipo_revisor") != "humano":
        gate.add(Finding("REVIEW-HUMAN-REQUIRED", f"risco '{risk}' exige revisor humano", str(review_path.relative_to(root))))
    base = manifest.get("estado_inicial_commit")
    if base:
        diff = git(root, "diff", "--binary", base, "--")
        if diff.returncode == 0:
            digest = hashlib.sha256(diff.stdout.encode("utf-8")).hexdigest()
            if review.get("diff_sha256") != digest:
                gate.add(Finding("REVIEW-DIFF-MISMATCH", "revisão não está vinculada ao diff atual", str(review_path.relative_to(root))))
    return gate


def validate(root: Path, publish: bool = False, run_id: str | None = None) -> ValidationReport:
    root = root.resolve()
    gates = [gate_preflight(root, publish, run_id)]
    try:
        gates.extend(structural_gates(root))
        gates.extend([
            gate_score_status(root),
            gate_references(root),
            gate_pending(root),
            gate_scope(root, run_id),
            gate_causality(root, run_id),
            gate_review(root, run_id),
        ])
    except checker.OperationalError as exc:
        gates[0].add(Finding("PREFLIGHT-OPERATIONAL-ERROR", str(exc)))
    return ValidationReport(str(root), "publish" if publish else "audit", run_id, gates)


def render(report: ValidationReport) -> str:
    lines = [
        f"RUN_ID: {report.run_id or 'não informado'}",
        f"Modo: {report.mode}",
        f"Resultado: {'BLOQUEADO' if report.blocked else 'APROVADO'}",
        "",
    ]
    for gate in report.gates:
        lines.append(f"[{gate.status}] {gate.name}")
        lines.extend(f"  - {item.code}: {item.path + ':' + str(item.line) + ': ' if item.path else ''}{item.message}" for item in gate.findings)
        lines.extend(f"  - NÃO VALIDADO: {item}" for item in gate.not_validated)
    lines.extend([
        "",
        "NÃO VALIDADO POR AUTOMAÇÃO: verdade factual externa integral, fidelidade semântica integral e julgamento humano de conflitos.",
    ])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", type=Path, default=Path(__file__).parent)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--run-id")
    args = parser.parse_args(argv)
    report = validate(args.directory, args.publish, args.run_id)
    print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2) if args.json else render(report))
    return 1 if report.blocked else 0


if __name__ == "__main__":
    raise SystemExit(main())
