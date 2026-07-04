#!/usr/bin/env python3
"""Executa os gates auditáveis no encerramento da sessão Claude Code."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


KB_DIR = Path(__file__).resolve().parents[2]
VALIDATOR = KB_DIR / "kb_validate.py"


def main() -> int:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(KB_DIR)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        sys.stderr.write(result.stdout + result.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
