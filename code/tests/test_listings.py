"""Every listing file under chNN/ runs as a script and exits cleanly.

A real subprocess, not runpy in-process: the book tells the reader to run a
listing as `uv run python chNN/file.py` from code/, and a subprocess is what
makes that claim checked rather than merely similar. A file whose name
starts with an underscore is a helper another listing imports, and is
exercised through that listing rather than run on its own.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

CODE = Path(__file__).resolve().parent.parent
LISTINGS = sorted(
    p
    for d in sorted(CODE.glob("ch[0-9][0-9]"))
    for p in d.rglob("*.py")
    if not p.name.startswith("_")
)


def _listing_id(p: Path) -> str:
    return p.relative_to(CODE).as_posix()


@pytest.mark.parametrize("path", LISTINGS, ids=_listing_id)
def test_listing_runs(path: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(path.relative_to(CODE))],
        cwd=CODE,
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert result.returncode == 0, (
        f"{path.name} exited {result.returncode}\n"
        f"--- stdout ---\n{result.stdout}"
        f"--- stderr ---\n{result.stderr}"
    )
    assert result.stderr == "", (
        f"{path.name} wrote to stderr:\n{result.stderr}")


def test_there_is_at_least_one_listing() -> None:
    # A parametrised test over an empty list is silently skipped, and a
    # check that passes because it read nothing is worse than no check.
    assert LISTINGS, "no listing files found under code/chNN/"
