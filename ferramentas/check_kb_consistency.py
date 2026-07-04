#!/usr/bin/env python3
"""Valida estrutura e consistência entre o ledger e as KBs.

Uso: python3 ferramentas/check_kb_consistency.py [diretorio] [--json]

Códigos: 0 = aprovado estruturalmente; 1 = divergências; 2 = falha operacional.
Este programa não valida factualidade, fidelidade semântica, causalidade ou atualidade.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import asdict, dataclass, field
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import kb_paths as paths


VALID_ID_RE = re.compile(r"^FONTE-(19|20)\d{2}-[A-Z0-9]+-[A-Z0-9-]+$")
KB_CODE_RE = re.compile(r"\bKB(?:-PROJ)?-\d+\b")
KB_FILENAME_RE = re.compile(r"^(KB(?:-PROJ)?-\d+)_.*\.md$")
SECTION_RE = re.compile(r"(?m)^## Registros\s*$")
HEADING_RE = re.compile(r"(?m)^###[ \t]+(.+?)\s*$")
FIELD_RE = re.compile(
    r"^(?:-\s*)?(?:"
    r"\*\*(?P<bold_before>[^*:\n]+)\*\*:\s*|"
    r"\*\*(?P<bold_inside>[^*:\n]+):\*\*\s*|"
    r"(?P<plain>[^*:\n][^:\n]*):\s*"
    r")(?P<value>.*)$"
)
REQUIRED_FIELDS = (
    "ID_FONTE",
    "TÍTULO",
    "LINK_REFERÊNCIA",
    "ARQUIVO_DESTINO_KB",
    "STATUS_DE_ROTEAMENTO",
)
VALID_ROUTING_STATUS = {"Pendente", "Roteado", "Revisar", "Bloqueado"}
NO_DESTINATION_VALUES = {
    "nenhum",
    "nenhum destino",
    "nenhum destino compatível",
    "nenhum destino compatível na matriz atual",
}


@dataclass(frozen=True)
class Issue:
    code: str
    category: str
    message: str
    path: str
    line: int = 1

    def display(self) -> str:
        return f"[{self.code}] {self.path}:{self.line}: {self.message}"


@dataclass
class Entry:
    heading_id: str
    path: Path
    line: int
    fields: dict[str, str] = field(default_factory=dict)
    field_lines: dict[str, int] = field(default_factory=dict)
    destinations: tuple[str, ...] = ()


@dataclass
class KbFile:
    code: str
    path: Path
    entries: list[Entry]


@dataclass
class Report:
    directory: str
    ledger_entries: int = 0
    kb_files_found: int = 0
    kb_files_parsed: int = 0
    kb_codes_unique: int = 0
    issues: list[Issue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.issues

    def to_dict(self) -> dict:
        data = asdict(self)
        data["result"] = "OK_ESTRUTURAL" if self.ok else "DIVERGENTE"
        data["not_validated"] = [
            "factualidade",
            "fidelidade semântica",
            "causalidade",
            "escopo",
            "atualidade",
        ]
        return data


class OperationalError(RuntimeError):
    pass


def relative(path: Path, directory: Path) -> str:
    try:
        return str(path.relative_to(directory))
    except ValueError:
        return str(path)


def normalize_title(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text).casefold()
    without_marks = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", " ", without_marks).strip()


def first_url(text: str) -> str | None:
    match = re.search(r"https?://[^\s<>()]+", text)
    if not match:
        return None
    return match.group(0).rstrip(".,;:!?")


def normalize_url(text: str) -> str | None:
    raw = first_url(text)
    if not raw:
        return None
    try:
        parts = urlsplit(raw)
        if not parts.hostname:
            return None
        host = parts.hostname.casefold()
        if parts.port:
            host = f"{host}:{parts.port}"
        if parts.username:
            auth = parts.username
            if parts.password:
                auth += f":{parts.password}"
            host = f"{auth}@{host}"
        path = parts.path or "/"
        if path != "/":
            path = path.rstrip("/")
        return urlunsplit((parts.scheme.casefold(), host, path, parts.query, parts.fragment))
    except (ValueError, UnicodeError):
        return None


def read_utf8(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise OperationalError(f"não foi possível ler {path}: {exc}") from exc


def registros_bounds(text: str, path: Path, directory: Path, issues: list[Issue]) -> tuple[int, int] | None:
    matches = list(SECTION_RE.finditer(text))
    display_path = relative(path, directory)
    if not matches:
        issues.append(Issue("STRUCT-MISSING-SECTION", "structure", "seção '## Registros' ausente", display_path, 1))
        return None
    if len(matches) > 1:
        for duplicate in matches[1:]:
            issues.append(Issue("STRUCT-DUPLICATE-SECTION", "structure", "seção '## Registros' repetida", display_path, text.count("\n", 0, duplicate.start()) + 1))
        return None
    return matches[0].end(), text.count("\n", 0, matches[0].end()) + 1


def parse_fields(block: str, start_line: int, path: Path, directory: Path, issues: list[Issue]) -> tuple[dict[str, str], dict[str, int]]:
    values: dict[str, str] = {}
    lines: dict[str, int] = {}
    for offset, raw_line in enumerate(block.splitlines()[1:], start=1):
        match = FIELD_RE.match(raw_line.strip())
        if not match:
            continue
        name = (
            match.group("bold_before")
            or match.group("bold_inside")
            or match.group("plain")
            or ""
        ).strip()
        value = match.group("value").strip()
        line = start_line + offset
        if name in values:
            issues.append(Issue("STRUCT-DUPLICATE-FIELD", "structure", f"campo '{name}' repetido", relative(path, directory), line))
            continue
        values[name] = value
        lines[name] = line
    return values, lines


def parse_entries(text: str, path: Path, directory: Path, issues: list[Issue], ledger: bool) -> list[Entry]:
    bounds = registros_bounds(text, path, directory, issues)
    if bounds is None:
        return []
    section_start, _ = bounds
    section = text[section_start:]
    headings = list(HEADING_RE.finditer(section))
    if ledger and not headings:
        issues.append(Issue("STRUCT-EMPTY-LEDGER", "structure", "ledger não possui registros", relative(path, directory), text.count("\n", 0, section_start) + 1))
        return []
    prefix = section[: headings[0].start()] if headings else ""
    if headings and prefix.strip():
        issues.append(Issue("STRUCT-ORPHAN-CONTENT", "structure", "conteúdo encontrado antes do primeiro registro", relative(path, directory), text.count("\n", 0, section_start) + 1))
    entries: list[Entry] = []
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(section)
        block = section[heading.start():end]
        heading_text = heading.group(1).strip()
        line = text.count("\n", 0, section_start + heading.start()) + 1
        heading_id = heading_text.split()[0] if heading_text else ""
        if not heading_id:
            issues.append(Issue("STRUCT-EMPTY-HEADING", "structure", "cabeçalho de registro sem ID", relative(path, directory), line))
            continue
        fields: dict[str, str] = {}
        field_lines: dict[str, int] = {}
        destinations: tuple[str, ...] = ()
        if ledger:
            fields, field_lines = parse_fields(block, line, path, directory, issues)
            for required in REQUIRED_FIELDS:
                if not fields.get(required, "").strip():
                    issues.append(Issue("STRUCT-MISSING-FIELD", "structure", f"'{heading_id}': campo obrigatório '{required}' ausente ou vazio", relative(path, directory), line))
            destination_value = fields.get("ARQUIVO_DESTINO_KB", "")
            found = KB_CODE_RE.findall(destination_value)
            destinations = tuple(dict.fromkeys(found))
            if len(found) != len(destinations):
                issues.append(Issue("STRUCT-DUPLICATE-DESTINATION", "structure", f"'{heading_id}': destino repetido", relative(path, directory), field_lines.get("ARQUIVO_DESTINO_KB", line)))
        entries.append(Entry(heading_id, path, line, fields, field_lines, destinations))
    return entries


def validate_ledger(entries: list[Entry], directory: Path, issues: list[Issue]) -> None:
    by_id: dict[str, list[Entry]] = {}
    titles: dict[str, str] = {}
    urls: dict[str, str] = {}
    for entry in entries:
        by_id.setdefault(entry.heading_id, []).append(entry)
        if not VALID_ID_RE.fullmatch(entry.heading_id):
            issues.append(Issue("ID-INVALID-FORMAT", "consistency", f"'{entry.heading_id}' não segue FONTE-<ANO>-<VEÍCULO>-<TEMA>", relative(entry.path, directory), entry.line))
        id_field = entry.fields.get("ID_FONTE")
        if id_field and id_field != entry.heading_id:
            issues.append(Issue("LEDGER-ID-MISMATCH", "consistency", f"cabeçalho '{entry.heading_id}' diverge do campo ID_FONTE '{id_field}'", relative(entry.path, directory), entry.field_lines.get("ID_FONTE", entry.line)))
        status = entry.fields.get("STATUS_DE_ROTEAMENTO")
        if status and status not in VALID_ROUTING_STATUS:
            issues.append(Issue("STRUCT-INVALID-STATUS", "structure", f"'{entry.heading_id}': STATUS_DE_ROTEAMENTO inválido: '{status}'", relative(entry.path, directory), entry.field_lines.get("STATUS_DE_ROTEAMENTO", entry.line)))
        destination_raw = entry.fields.get("ARQUIVO_DESTINO_KB", "").strip()
        no_destination = normalize_title(destination_raw) in {normalize_title(v) for v in NO_DESTINATION_VALUES}
        if status == "Roteado" and not entry.destinations:
            issues.append(Issue("ROUTING-EMPTY", "consistency", f"'{entry.heading_id}' está Roteado sem destino válido", relative(entry.path, directory), entry.field_lines.get("ARQUIVO_DESTINO_KB", entry.line)))
        if destination_raw and not entry.destinations and not no_destination:
            issues.append(Issue("ROUTING-INVALID-DESTINATION", "consistency", f"'{entry.heading_id}' não contém código de KB reconhecível", relative(entry.path, directory), entry.field_lines.get("ARQUIVO_DESTINO_KB", entry.line)))
        title = entry.fields.get("TÍTULO")
        if title:
            key = normalize_title(title)
            previous = titles.get(key)
            if previous and previous != entry.heading_id:
                issues.append(Issue("SOURCE-DUPLICATE-TITLE", "consistency", f"'{entry.heading_id}' e '{previous}' têm o mesmo título normalizado", relative(entry.path, directory), entry.field_lines.get("TÍTULO", entry.line)))
            titles.setdefault(key, entry.heading_id)
        link = entry.fields.get("LINK_REFERÊNCIA")
        if link:
            key = normalize_url(link)
            if key:
                previous = urls.get(key)
                if previous and previous != entry.heading_id:
                    issues.append(Issue("SOURCE-DUPLICATE-LINK", "consistency", f"'{entry.heading_id}' e '{previous}' têm o mesmo link canônico", relative(entry.path, directory), entry.field_lines.get("LINK_REFERÊNCIA", entry.line)))
                urls.setdefault(key, entry.heading_id)
    for source_id, occurrences in by_id.items():
        if len(occurrences) > 1:
            issues.append(Issue("LEDGER-DUPLICATE-ID", "consistency", f"'{source_id}' aparece {len(occurrences)} vezes no ledger", relative(occurrences[1].path, directory), occurrences[1].line))


def discover_kbs(directory: Path, issues: list[Issue]) -> tuple[list[KbFile], int]:
    kb_file_paths = paths.kb_paths(directory)
    files: list[KbFile] = []
    by_code: dict[str, list[KbFile]] = {}
    for path in kb_file_paths:
        match = KB_FILENAME_RE.fullmatch(path.name)
        if not match:
            issues.append(Issue("STRUCT-INVALID-KB-FILENAME", "structure", "nome não segue <KB_CODE>_<nome>.md", relative(path, directory), 1))
            continue
        text = read_utf8(path)
        entries = parse_entries(text, path, directory, issues, ledger=False)
        kb_file = KbFile(match.group(1), path, entries)
        files.append(kb_file)
        by_code.setdefault(kb_file.code, []).append(kb_file)
    for code, occurrences in by_code.items():
        if len(occurrences) > 1:
            for duplicate in occurrences[1:]:
                issues.append(Issue("STRUCT-DUPLICATE-KB-CODE", "structure", f"código '{code}' também pertence a '{occurrences[0].path.name}'", relative(duplicate.path, directory), 1))
    return files, len(by_code)


def validate_kbs(ledger_entries: list[Entry], kb_files: list[KbFile], directory: Path, issues: list[Issue]) -> None:
    ledger_by_id: dict[str, Entry] = {}
    for entry in ledger_entries:
        ledger_by_id.setdefault(entry.heading_id, entry)
    kbs_by_code: dict[str, list[KbFile]] = {}
    for kb in kb_files:
        kbs_by_code.setdefault(kb.code, []).append(kb)
        seen: set[str] = set()
        for entry in kb.entries:
            if entry.heading_id in seen:
                issues.append(Issue("KB-DUPLICATE-ID", "consistency", f"'{entry.heading_id}' aparece mais de uma vez nesta KB", relative(kb.path, directory), entry.line))
            seen.add(entry.heading_id)
            ledger_entry = ledger_by_id.get(entry.heading_id)
            if ledger_entry is None:
                issues.append(Issue("ROUTING-ORPHAN", "consistency", f"'{entry.heading_id}' existe na KB, mas não no ledger", relative(kb.path, directory), entry.line))
            elif kb.code not in ledger_entry.destinations:
                issues.append(Issue("ROUTING-UNDECLARED", "consistency", f"'{entry.heading_id}' existe aqui, mas o ledger não declara '{kb.code}'", relative(kb.path, directory), entry.line))
    for entry in ledger_entries:
        if entry.fields.get("STATUS_DE_ROTEAMENTO") != "Roteado":
            continue
        for destination in entry.destinations:
            candidates = kbs_by_code.get(destination, [])
            if not candidates:
                issues.append(Issue("ROUTING-MISSING-KB", "consistency", f"'{entry.heading_id}' declara destino inexistente '{destination}'", relative(entry.path, directory), entry.field_lines.get("ARQUIVO_DESTINO_KB", entry.line)))
                continue
            if not any(entry.heading_id in {item.heading_id for item in kb.entries} for kb in candidates):
                issues.append(Issue("ROUTING-MISSING-ENTRY", "consistency", f"'{entry.heading_id}' não foi gravado em '{destination}'", relative(entry.path, directory), entry.field_lines.get("ARQUIVO_DESTINO_KB", entry.line)))


def validate(directory: Path) -> Report:
    directory = directory.resolve()
    if not directory.exists() or not directory.is_dir():
        raise OperationalError(f"diretório inválido: {directory}")
    ledger_path = directory / paths.LEDGER_PATH
    if not ledger_path.is_file():
        raise OperationalError(f"ledger não encontrado: {ledger_path}")
    report = Report(str(directory))
    ledger_text = read_utf8(ledger_path)
    ledger_entries = parse_entries(ledger_text, ledger_path, directory, report.issues, ledger=True)
    report.ledger_entries = len(ledger_entries)
    validate_ledger(ledger_entries, directory, report.issues)
    kb_files, unique_codes = discover_kbs(directory, report.issues)
    report.kb_files_found = len(paths.kb_paths(directory))
    report.kb_files_parsed = len(kb_files)
    report.kb_codes_unique = unique_codes
    validate_kbs(ledger_entries, kb_files, directory, report.issues)
    report.issues.sort(key=lambda item: (item.path, item.line, item.code, item.message))
    return report


def render(report: Report) -> str:
    lines = [
        f"Fontes interpretadas: {report.ledger_entries}",
        f"KBs: {report.kb_files_found} encontradas | {report.kb_files_parsed} interpretadas | {report.kb_codes_unique} códigos únicos",
        "",
    ]
    if report.ok:
        lines.extend([
            "OK ESTRUTURAL: invariantes ledger↔KB verificadas.",
            "NÃO VERIFICADO: factualidade, fidelidade semântica, causalidade, escopo e atualidade.",
        ])
    else:
        lines.append(f"DIVERGENTE: {len(report.issues)} issue(s) encontrada(s).")
        lines.append("")
        lines.extend(f"- {issue.display()}" for issue in report.issues)
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        report = validate(args.directory)
    except OperationalError as exc:
        print(f"ERRO OPERACIONAL: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2) if args.as_json else render(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
