#!/usr/bin/env python3
"""Convert Markdown + YAML frontmatter to canonical JSON and validate JSON Schema.

Usage examples:
  python3 ferramentas/kb_compile.py entrada.md --schema schemas/domain_knowledge.schema.json
  python3 ferramentas/kb_compile.py entrada.md --output build/entrada.json --pretty
  python3 ferramentas/kb_compile.py entrada.md --check-only

Exit codes:
  0 = conversion and validation succeeded
  1 = validation failed
  2 = operational error, such as unreadable input or invalid schema
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Knowledge Base Markdown Entry",
    "type": "object",
    "required": ["id", "title", "type", "version", "status", "content"],
    "properties": {
        "id": {"type": "string", "minLength": 1},
        "title": {"type": "string", "minLength": 1},
        "type": {"type": "string", "minLength": 1},
        "version": {"type": "string", "pattern": r"^\d+\.\d+\.\d+$"},
        "status": {"type": "string", "minLength": 1},
        "domain": {"type": "string"},
        "subdomain": {"type": "string"},
        "boundedContext": {"type": "string"},
        "aliases": {"type": "array", "items": {"type": "string"}},
        "tags": {"type": "array", "items": {"type": "string"}},
        "relationships": {"type": "object"},
        "retrieval": {"type": "object"},
        "content": {
            "type": "object",
            "required": ["markdown"],
            "properties": {
                "markdown": {"type": "string"},
                "summary": {"type": "string"},
                "concepts": {"type": "array"},
                "businessRules": {"type": "array"},
                "examples": {"type": "array"},
            },
            "additionalProperties": True,
        },
    },
    "additionalProperties": True,
}


class CompileError(Exception):
    """Raised when conversion cannot be completed."""


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"


def split_frontmatter(markdown: str) -> tuple[str, str]:
    """Return frontmatter and Markdown body.

    Frontmatter must be the first block in the file and be delimited by lines
    containing only three hyphens.
    """
    normalized = markdown.lstrip("\ufeff")
    if not normalized.startswith("---\n") and not normalized.startswith("---\r\n"):
        raise CompileError("arquivo Markdown não começa com YAML Frontmatter delimitado por ---")

    lines = normalized.splitlines()
    closing_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            closing_index = index
            break

    if closing_index is None:
        raise CompileError("YAML Frontmatter não possui delimitador final ---")

    frontmatter = "\n".join(lines[1:closing_index])
    body = "\n".join(lines[closing_index + 1 :]).strip()
    return frontmatter, body


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "":
        return ""
    if value in {"null", "Null", "NULL", "~"}:
        return None
    if value in {"true", "True", "TRUE"}:
        return True
    if value in {"false", "False", "FALSE"}:
        return False
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    if value.startswith("[") or value.startswith("{"):
        try:
            return json.loads(value)
        except json.JSONDecodeError as exc:
            if value.startswith("[") and value.endswith("]"):
                items = value[1:-1].strip()
                if not items:
                    return []
                return [parse_scalar(item.strip()) for item in items.split(",")]
            raise CompileError(f"valor inline inválido no frontmatter: {value}") from exc
    return value


def parse_simple_yaml(frontmatter: str) -> dict[str, Any]:
    """Parse a conservative YAML subset using only Python stdlib.

    Supported syntax:
      key: value
      key: [a, b]
      key:
        nested: value
        list:
          - item

    This intentionally rejects advanced YAML features so the canonical JSON
    remains predictable for automation.
    """
    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]

    raw_lines = frontmatter.splitlines()
    for line_number, raw_line in enumerate(raw_lines, start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if "\t" in raw_line:
            raise CompileError(f"linha {line_number}: tabs não são permitidos no frontmatter")

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        while stack and indent <= stack[-1][0]:
            stack.pop()
        if not stack:
            raise CompileError(f"linha {line_number}: indentação inválida")

        parent = stack[-1][1]

        if line.startswith("- "):
            if not isinstance(parent, list):
                raise CompileError(f"linha {line_number}: item de lista sem lista pai")
            item_value = line[2:].strip()
            if ":" in item_value and not item_value.startswith(("'", '"')):
                key, value = item_value.split(":", 1)
                item: dict[str, Any] = {key.strip(): parse_scalar(value)}
                parent.append(item)
                stack.append((indent, item))
            else:
                parent.append(parse_scalar(item_value))
            continue

        if ":" not in line:
            raise CompileError(f"linha {line_number}: esperado formato chave: valor")

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise CompileError(f"linha {line_number}: chave vazia")
        if not isinstance(parent, dict):
            raise CompileError(f"linha {line_number}: chave declarada dentro de lista simples")

        if value:
            parent[key] = parse_scalar(value)
            continue

        next_container: Any = {}
        next_line = next((candidate for candidate in raw_lines[line_number:] if candidate.strip()), "")
        if next_line.strip().startswith("- "):
            next_container = []
        parent[key] = next_container
        stack.append((indent, next_container))

    return root


def normalize_entry(frontmatter: dict[str, Any], body: str) -> dict[str, Any]:
    entry = dict(frontmatter)

    existing_content = entry.get("content")
    if existing_content is None:
        entry["content"] = {"markdown": body}
    elif isinstance(existing_content, dict):
        entry["content"] = {**existing_content, "markdown": body}
    else:
        raise CompileError("campo content no frontmatter deve ser objeto, se existir")

    return entry


def schema_type_matches(value: Any, expected_type: str) -> bool:
    if expected_type == "object":
        return isinstance(value, dict)
    if expected_type == "array":
        return isinstance(value, list)
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected_type == "boolean":
        return isinstance(value, bool)
    if expected_type == "null":
        return value is None
    return True


def validate_json_schema(instance: Any, schema: dict[str, Any], path: str = "$") -> list[ValidationIssue]:
    """Validate the JSON Schema subset used by the KB pipeline."""
    issues: list[ValidationIssue] = []

    expected_type = schema.get("type")
    if isinstance(expected_type, str) and not schema_type_matches(instance, expected_type):
        issues.append(ValidationIssue(path, f"tipo inválido; esperado {expected_type}"))
        return issues
    if isinstance(expected_type, list) and not any(schema_type_matches(instance, item) for item in expected_type):
        issues.append(ValidationIssue(path, f"tipo inválido; esperado um de {expected_type}"))
        return issues

    if "const" in schema and instance != schema["const"]:
        issues.append(ValidationIssue(path, f"valor deve ser {schema['const']!r}"))

    if "enum" in schema and instance not in schema["enum"]:
        issues.append(ValidationIssue(path, f"valor deve estar em {schema['enum']!r}"))

    if isinstance(instance, str):
        min_length = schema.get("minLength")
        if isinstance(min_length, int) and len(instance) < min_length:
            issues.append(ValidationIssue(path, f"texto deve ter pelo menos {min_length} caractere(s)"))
        pattern = schema.get("pattern")
        if isinstance(pattern, str) and not re.search(pattern, instance):
            issues.append(ValidationIssue(path, f"texto não corresponde ao padrão {pattern!r}"))

    if isinstance(instance, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in instance:
                issues.append(ValidationIssue(f"{path}.{key}", "campo obrigatório ausente"))

        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            for key, subschema in properties.items():
                if key in instance and isinstance(subschema, dict):
                    issues.extend(validate_json_schema(instance[key], subschema, f"{path}.{key}"))

        additional = schema.get("additionalProperties", True)
        if additional is False and isinstance(properties, dict):
            allowed = set(properties)
            for key in instance:
                if key not in allowed:
                    issues.append(ValidationIssue(f"{path}.{key}", "campo adicional não permitido"))

    if isinstance(instance, list):
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(instance):
                issues.extend(validate_json_schema(item, item_schema, f"{path}[{index}]"))

    return issues


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise CompileError(f"não foi possível ler {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise CompileError(f"JSON inválido em {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise CompileError(f"schema em {path} deve ser um objeto JSON")
    return data


def compile_markdown(input_path: Path, schema: dict[str, Any]) -> tuple[dict[str, Any], list[ValidationIssue]]:
    try:
        markdown = input_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise CompileError(f"não foi possível ler {input_path}: {exc}") from exc

    frontmatter_raw, body = split_frontmatter(markdown)
    frontmatter = parse_simple_yaml(frontmatter_raw)
    entry = normalize_entry(frontmatter, body)
    issues = validate_json_schema(entry, schema)
    return entry, issues


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Converte Markdown com YAML Frontmatter para JSON canônico e valida contra JSON Schema."
    )
    parser.add_argument("input", type=Path, help="Arquivo Markdown de entrada.")
    parser.add_argument("--schema", type=Path, help="Arquivo JSON Schema. Se omitido, usa schema padrão embutido.")
    parser.add_argument("--output", "-o", type=Path, help="Arquivo JSON de saída.")
    parser.add_argument("--pretty", action="store_true", help="Grava JSON com indentação.")
    parser.add_argument("--check-only", action="store_true", help="Apenas valida; não imprime nem grava JSON.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        schema = load_json(args.schema) if args.schema else DEFAULT_SCHEMA
        entry, issues = compile_markdown(args.input, schema)
    except CompileError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 2

    if issues:
        print(f"{len(issues)} erro(s) de validação:", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1

    if args.check_only:
        print("OK: documento convertido e validado contra o JSON Schema.")
        return 0

    indent = 2 if args.pretty else None
    output = json.dumps(entry, ensure_ascii=False, indent=indent)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output + "\n", encoding="utf-8")
        print(f"OK: JSON canônico gravado em {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
