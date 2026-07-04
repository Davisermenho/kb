import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("checker", ROOT / "check_kb_consistency.py")
checker = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = checker
SPEC.loader.exec_module(checker)


def ledger_entry(source_id="FONTE-2026-ORG-TEMA", **overrides):
    values = {
        "ID_FONTE": source_id,
        "TÍTULO": "Título único",
        "LINK_REFERÊNCIA": "https://example.com/a-b",
        "ARQUIVO_DESTINO_KB": "KB-01 — Teste",
        "STATUS_DE_ROTEAMENTO": "Roteado",
    }
    values.update(overrides)
    fields = "\n".join(f"- **{key}:** {value}" for key, value in values.items() if value is not None)
    return f"### {source_id}\n{fields}\n"


class CheckerTests(unittest.TestCase):
    def make_base(self, entry=None, kb_id="FONTE-2026-ORG-TEMA"):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        (root / "FONTES_REGISTRADAS.md").write_text("# Ledger\n\n## Registros\n\n" + (entry or ledger_entry()), encoding="utf-8")
        (root / "KB-01_Teste.md").write_text(f"# KB\n\n## Registros\n\n### {kb_id}\n- Conteúdo: teste\n", encoding="utf-8")
        return temp, root

    def codes(self, report):
        return {issue.code for issue in report.issues}

    def test_consistent_base_passes(self):
        temp, root = self.make_base()
        self.addCleanup(temp.cleanup)
        self.assertTrue(checker.validate(root).ok)

    def test_missing_registros_fails_closed(self):
        temp, root = self.make_base()
        self.addCleanup(temp.cleanup)
        (root / "FONTES_REGISTRADAS.md").write_text("# Ledger\n", encoding="utf-8")
        self.assertIn("STRUCT-MISSING-SECTION", self.codes(checker.validate(root)))

    def test_missing_required_field(self):
        temp, root = self.make_base(ledger_entry(**{"ID_FONTE": None}))
        self.addCleanup(temp.cleanup)
        self.assertIn("STRUCT-MISSING-FIELD", self.codes(checker.validate(root)))

    def test_accepts_bold_colon_inside_field_style(self):
        temp, root = self.make_base()
        self.addCleanup(temp.cleanup)
        self.assertNotIn("STRUCT-MISSING-FIELD", self.codes(checker.validate(root)))

    def test_empty_kb_placeholder_is_allowed(self):
        temp, root = self.make_base()
        self.addCleanup(temp.cleanup)
        (root / "KB-02_Vazia.md").write_text(
            "# KB\n\n## Registros\n\n_Nenhum registro até o momento._\n",
            encoding="utf-8",
        )
        self.assertNotIn("STRUCT-ORPHAN-CONTENT", self.codes(checker.validate(root)))

    def test_invalid_status(self):
        temp, root = self.make_base(ledger_entry(**{"STATUS_DE_ROTEAMENTO": "Pronto"}))
        self.addCleanup(temp.cleanup)
        self.assertIn("STRUCT-INVALID-STATUS", self.codes(checker.validate(root)))

    def test_routed_without_destination(self):
        temp, root = self.make_base(ledger_entry(**{"ARQUIVO_DESTINO_KB": "Nenhum"}))
        self.addCleanup(temp.cleanup)
        self.assertIn("ROUTING-EMPTY", self.codes(checker.validate(root)))

    def test_duplicate_kb_code_is_not_overwritten(self):
        temp, root = self.make_base()
        self.addCleanup(temp.cleanup)
        (root / "KB-01_Outra.md").write_text("# KB\n\n## Registros\n", encoding="utf-8")
        report = checker.validate(root)
        self.assertEqual(report.kb_files_found, 2)
        self.assertIn("STRUCT-DUPLICATE-KB-CODE", self.codes(report))

    def test_urls_with_different_path_punctuation_do_not_collide(self):
        first = ledger_entry()
        second = ledger_entry("FONTE-2026-ORG-OUTRO", **{
            "TÍTULO": "Outro título",
            "LINK_REFERÊNCIA": "https://example.com/a/b",
        })
        temp, root = self.make_base(first + "\n" + second)
        self.addCleanup(temp.cleanup)
        (root / "KB-01_Teste.md").write_text(
            "# KB\n\n## Registros\n\n### FONTE-2026-ORG-TEMA\n- Conteúdo: a\n\n### FONTE-2026-ORG-OUTRO\n- Conteúdo: b\n",
            encoding="utf-8",
        )
        self.assertNotIn("SOURCE-DUPLICATE-LINK", self.codes(checker.validate(root)))

    def test_duplicate_title_and_link_are_reported(self):
        first = ledger_entry()
        second = ledger_entry("FONTE-2026-ORG-OUTRO")
        temp, root = self.make_base(first + "\n" + second)
        self.addCleanup(temp.cleanup)
        codes = self.codes(checker.validate(root))
        self.assertIn("SOURCE-DUPLICATE-TITLE", codes)
        self.assertIn("SOURCE-DUPLICATE-LINK", codes)

    def test_orphan_and_missing_are_reported(self):
        temp, root = self.make_base(kb_id="FONTE-2026-ORG-ORFA")
        self.addCleanup(temp.cleanup)
        codes = self.codes(checker.validate(root))
        self.assertIn("ROUTING-ORPHAN", codes)
        self.assertIn("ROUTING-MISSING-ENTRY", codes)

    def test_missing_ledger_is_operational_error(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(checker.OperationalError):
                checker.validate(Path(directory))


if __name__ == "__main__":
    unittest.main()
