# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cláudio Drews
"""Shared test helpers (no third-party test framework needed: `python -m unittest discover -s tests`)."""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
FIXTURES = ROOT / "tests" / "fixtures"
sys.path.insert(0, str(SCRIPTS))


def have_render_stack():
    return bool(shutil.which("bwrap") and (shutil.which("google-chrome") or shutil.which("chromium")
                                           or shutil.which("chromium-browser")))
