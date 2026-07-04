#!/usr/bin/env python3
"""Gerencia RUN_ID, manifestos, rascunhos e locks do Fluxo V2."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import socket
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import kb_validate
import check_kb_consistency as checker
import kb_paths as paths


VALID_RISK = {"baixo", "medio", "alto", "critico"}
VALID_OPERATIONS = {"criar", "editar", "excluir", "renomear", "sincronizar"}
TRANSITIONS = {
    "RASCUNHO": {"EXTRAÍDO", "BLOQUEADO", "DUPLICATA_CANDIDATA", "REJEITADO"},
    "EXTRAÍDO": {"AVALIADO", "BLOQUEADO", "CONFLITO", "REJEITADO"},
    "AVALIADO": {"ROTEAMENTO_PROPOSTO", "CONFLITO", "SEM_DESTINO", "REJEITADO"},
    "ROTEAMENTO_PROPOSTO": {"APROVADO", "REVISÃO_HUMANA", "SEM_DESTINO", "BLOQUEADO"},
    "REVISÃO_HUMANA": {"APROVADO", "BLOQUEADO", "REJEITADO"},
    "CONFLITO": {"REVISÃO_HUMANA", "BLOQUEADO", "REJEITADO"},
    "DUPLICATA_CANDIDATA": {"RASCUNHO", "REJEITADO", "BLOQUEADO"},
    "SEM_DESTINO": {"REVISÃO_HUMANA", "REJEITADO", "BLOQUEADO"},
    "APROVADO": {"PREPARADO", "BLOQUEADO"},
    "PREPARADO": {"VALIDADO_ESTRUTURALMENTE", "FALHA_DE_VALIDACAO", "FALHA_DE_PUBLICACAO"},
    "VALIDADO_ESTRUTURALMENTE": {"VALIDADO_SEMANTICAMENTE", "FALHA_DE_VALIDACAO"},
    "VALIDADO_SEMANTICAMENTE": {"PUBLICADO", "FALHA_DE_PUBLICACAO"},
    "FALHA_DE_VALIDACAO": {"PREPARADO", "BLOQUEADO"},
    "FALHA_DE_PUBLICACAO": {"PREPARADO", "BLOQUEADO"},
    "BLOQUEADO": {"RASCUNHO", "REJEITADO"},
    "REJEITADO": set(),
    "PUBLICADO": set(),
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def git_head(root: Path) -> str | None:
    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, text=True, capture_output=True)
    return result.stdout.strip() if result.returncode == 0 else None


def git_changes(root: Path) -> list[str]:
    result = subprocess.run(["git", "status", "--porcelain"], cwd=root, text=True, capture_output=True)
    return result.stdout.splitlines() if result.returncode == 0 else []


def file_sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def preexisting_snapshot(root: Path) -> dict[str, str | None]:
    snapshot: dict[str, str | None] = {}
    for status_line in git_changes(root):
        raw_path = status_line[3:]
        paths = raw_path.split(" -> ")
        for value in paths:
            snapshot[value] = file_sha256(root / value)
    return snapshot


def create_run(root: Path, run_id: str, objective: str, risk: str, files: list[str], operations: list[str]) -> Path:
    if risk not in VALID_RISK:
        raise ValueError(f"risco inválido: {risk}")
    invalid_operations = set(operations) - VALID_OPERATIONS
    if invalid_operations:
        raise ValueError(f"operações inválidas: {sorted(invalid_operations)}")
    run_dir = root / ".kb" / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    run_prefix = f".kb/runs/{run_id}"
    generated_files = {
        f"{run_prefix}/manifest.json",
        f"{run_prefix}/draft.md",
        f"{run_prefix}/state.json",
        f"{run_prefix}/validation.json",
        f"{run_prefix}/review.json",
    }
    manifest = {
        "schema_version": 1,
        "run_id": run_id,
        "objetivo": objective,
        "solicitante": os.environ.get("USER", "desconhecido"),
        "criado_em": now(),
        "risco": risk,
        "fontes_planejadas": [],
        "arquivos_permitidos": sorted(set(files) | generated_files),
        "operacoes_permitidas": sorted(set(operations)),
        "operacoes_proibidas": sorted(VALID_OPERATIONS - set(operations)),
        "estado_inicial_commit": git_head(root),
        "alteracoes_preexistentes": git_changes(root),
        "snapshot_preexistente": preexisting_snapshot(root),
        "causalidade": [],
        "aprovacoes_exigidas": ["humano"] if risk in {"alto", "critico"} else (["independente"] if risk == "medio" else []),
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (run_dir / "draft.md").write_text(f"# Rascunho — {run_id}\n\n**Objetivo:** {objective}\n\n**Estado:** RASCUNHO\n", encoding="utf-8")
    (run_dir / "state.json").write_text(
        json.dumps({"run_id": run_id, "state": "RASCUNHO", "updated_at": now(), "history": [{"state": "RASCUNHO", "at": now()}]}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return run_dir


def transition(root: Path, run_id: str, target: str, reason: str) -> dict:
    run_dir = root / ".kb" / "runs" / run_id
    state_path = run_dir / "state.json"
    if not state_path.exists():
        raise RuntimeError(f"estado do RUN_ID não encontrado: {run_id}")
    state = json.loads(state_path.read_text(encoding="utf-8"))
    current = state.get("state")
    if target not in TRANSITIONS.get(current, set()):
        raise RuntimeError(f"transição inválida: {current} → {target}")
    if target == "PUBLICADO":
        validation_path = run_dir / "validation.json"
        if not validation_path.exists():
            raise RuntimeError("PUBLICADO exige validation.json")
        validation = json.loads(validation_path.read_text(encoding="utf-8"))
        if validation.get("result") != "APROVADO" or validation.get("mode") != "publish":
            raise RuntimeError("PUBLICADO exige validação aprovada em modo publish")
    event = {"from": current, "state": target, "at": now(), "reason": reason}
    state["state"] = target
    state["updated_at"] = event["at"]
    state.setdefault("history", []).append(event)
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    draft_path = run_dir / "draft.md"
    if draft_path.exists():
        draft = draft_path.read_text(encoding="utf-8")
        draft = re.sub(r"\*\*Estado:\*\*\s*\S+", f"**Estado:** {target}", draft, count=1)
        draft_path.write_text(draft, encoding="utf-8")
    return state


def lock_path(root: Path) -> Path:
    return root / ".kb" / "locks" / "publish.lock"


def acquire_lock(root: Path, run_id: str) -> None:
    path = lock_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps({"run_id": run_id, "pid": os.getpid(), "host": socket.gethostname(), "created_at": now()}, ensure_ascii=False)
    try:
        descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    except FileExistsError as exc:
        owner = path.read_text(encoding="utf-8") if path.exists() else "desconhecido"
        raise RuntimeError(f"lock de publicação já existe: {owner}") from exc
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        handle.write(payload + "\n")


def release_lock(root: Path, run_id: str) -> None:
    path = lock_path(root)
    if not path.exists():
        raise RuntimeError("lock de publicação não existe")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("run_id") != run_id:
        raise RuntimeError(f"lock pertence a {payload.get('run_id')}; não será removido")
    path.unlink()


def command_init(args: argparse.Namespace) -> int:
    root = args.directory.resolve()
    run_dir = create_run(root, args.run_id, args.objective, args.risk, args.file, args.operation)
    print(f"RUN criado: {run_dir}")
    return 0


def command_validate(args: argparse.Namespace) -> int:
    report = kb_validate.validate(args.directory, args.publish, args.run_id)
    run_dir = args.directory.resolve() / ".kb" / "runs" / args.run_id
    if run_dir.exists():
        (run_dir / "validation.json").write_text(json.dumps(report.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(kb_validate.render(report))
    return 1 if report.blocked else 0


def command_lock(args: argparse.Namespace) -> int:
    acquire_lock(args.directory.resolve(), args.run_id)
    print(f"Lock adquirido por {args.run_id}")
    return 0


def command_unlock(args: argparse.Namespace) -> int:
    release_lock(args.directory.resolve(), args.run_id)
    print(f"Lock liberado por {args.run_id}")
    return 0


def command_transition(args: argparse.Namespace) -> int:
    state = transition(args.directory.resolve(), args.run_id, args.to, args.reason)
    print(f"{args.run_id}: estado atual = {state['state']}")
    return 0


def duplicate_candidates(root: Path, title: str | None, url: str | None, author: str | None) -> list[dict]:
    ledger_path = root / paths.LEDGER_PATH
    issues: list[checker.Issue] = []
    entries = checker.parse_entries(checker.read_utf8(ledger_path), ledger_path, root, issues, ledger=True)
    if issues:
        raise RuntimeError("ledger malformado; deduplicação prévia não é confiável")
    title_key = checker.normalize_title(title) if title else None
    url_key = checker.normalize_url(url) if url else None
    author_key = checker.normalize_title(author) if author else None
    candidates: list[dict] = []
    for entry in entries:
        reasons: list[str] = []
        if title_key and checker.normalize_title(entry.fields.get("TÍTULO", "")) == title_key:
            reasons.append("titulo")
        if url_key and checker.normalize_url(entry.fields.get("LINK_REFERÊNCIA", "")) == url_key:
            reasons.append("url")
        if author_key and checker.normalize_title(entry.fields.get("AUTOR_ORGANIZAÇÃO", "")) == author_key:
            reasons.append("autor")
        if reasons:
            candidates.append({"id_fonte": entry.heading_id, "motivos": reasons, "line": entry.line})
    return candidates


def command_candidates(args: argparse.Namespace) -> int:
    candidates = duplicate_candidates(args.directory.resolve(), args.title, args.url, args.author)
    print(json.dumps({"result": "DUPLICATA_CANDIDATA" if candidates else "SEM_CANDIDATO", "candidates": candidates}, ensure_ascii=False, indent=2))
    return 1 if candidates else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=Path(__file__).resolve().parents[1])
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init-run")
    init.add_argument("--run-id", required=True)
    init.add_argument("--objective", required=True)
    init.add_argument("--risk", choices=sorted(VALID_RISK), default="medio")
    init.add_argument("--file", action="append", default=[])
    init.add_argument("--operation", action="append", choices=sorted(VALID_OPERATIONS), default=["criar", "editar"])
    init.set_defaults(func=command_init)

    validate = subparsers.add_parser("validate")
    validate.add_argument("--run-id", required=True)
    validate.add_argument("--publish", action="store_true")
    validate.set_defaults(func=command_validate)

    lock = subparsers.add_parser("lock")
    lock.add_argument("--run-id", required=True)
    lock.set_defaults(func=command_lock)

    unlock = subparsers.add_parser("unlock")
    unlock.add_argument("--run-id", required=True)
    unlock.set_defaults(func=command_unlock)

    transition_parser = subparsers.add_parser("transition")
    transition_parser.add_argument("--run-id", required=True)
    transition_parser.add_argument("--to", required=True, choices=sorted(TRANSITIONS))
    transition_parser.add_argument("--reason", required=True)
    transition_parser.set_defaults(func=command_transition)

    candidates = subparsers.add_parser("check-source")
    candidates.add_argument("--title")
    candidates.add_argument("--url")
    candidates.add_argument("--author")
    candidates.set_defaults(func=command_candidates)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
