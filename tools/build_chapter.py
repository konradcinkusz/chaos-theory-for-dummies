#!/usr/bin/env python3
"""Build ONE chapter, in its own directory, with everything it needs.

    python3 tools/build_chapter.py ch05            # both editions
    python3 tools/build_chapter.py ch05 pl         # one

For writing a chapter without building the book. It runs the chapter's own
measurement script and transcripts, draws its plots, renders its diagrams,
and compiles the chapter alone into _build/<chNN>-<lang>/, followed by its
answers and its manifests -- so two chapters can be written at the same time
without their builds touching each other's files.

Cross-references to OTHER chapters are seeded with their numbers from the
manifest, so "Chapter 9" prints as it will in the book; a reference to a
section of another chapter prints ?? here and resolves in the full build.

Exit 0 when the chapter compiled cleanly by the same standard as the book
(tools/checklog.py), except for references into other chapters.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CODE = ROOT / "code"


def run(cmd: list[str], cwd: Path, quiet: bool = False) -> int:
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if p.returncode != 0 or not quiet:
        sys.stdout.write(p.stdout[-4000:])
        sys.stderr.write(p.stderr[-4000:])
    return p.returncode


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    key = sys.argv[1]
    langs = sys.argv[2:] or ["en", "pl"]
    m = json.loads((ROOT / "tools" / "chapters.json").read_text(encoding="utf8"))
    chap = next((c for c in m["chapters"] if c["key"] == key), None)
    if chap is None:
        print(f"no chapter {key!r} in tools/chapters.json")
        return 2
    num = int(chap["id"])
    uv = os.environ.get("UV", "uv")

    # 1. The chapter's numbers, transcripts and plots -- its own only.
    script = CODE / "measure" / f"{key}.py"
    if script.is_file():
        print(f"== measure/{script.name}")
        if run([uv, "run", "python", f"measure/{script.name}"], CODE):
            return 1
    print(f"== transcripts for {key}")
    if run([uv, "run", "python", "measure/transcripts.py", key], CODE):
        return 1
    plots = CODE / "plots" / f"{key}.py"
    if plots.is_file():
        print(f"== plots/{plots.name}")
        if run([uv, "run", "python", f"plots/{plots.name}"], CODE):
            return 1

    # 2. Its diagrams, if a renderer is available.
    mmdc = shutil.which("mmdc")
    for lang in langs:
        for src in sorted((ROOT / "figures" / "mermaid" / lang).glob(f"{key}-*.mmd")):
            out = ROOT / "figures" / "diagrams" / lang / f"{src.stem}.pdf"
            if out.is_file() and out.stat().st_mtime >= src.stat().st_mtime:
                continue
            if not mmdc:
                print(f"  (no mmdc: {src.name} not rendered)")
                continue
            out.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["make", "-s", f"figures/diagrams/{lang}/{src.stem}.pdf"],
                           cwd=ROOT)

    ok = True
    for lang in langs:
        build = ROOT / "_build" / f"{key}-{lang}"
        build.mkdir(parents=True, exist_ok=True)
        # A private index of every value file there is, so this build does
        # not depend on -- or rewrite -- figures/values/all.tex.
        vals = sorted((ROOT / "figures" / "values").glob("*.tex"))
        (build / "values.tex").write_text("".join(
            f"\\input{{figures/values/{v.stem}}}\n"
            for v in vals if v.stem != "all"), encoding="utf8")
        seeds = []
        for c in m["chapters"]:
            if c["key"] == key:
                continue
            title = c[lang].replace("\\", "")
            seeds.append(f"\\newlabel{{{c['label']}}}{{{{{c['id']}}}{{1}}"
                         f"{{{title}}}{{chapter.{c['id']}}}{{}}}}")
        main = f"""\\documentclass[12pt,oneside,openany]{{book}}
\\def\\booklang{{{lang}}}
\\def\\valuesindex{{_build/{key}-{lang}/values}}
\\input{{preamble}}
\\makeatletter
{chr(10).join(seeds)}
\\makeatother
\\begin{{document}}
\\mainmatter
\\setcounter{{chapter}}{{{num - 1}}}
\\input{{chapters/{lang}/{chap['file']}}}
\\appendix
\\chapter{{{'Odpowiedzi' if lang == 'pl' else 'Answers'}}}
\\answersbody
\\listoflabs
\\listofplots
\\listofdiagrams
\\end{{document}}
"""
        (build / "main.tex").write_text(main, encoding="utf8")
        print(f"== compile {key} ({lang})")
        rc = run(["latexmk", "-pdf", "-interaction=nonstopmode", "-file-line-error",
                  f"-outdir={build.relative_to(ROOT)}",
                  str((build / "main.tex").relative_to(ROOT))], ROOT, quiet=True)
        log = build / "main.log"
        if not log.is_file():
            print("  no log was written")
            ok = False
            continue
        text = log.read_text(encoding="utf8", errors="replace")
        # References into sections of OTHER chapters cannot resolve here.
        own = re.findall(r"\\label\{([^}]*)\}",
                         (ROOT / "chapters" / lang / f"{chap['file']}.tex")
                         .read_text(encoding="utf8"))
        undef = set(re.findall(r"Reference `([^']+)' on page \d+ undefined", text))
        foreign = {u for u in undef if u not in own}
        mine = undef - foreign
        p = subprocess.run([sys.executable, str(ROOT / "tools" / "checklog.py"), str(log)],
                           capture_output=True, text=True)
        report = p.stdout
        if foreign and not mine:
            report = report.replace("UNRESOLVED REFS", "refs to other chapters (ok here)")
        print(report)
        bad = ("ERRORS" in report or "OVER 15" in report or "OVERFULL VBOX" in report
               or "NON-CONVERGENCE" in report or "PAGE DEFECT" in report or mine
               or "NO COMPUTED VALUES" in report)
        if rc and not bad:
            print(f"  latexmk exited {rc}; read {log.relative_to(ROOT)}")
        if bad:
            ok = False
        print(f"  PDF: {(build / 'main.pdf').relative_to(ROOT)}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
