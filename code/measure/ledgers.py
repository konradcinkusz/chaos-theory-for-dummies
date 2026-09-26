"""Appendix E's ledgers, counted from the tree rather than typed.

Each figure is a promise the book makes to its reader -- how many of its
chapters are written, how many listings run, how many questions it asks --
and a promise typed by hand goes stale the day the book changes. These are
recomputed by `make numbers`, so `make verify` fails when the book moves and
the appendix does not.

Counts are per edition: the two editions contain the same chapters, labs and
figures, and tools/parity.py checks that they do.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from _values import Values

CODE = Path(__file__).resolve().parents[1]
ROOT = CODE.parent
COMMENT = re.compile(r"(?<!\\)%.*$", re.M)


def src(path: Path) -> str:
    return COMMENT.sub("", path.read_text(encoding="utf8"))


manifest = json.loads((ROOT / "tools" / "chapters.json").read_text("utf8"))
chapters = [ROOT / "chapters" / "en" / f"{c['file']}.tex"
            for c in manifest["chapters"]]
texts = [src(p) for p in chapters]
written = [t for t in texts if "\\chapterstub{" not in t]

listings = [p for d in sorted(CODE.glob("ch[0-9][0-9]"))
            for p in d.rglob("*.py") if not p.name.startswith("_")]
labs = sorted(p for p in CODE.glob("labs/ch[0-9][0-9]/l[0-9]*.py"))
tests = sum(len(re.findall(r"^def test_", p.read_text("utf8"), re.M))
            for p in CODE.glob("labs/ch[0-9][0-9]/test_*.py"))
plots = sum(len(re.findall(r'^@plot\("', p.read_text("utf8"), re.M))
            for p in CODE.glob("plots/ch[0-9][0-9].py"))
diagrams = len(list((ROOT / "figures" / "mermaid" / "en").glob("*.mmd")))
transcripts = len(list((ROOT / "figures" / "transcripts").glob("*.txt")))
values = sum(len(re.findall(r"^\\pyval", p.read_text("utf8"), re.M))
             for p in (ROOT / "figures" / "values").glob("*.tex")
             if p.stem not in ("all", "ledgers"))
thinks = sum(t.count("\\begin{think}") for t in written)
answers = sum(t.count("\\answerto{") for t in written)
verify = sum(t.count("\\begin{verifybox}") for t in written)
traps = sum(len(json.loads(p.read_text("utf8")))
            for p in (ROOT / "notes" / "traps").glob("ch[0-9][0-9].json"))
library = sum(1 for p in (CODE / "src" / "chaoslab").glob("*.py")
              for line in p.read_text("utf8").splitlines() if line.strip())

v = Values("ledgers")
v.num("chapters", len(manifest["chapters"]))
v.num("written", len(written))
v.num("listings", len(listings))
v.num("labs", len(labs))
v.num("tests", tests)
v.num("plots", plots)
v.num("diagrams", diagrams)
v.num("transcripts", transcripts)
v.num("values", values)
v.num("thinks", thinks)
v.num("answers", answers)
v.num("verify", verify)
v.num("traps", traps)
v.num("library", library)
v.write()
