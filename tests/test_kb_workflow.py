import json
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import kb_workflow
import kb_validate


class WorkflowTests(unittest.TestCase):
    def test_create_run_creates_manifest_and_draft(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            run = kb_workflow.create_run(root, "RUN-TEST", "Testar", "medio", ["A.md"], ["editar"])
            manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["run_id"], "RUN-TEST")
            self.assertIn("A.md", manifest["arquivos_permitidos"])
            self.assertIn(".kb/runs/RUN-TEST/manifest.json", manifest["arquivos_permitidos"])
            self.assertEqual(manifest["causalidade"], [])
            self.assertIn("RASCUNHO", (run / "draft.md").read_text(encoding="utf-8"))
            state = json.loads((run / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["state"], "RASCUNHO")

    def test_duplicate_run_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            kb_workflow.create_run(root, "RUN-TEST", "Testar", "baixo", [], ["editar"])
            with self.assertRaises(FileExistsError):
                kb_workflow.create_run(root, "RUN-TEST", "Testar", "baixo", [], ["editar"])

    def test_lock_is_atomic_and_owned(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            kb_workflow.acquire_lock(root, "RUN-A")
            with self.assertRaises(RuntimeError):
                kb_workflow.acquire_lock(root, "RUN-B")
            with self.assertRaises(RuntimeError):
                kb_workflow.release_lock(root, "RUN-B")
            kb_workflow.release_lock(root, "RUN-A")
            self.assertFalse(kb_workflow.lock_path(root).exists())

    def test_state_machine_accepts_sequence_and_rejects_jump(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            kb_workflow.create_run(root, "RUN-TEST", "Testar", "baixo", [], ["editar"])
            state = kb_workflow.transition(root, "RUN-TEST", "EXTRAÍDO", "extração pronta")
            self.assertEqual(state["state"], "EXTRAÍDO")
            with self.assertRaises(RuntimeError):
                kb_workflow.transition(root, "RUN-TEST", "PUBLICADO", "salto indevido")

    def test_prewrite_duplicate_candidates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "FONTES_REGISTRADAS.md").write_text(
                "# Ledger\n\n## Registros\n\n"
                "### FONTE-2026-ORG-TEMA\n"
                "- ID_FONTE: FONTE-2026-ORG-TEMA\n"
                "- TÍTULO: Uma Fonte\n"
                "- AUTOR_ORGANIZAÇÃO: Org\n"
                "- LINK_REFERÊNCIA: https://example.com/fonte\n"
                "- ARQUIVO_DESTINO_KB: KB-01\n"
                "- STATUS_DE_ROTEAMENTO: Roteado\n",
                encoding="utf-8",
            )
            candidates = kb_workflow.duplicate_candidates(root, "Uma Fonte", "https://example.com/fonte/", None)
            self.assertEqual(candidates[0]["id_fonte"], "FONTE-2026-ORG-TEMA")
            self.assertEqual(set(candidates[0]["motivos"]), {"titulo", "url"})

    def test_review_diff_excludes_run_artifacts(self):
        # Contrato estrutural: review.json/validation.json não podem alterar o
        # hash do produto que a própria revisão precisa assinar.
        source = Path(kb_validate.__file__).read_text(encoding="utf-8")
        self.assertIn(":(exclude).kb/runs/{run_id}/**", source)
        self.assertIn("core.quotepath=false", source)


if __name__ == "__main__":
    unittest.main()
