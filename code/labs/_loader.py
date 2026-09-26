"""Load a lab from the reader's starter or from the reference solution.

Every lab is two files: the starter the reader edits, and the solution
under solutions/. A test imports the lab through here rather than with a
plain import, so the SAME test runs against whichever the environment names:

    uv run pytest -k l05_01                  # the starter -- you
    CHAOS_SOLUTIONS=1 uv run pytest          # the solutions -- CI

The starter is expected to FAIL its test: a lab whose starter already passes
is not a lab. The build checks that too, with CHAOS_STARTERS=fail, under
which conftest.py marks every lab test as a strict expected failure.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path
from types import ModuleType

HERE = Path(__file__).resolve().parent


def load(chapter: str, key: str) -> ModuleType:
    """Import labs/<chapter>/<key>.py, or its solution under CI."""
    folder = HERE / chapter
    # Off is unset, empty or "0"; a bare truthiness test would read "0" as on.
    if os.environ.get("CHAOS_SOLUTIONS", "0") not in ("0", ""):
        folder = folder / "solutions"
    path = folder / f"{key}.py"
    spec = importlib.util.spec_from_file_location(f"lab_{key}", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load lab from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module
