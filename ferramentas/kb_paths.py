"""Caminhos canônicos da base de conhecimento."""
from __future__ import annotations

from pathlib import Path


CONTENT_DIR = Path("conteudo")
DOMAINS_DIR = CONTENT_DIR / "dominios"
PROJECTS_DIR = CONTENT_DIR / "projetos"
LEDGER_PATH = CONTENT_DIR / "FONTES_REGISTRADAS.md"

GOVERNANCE_DIR = Path("governanca")
PROTOCOL_PATH = GOVERNANCE_DIR / "PROTOCOLO.md"
ARCHITECTURE_PATH = GOVERNANCE_DIR / "REGISTRO_FONTES.md"
TEMPLATE_PATH = GOVERNANCE_DIR / "TEMPLATE.md"
VERIFICATION_CONTRACT_PATH = GOVERNANCE_DIR / "LEDGER_KB_VERIFY.md"

REQUIRED_DIRECTORIES = (CONTENT_DIR, DOMAINS_DIR, PROJECTS_DIR, GOVERNANCE_DIR)
REQUIRED_GOVERNANCE_FILES = (
    PROTOCOL_PATH,
    ARCHITECTURE_PATH,
    TEMPLATE_PATH,
    VERIFICATION_CONTRACT_PATH,
)


def kb_paths(root: Path) -> list[Path]:
    """Retorna todas as KBs publicadas nas duas categorias canônicas."""
    return sorted((root / DOMAINS_DIR).glob("KB-*.md")) + sorted(
        (root / PROJECTS_DIR).glob("KB-*.md")
    )
