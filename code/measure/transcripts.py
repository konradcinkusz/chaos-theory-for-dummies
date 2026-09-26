#!/usr/bin/env python3
"""Run every listing whose output the book quotes, and write the transcript.

A listing opts in with a line near its top:

    # transcript: ch05-four-rates

and its stdout, run from code/ on the pinned interpreter, becomes
figures/transcripts/ch05-four-rates.txt, which the page pulls in with
\\transcript{ch05-four-rates}. No registry to edit: the listing says what it
is quoted as, so two chapters written at once cannot collide in this file.

Four guards, each a way a transcript has gone wrong in a sibling book:

  * ASCII only -- listings aborts the build on a multi-byte character;
  * no control characters -- an ESC or a tab prints as mojibake or runs past
    the 79 columns the width check has already cleared;
  * 79 columns -- a long line wraps silently with an arrow in the middle of
    what the reader is meant to compare with their own run;
  * no memory addresses -- `<object at 0x7f...>` differs on every run, so a
    committed transcript carrying one fails `make verify` for no defect.

Run from code/:   uv run python measure/transcripts.py [chNN ...]
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

CODE = Path(__file__).resolve().parents[1]
OUT = CODE.parent / "figures" / "transcripts"
WIDTH = 79
RE_MARK = re.compile(r"^#\s*transcript:\s*(\S+)\s*$", re.M)


def listings(only: set[str]) -> list[tuple[Path, str]]:
    found = []
    for d in sorted(CODE.glob("ch[0-9][0-9]")):
        if only and d.name not in only:
            continue
        for p in sorted(d.rglob("*.py")):
            head = "\n".join(p.read_text(encoding="utf8").splitlines()[:25])
            for stem in RE_MARK.findall(head):
                if not stem.startswith(d.name + "-"):
                    raise SystemExit(f"{p}: transcript {stem!r} must start "
                                     f"with {d.name}-")
                found.append((p, stem))
    return found


def check(stem: str, text: str) -> None:
    for i, line in enumerate(text.splitlines(), 1):
        bad = [ch for ch in line if ord(ch) > 127 or (ord(ch) < 32)]
        if bad:
            raise SystemExit(f"{stem}:{i} carries {bad[0]!r}; transcripts "
                             f"are ASCII without control characters")
        if len(line) > WIDTH:
            raise SystemExit(f"{stem}:{i} is {len(line)} columns (limit "
                             f"{WIDTH}); shorten the listing's output")
        if re.search(r"0x[0-9a-f]{6,}", line):
            raise SystemExit(f"{stem}:{i} carries a memory address, which "
                             f"differs on every run")


def main() -> int:
    only = set(sys.argv[1:])
    OUT.mkdir(parents=True, exist_ok=True)
    seen: set[str] = set()
    for path, stem in listings(only):
        if stem in seen:
            raise SystemExit(f"transcript {stem!r} is claimed twice")
        seen.add(stem)
        result = subprocess.run(
            [sys.executable, str(path.relative_to(CODE))],
            cwd=CODE, capture_output=True, text=True, timeout=600,
        )
        if result.returncode != 0 or result.stderr:
            raise SystemExit(f"{path.relative_to(CODE)} failed:\n"
                             f"{result.stdout}\n{result.stderr}")
        check(stem, result.stdout)
        (OUT / f"{stem}.txt").write_text(result.stdout, encoding="utf8")
        print(f"  transcript: figures/transcripts/{stem}.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
