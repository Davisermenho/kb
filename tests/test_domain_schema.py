import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "domain_knowledge.schema.json"
MARKDOWN_PATH = ROOT / "exemplos" / "domain_customer.md"
JSON_PATH = ROOT / "exemplos" / "domain_customer.json"


def parse_scalar(value):
    if value == "true":
        return True
    if value == "false":
        return False
    if value == "[]":
        return []
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1]
        return [item.strip() for item in inner.split(",") if item.strip()]
    return value


def parse_frontmatter_mapping(lines, start=0, indent=0):
    result = {}
    index = start
    while index < len(lines):
        current_indent = len(lines[index]) - len(lines[index].lstrip(" "))
        if current_indent < indent:
            break
        if current_indent > indent:
            raise ValueError(f"indentação inesperada na linha: {lines[index]}")
        key, separator, raw_value = lines[index].strip().partition(":")
        if not separator:
            raise ValueError(f"campo sem dois-pontos: {lines[index]}")
        value = raw_value.strip()
        index += 1
        if value:
            result[key] = parse_scalar(value)
            continue
        if index >= len(lines):
            result[key] = {}
            continue
        child_indent = len(lines[index]) - len(lines[index].lstrip(" "))
        if lines[index].strip().startswith("- "):
            items = []
            while index < len(lines):
                item_indent = len(lines[index]) - len(lines[index].lstrip(" "))
                if item_indent != child_indent or not lines[index].strip().startswith("- "):
                    break
                items.append(parse_scalar(lines[index].strip()[2:].strip()))
                index += 1
            result[key] = items
        else:
            result[key], index = parse_frontmatter_mapping(lines, index, child_indent)
    return result, index


def split_markdown(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("front matter inicial ausente")
    frontmatter, separator, body = text[4:].partition("\n---\n")
    if not separator:
        raise ValueError("front matter final ausente")
    metadata, consumed = parse_frontmatter_mapping(frontmatter.splitlines())
    if consumed != len(frontmatter.splitlines()):
        raise ValueError("front matter não consumido integralmente")
    return metadata, body.strip()


def validate_schema(instance, schema, path="$"):
    expected_type = schema.get("type")
    type_map = {
        "object": dict,
        "array": list,
        "string": str,
        "boolean": bool,
        "integer": int,
        "number": (int, float),
        "null": type(None),
    }
    if expected_type and not isinstance(instance, type_map[expected_type]):
        raise AssertionError(f"{path}: tipo esperado {expected_type}")
    if "const" in schema and instance != schema["const"]:
        raise AssertionError(f"{path}: valor diferente de const")
    if "enum" in schema and instance not in schema["enum"]:
        raise AssertionError(f"{path}: valor fora do enum")
    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            raise AssertionError(f"{path}: string menor que minLength")
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            raise AssertionError(f"{path}: string não corresponde ao pattern")
    if isinstance(instance, dict):
        missing = set(schema.get("required", [])) - set(instance)
        if missing:
            raise AssertionError(f"{path}: campos obrigatórios ausentes: {sorted(missing)}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extra = set(instance) - set(properties)
            if extra:
                raise AssertionError(f"{path}: propriedades adicionais: {sorted(extra)}")
        for key, value in instance.items():
            if key in properties:
                validate_schema(value, properties[key], f"{path}.{key}")
    if isinstance(instance, list) and "items" in schema:
        for index, value in enumerate(instance):
            validate_schema(value, schema["items"], f"{path}[{index}]")


class DomainSchemaTests(unittest.TestCase):
    def setUp(self):
        self.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.example = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    def test_domain_customer_json_satisfies_schema(self):
        self.assertEqual(self.schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        validate_schema(self.example, self.schema)

    def test_markdown_frontmatter_and_body_match_json(self):
        metadata, body = split_markdown(MARKDOWN_PATH)
        metadata.setdefault("content", {})["markdown"] = body
        self.assertEqual(metadata, self.example)


if __name__ == "__main__":
    unittest.main()
