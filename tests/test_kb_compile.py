import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPILER = ROOT / "ferramentas" / "kb_compile.py"
EXAMPLE_MD = ROOT / "exemplos" / "domain_customer.md"
EXAMPLE_JSON = ROOT / "exemplos" / "domain_customer.json"
SCHEMA = ROOT / "schemas" / "domain_knowledge.schema.json"


def run_compiler(*args):
    return subprocess.run(
        [sys.executable, str(COMPILER), *map(str, args)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class KbCompileTests(unittest.TestCase):
    def test_check_only_accepts_canonical_example(self):
        result = run_compiler(EXAMPLE_MD, "--schema", SCHEMA, "--check-only")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("OK: documento convertido e validado", result.stdout)

    def test_generated_json_matches_canonical_example(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "domain_customer.json"
            result = run_compiler(EXAMPLE_MD, "--schema", SCHEMA, "--output", output, "--pretty")
            self.assertEqual(result.returncode, 0, result.stderr)
            generated = json.loads(output.read_text(encoding="utf-8"))
            expected = json.loads(EXAMPLE_JSON.read_text(encoding="utf-8"))
            self.assertEqual(generated, expected)

    def test_missing_frontmatter_is_operational_error(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "missing-frontmatter.md"
            source.write_text("# Documento sem front matter\n", encoding="utf-8")
            result = run_compiler(source, "--schema", SCHEMA, "--check-only")
            self.assertEqual(result.returncode, 2)
            self.assertIn("não começa com YAML Frontmatter", result.stderr)

    def test_invalid_schema_json_is_operational_error(self):
        with tempfile.TemporaryDirectory() as directory:
            schema = Path(directory) / "invalid.schema.json"
            schema.write_text("{invalid", encoding="utf-8")
            result = run_compiler(EXAMPLE_MD, "--schema", schema, "--check-only")
            self.assertEqual(result.returncode, 2)
            self.assertIn("JSON inválido", result.stderr)

    def test_missing_required_field_is_validation_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "missing-id.md"
            markdown = EXAMPLE_MD.read_text(encoding="utf-8").replace("id: domain.customer\n", "", 1)
            source.write_text(markdown, encoding="utf-8")
            result = run_compiler(source, "--schema", SCHEMA, "--check-only")
            self.assertEqual(result.returncode, 1)
            self.assertIn("$.id: campo obrigatório ausente", result.stderr)


if __name__ == "__main__":
    unittest.main()
