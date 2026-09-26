#!/usr/bin/env python3
"""The source-level gates: everything that can be checked without a PDF.

Each check reads the source and needs no build, so they run in seconds and
belong BEFORE a build rather than inside it (the sibling books paid for that
ordering). Run one, several or all:

    python3 tools/check_structure.py --all
    python3 tools/check_structure.py --think --labs
    python3 tools/check_structure.py --words --soft     # report, never fail

  --stubs        count the chapters and appendices still carrying a stub
  --listings     every \\pyfile / \\pyregion names a file and region that exist
  --labs         every lab has a starter, a solution and a test, its key names
                 its chapter, and its ordinal matches where it prints
  --transcripts  every \\transcript{} has a committed file, and is a stem
  --plots        every \\plotfig key is produced by code/plots/, and every
                 plot the scripts produce is placed
  --lines        no file under code/ and no transcript is wider than 79
  --pins         preamble.tex and code/pyproject.toml pin the same versions
  --words        prose in a written chapter is inside its word budget
  --think        every question is answered, and every answer has a question
  --skeleton     every written chapter has outcomes, a summary, the self-check
                 and a checkpoint whose every item carries an answer
  --traps        Appendix B prints every entry of notes/02-traps.md, once

Exit 0 when every requested check passes (or with --soft), 1 otherwise.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGS = ("en", "pl")
RE_COMMENT = re.compile(r"(?<!\\)%.*$", re.M)
WIDTH = 79


def manifest() -> dict:
    return json.loads((ROOT / "tools" / "chapters.json").read_text(encoding="utf8"))


def strip(src: str) -> str:
    return RE_COMMENT.sub("", src)


def written(path: Path) -> bool:
    """A file with no \\chapterstub{} left in its uncommented source."""
    return path.is_file() and "\\chapterstub{" not in strip(
        path.read_text(encoding="utf8"))


def chapter_files(lang: str = "en") -> list[tuple[dict, Path]]:
    m = manifest()
    return [(c, ROOT / "chapters" / lang / f"{c['file']}.tex") for c in m["chapters"]]


def all_sources() -> list[Path]:
    out = []
    for tree in ("chapters", "appendices", "frontmatter"):
        for lang in LANGS:
            d = ROOT / tree / lang
            if d.is_dir():
                out += sorted(d.glob("*.tex"))
    return out


def balanced(src: str, i: int) -> tuple[str, int]:
    while i < len(src) and src[i] in " \t\n":
        i += 1
    if i >= len(src) or src[i] != "{":
        return "", i
    depth, j = 0, i
    while j < len(src):
        c = src[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return src[i + 1:j], j + 1
        j += 1
    return src[i + 1:], len(src)


def macro_args(src: str, name: str, n: int) -> list[tuple[list[str], int]]:
    """Every call of \\name with its first n brace arguments and its line."""
    out = []
    for m in re.finditer(r"\\" + name + r"(?![A-Za-z])", src):
        pos, args = m.end(), []
        for _ in range(n):
            a, pos = balanced(src, pos)
            args.append(a)
        out.append((args, src.count("\n", 0, m.start()) + 1))
    return out


class Result:
    def __init__(self, name: str) -> None:
        self.name = name
        self.fails: list[str] = []
        self.notes: list[str] = []

    def fail(self, msg: str) -> None:
        self.fails.append(msg)

    def note(self, msg: str) -> None:
        self.notes.append(msg)

    def show(self) -> bool:
        head = "FAIL" if self.fails else "ok"
        print(f"== {self.name}: {head}")
        for n in self.notes:
            print(f"   {n}")
        for f in self.fails[:40]:
            print(f"   FAIL {f}")
        if len(self.fails) > 40:
            print(f"   ... and {len(self.fails) - 40} more")
        return not self.fails


# ---------------------------------------------------------------------------

def check_stubs() -> Result:
    r = Result("stubs")
    m = manifest()
    for lang in LANGS:
        stubs = [c["key"] for c in m["chapters"]
                 if not written(ROOT / "chapters" / lang / f"{c['file']}.tex")]
        apps = [a["key"] for a in m["appendices"]
                if not written(ROOT / "appendices" / lang / f"{a['file']}.tex")]
        r.note(f"{lang}: {len(stubs)} of {len(m['chapters'])} chapters are stubs"
               + (f" ({', '.join(stubs)})" if stubs else "")
               + f"; {len(apps)} of {len(m['appendices'])} appendices"
               + (f" ({', '.join(apps)})" if apps else ""))
        if stubs or apps:
            r.fail(f"{lang}: {len(stubs) + len(apps)} stubs remain")
    return r


def check_listings() -> Result:
    r = Result("listings")
    count = 0
    for p in all_sources():
        src = strip(p.read_text(encoding="utf8"))
        rel = p.relative_to(ROOT)
        for (path, cap, lab), line in macro_args(src, "pyfile", 3):
            count += 1
            if not (ROOT / path).is_file():
                r.fail(f"{rel}:{line} \\pyfile names {path}, which does not exist")
        for (path, region, cap, lab), line in macro_args(src, "pyregion", 4):
            count += 1
            f = ROOT / path
            if not f.is_file():
                r.fail(f"{rel}:{line} \\pyregion names {path}, which does not exist")
                continue
            text = f.read_text(encoding="utf8")
            if f"# --8<-- [start:{region}]" not in text or \
               f"# --8<-- [end:{region}]" not in text:
                r.fail(f"{rel}:{line} region {region!r} is not marked in {path}")
    r.note(f"{count} listing references across both editions")
    return r


def check_labs() -> Result:
    r = Result("labs")
    count = 0
    for c, _ in chapter_files():
        num = int(c["id"])
        for lang in LANGS:
            p = ROOT / "chapters" / lang / f"{c['file']}.tex"
            if not p.is_file():
                continue
            src = strip(p.read_text(encoding="utf8"))
            for k, m in enumerate(re.finditer(r"\\begin\{lab\}", src), start=1):
                key, _ = balanced(src, m.end())
                key = key.strip()
                line = src.count("\n", 0, m.start()) + 1
                rel = p.relative_to(ROOT)
                want = f"l{num:02d}_{k:02d}_"
                if not key.startswith(want):
                    r.fail(f"{rel}:{line} lab {key!r} prints as Lab {num}.{k}; "
                           f"its key must start {want!r}")
                if lang != "en":
                    continue
                count += 1
                d = ROOT / "code" / "labs" / f"ch{num:02d}"
                for f in (d / f"{key}.py", d / "solutions" / f"{key}.py",
                          d / f"test_{key}.py"):
                    if not f.is_file():
                        r.fail(f"{rel}:{line} lab {key!r} is missing {f.relative_to(ROOT)}")
    r.note(f"{count} labs, each a starter, a solution and a test")
    return r


def check_transcripts() -> Result:
    r = Result("transcripts")
    used = set()
    for p in all_sources():
        src = strip(p.read_text(encoding="utf8"))
        for (stem,), line in macro_args(src, "transcript", 1):
            stem = stem.strip()
            used.add(stem)
            if "/" in stem or stem.endswith(".txt"):
                r.fail(f"{p.relative_to(ROOT)}:{line} \\transcript takes a stem, not a path: {stem!r}")
            elif not (ROOT / "figures" / "transcripts" / f"{stem}.txt").is_file():
                r.fail(f"{p.relative_to(ROOT)}:{line} no figures/transcripts/{stem}.txt "
                       f"-- run `make numbers`, or the stem is a typo")
    made = {f.stem for f in (ROOT / "figures" / "transcripts").glob("*.txt")}
    for stem in sorted(made - used):
        r.fail(f"figures/transcripts/{stem}.txt is generated and never printed")
    r.note(f"{len(used)} transcripts on the page")
    return r


RE_PLOTKEY = re.compile(r"""@plot\(\s*["']([^"']+)["']""")


def check_plots() -> Result:
    r = Result("plots")
    produced: dict[str, str] = {}
    for f in sorted((ROOT / "code" / "plots").glob("ch*.py")):
        for key in RE_PLOTKEY.findall(f.read_text(encoding="utf8")):
            if key in produced:
                r.fail(f"plot {key!r} is produced by both {produced[key]} and {f.name}")
            produced[key] = f.name
            if not key.startswith(f.stem[:4] + "-"):
                r.fail(f"{f.name} produces {key!r}; a plot key starts with its chapter, "
                       f"{f.stem[:4]}-")
    used = set()
    for p in all_sources():
        src = strip(p.read_text(encoding="utf8"))
        for (key, cap, man), line in macro_args(src, "plotfig", 3):
            used.add(key)
            if key not in produced:
                r.fail(f"{p.relative_to(ROOT)}:{line} \\plotfig{{{key}}} -- no script "
                       f"under code/plots/ produces it")
    for key in sorted(set(produced) - used):
        r.fail(f"plot {key!r} is produced by {produced[key]} and never placed")
    r.note(f"{len(used)} plots placed, {len(produced)} produced")
    return r


def check_lines() -> Result:
    r = Result("lines")
    n = 0
    files = [p for p in (ROOT / "code").rglob("*.py")
             if ".venv" not in p.parts and "__pycache__" not in p.parts]
    files += sorted((ROOT / "figures" / "transcripts").glob("*.txt"))
    for p in files:
        n += 1
        for i, line in enumerate(p.read_text(encoding="utf8").splitlines(), 1):
            if len(line) > WIDTH:
                r.fail(f"{p.relative_to(ROOT)}:{i} is {len(line)} columns (limit {WIDTH})")
    r.note(f"{n} files held to {WIDTH} columns")
    return r


PINS = {"numpyver": "numpy", "matplotlibver": "matplotlib",
        "pytestver": "pytest", "ruffver": "ruff"}


def check_pins() -> Result:
    r = Result("pins")
    pre = (ROOT / "preamble.tex").read_text(encoding="utf8")
    macros = dict(re.findall(r"\\newcommand\{\\([a-z]+ver|pypatch)\}\{([^}]*)\}", pre))
    pyproject = (ROOT / "code" / "pyproject.toml").read_text(encoding="utf8")
    for macro, dist in PINS.items():
        want = macros.get(macro)
        got = re.search(rf'"{re.escape(dist)}==([^"]+)"', pyproject)
        if not want:
            r.fail(f"preamble.tex has no \\{macro}")
        elif not got:
            r.fail(f"code/pyproject.toml does not pin {dist}")
        elif got.group(1) != want:
            r.fail(f"{dist}: preamble says {want}, pyproject says {got.group(1)}")
    pv = ROOT / "code" / ".python-version"
    if pv.is_file() and pv.read_text().strip() != macros.get("pypatch"):
        r.fail(f"code/.python-version says {pv.read_text().strip()}, "
               f"\\pypatch says {macros.get('pypatch')}")
    uv = macros.get("uvver")
    for wf in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
        for m in re.finditer(r'setup-uv@[^\n]*\n(?:[^\n]*\n){0,3}?\s*version:\s*"([^"]+)"',
                             wf.read_text(encoding="utf8")):
            if m.group(1) != uv:
                r.fail(f"{wf.name} installs uv {m.group(1)}, \\uvver is {uv}")
    r.note(f"{len(PINS)} pins compared, plus Python and uv")
    return r


LISTING_ENV = re.compile(r"\\begin\{(python|shellcmd|lstlisting|verbatim)\}.*?\\end\{\1\}", re.S)
MATH = re.compile(r"\$[^$]*\$|\\\[.*?\\\]|\\begin\{(equation|align|gather)\*?\}.*?\\end\{\1\*?\}", re.S)


def prose_words(src: str) -> int:
    s = strip(src)
    s = LISTING_ENV.sub(" ", s)
    s = MATH.sub(" x ", s)
    # Arguments that are paths, keys and labels are not prose.
    s = re.sub(r"\\(?:label|ref|index|pyfile|pyregion|transcript|plotfig|mermaidfig|"
               r"begin\{lab\})\{[^{}]*\}", " ", s)
    s = re.sub(r"\\[A-Za-z@]+\*?", " ", s)
    s = re.sub(r"[{}\[\]~\\]", " ", s)
    return len([w for w in s.split() if re.search(r"[A-Za-zÀ-ž]", w)])


def check_words() -> Result:
    r = Result("words")
    for c, _ in chapter_files():
        row = []
        for lang in LANGS:
            p = ROOT / "chapters" / lang / f"{c['file']}.tex"
            if not written(p):
                row.append(f"{lang}: stub")
                continue
            w = prose_words(p.read_text(encoding="utf8"))
            row.append(f"{lang}: {w}")
            if w > c.get("words", 3000):
                r.fail(f"{c['key']} {lang} has {w} words of prose, budget {c['words']}")
        r.note(f"{c['key']}  " + "  ".join(row))
    return r


def check_think() -> Result:
    """Every question is answered, and every answer has a question.

    A think box must be followed by \\reveal or a revealblock before the next
    think box, section or the end of the file; a reveal must have an open
    question to answer. That is the whole method made mechanical: a question
    left open is a reader told to stop and then given nothing to check, and
    an answer with no question is a reveal that spoils nothing it was meant
    to protect.
    """
    r = Result("think")
    total = 0
    tok = re.compile(r"\\begin\{think\}|\\reveal(?![A-Za-z])|\\begin\{revealblock\}|"
                     r"\\section\*?|\\chapter\*?")
    for p in all_sources():
        src = strip(p.read_text(encoding="utf8"))
        rel = p.relative_to(ROOT)
        open_q = None
        for m in tok.finditer(src):
            t = m.group(0)
            line = src.count("\n", 0, m.start()) + 1
            if t == "\\begin{think}":
                total += 1
                if open_q:
                    r.fail(f"{rel}:{open_q} question is never answered")
                open_q = line
            elif t in ("\\reveal", "\\begin{revealblock}"):
                if not open_q:
                    r.fail(f"{rel}:{line} an answer with no question before it")
                open_q = None
            else:
                if open_q:
                    r.fail(f"{rel}:{open_q} question is never answered before the next heading")
                open_q = None
        if open_q:
            r.fail(f"{rel}:{open_q} question is never answered")
    r.note(f"{total // 2 if total else 0} questions per edition (average of both)")
    return r


def check_skeleton() -> Result:
    r = Result("skeleton")
    for c, _ in chapter_files():
        for lang in LANGS:
            p = ROOT / "chapters" / lang / f"{c['file']}.tex"
            if not written(p):
                continue
            src = strip(p.read_text(encoding="utf8"))
            rel = p.relative_to(ROOT)
            outs = len(re.findall(r"\\outcome(?![A-Za-z])", src))
            if outs < 3:
                r.fail(f"{rel}: {outs} outcomes; a chapter declares at least three")
            order = []
            for name, pat in (("outcomes", r"\\begin\{outcomes\}"),
                              ("summary", r"\\begin\{summarybox\}"),
                              ("canyou", r"\\canyou(?![A-Za-z])"),
                              ("checkpoint", r"\\begin\{checkpoint\}")):
                m = re.search(pat, src)
                if not m:
                    r.fail(f"{rel}: no {name}")
                else:
                    order.append((m.start(), name))
            names = [n for _, n in sorted(order)]
            if len(names) == 4 and names != ["outcomes", "summary", "canyou", "checkpoint"]:
                r.fail(f"{rel}: the closing sequence is {names}; it must be "
                       f"outcomes ... summary, canyou, checkpoint")
            m = re.search(r"\\begin\{checkpoint\}(.*?)\\end\{checkpoint\}", src, re.S)
            if m:
                body = m.group(1)
                items = len(re.findall(r"\\item(?![A-Za-z])", body))
                answers = len(re.findall(r"\\answerto(?![A-Za-z])", body))
                if items < 4:
                    r.fail(f"{rel}: checkpoint has {items} questions; at least four")
                if items != answers:
                    r.fail(f"{rel}: checkpoint has {items} questions and {answers} answers")
            if not re.search(r"\\begin\{think\}", src):
                r.fail(f"{rel}: not one question is put to the reader")
    return r


def check_traps() -> Result:
    r = Result("traps")
    notes = ROOT / "notes" / "02-traps.md"
    if not notes.is_file():
        r.fail("notes/02-traps.md is missing")
        return r
    rows = re.findall(r"^\|\s*(\d+)\s*\|", notes.read_text(encoding="utf8"), re.M)
    nums = [int(x) for x in rows]
    dup = sorted({n for n in nums if nums.count(n) > 1})
    if dup:
        r.fail(f"notes/02-traps.md numbers {dup} more than once")
    for lang in LANGS:
        p = ROOT / "appendices" / lang / "appB-misreadings.tex"
        if not written(p):
            r.note(f"{lang}: Appendix B is a stub")
            continue
        src = strip(p.read_text(encoding="utf8"))
        printed = [int(a[0]) for a, _ in macro_args(src, "trapentry", 1)]
        for n in sorted(set(nums) - set(printed)):
            r.fail(f"{lang}: trap {n} is in the catalogue and not in Appendix B")
        for n in sorted(set(printed) - set(nums)):
            r.fail(f"{lang}: Appendix B prints trap {n}, which the catalogue lacks")
        dup = sorted({n for n in printed if printed.count(n) > 1})
        if dup:
            r.fail(f"{lang}: Appendix B prints {dup} more than once")
    r.note(f"{len(nums)} entries in the catalogue")
    return r


CHECKS = {
    "stubs": check_stubs, "listings": check_listings, "labs": check_labs,
    "transcripts": check_transcripts, "plots": check_plots, "lines": check_lines,
    "pins": check_pins, "words": check_words, "think": check_think,
    "skeleton": check_skeleton, "traps": check_traps,
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    for name in CHECKS:
        ap.add_argument(f"--{name}", action="store_true")
    ap.add_argument("--all", action="store_true",
                    help="every check except --stubs, which is a ledger")
    ap.add_argument("--soft", action="store_true", help="report and exit 0")
    ap.add_argument("--only", metavar="chNN",
                    help="keep only the failures that mention this chapter")
    a = ap.parse_args()
    chosen = [n for n in CHECKS if getattr(a, n)]
    if a.all:
        chosen = [n for n in CHECKS if n != "stubs"]
    if not chosen:
        ap.print_help()
        return 2
    ok = True
    for n in chosen:
        res = CHECKS[n]()
        if a.only:
            k = a.only
            res.fails = [f for f in res.fails
                         if k in f or ("l" + k[2:] + "_") in f]
            res.notes = [x for x in res.notes if k in x]
        ok &= res.show()
    return 0 if ok or a.soft else 1


if __name__ == "__main__":
    sys.exit(main())
