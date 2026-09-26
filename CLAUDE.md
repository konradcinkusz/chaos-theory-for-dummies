# CLAUDE.md — working on this book

Context for continuing *Chaos from Zero* / *Chaos od zera*. Read this before
touching a chapter, and read `notes/03-authoring-contract.md` before writing
one.

This repository is the third book built on the same machinery as
[math-for-ai-engineers](https://github.com/konradcinkusz/math-for-ai-engineers)
(the bilingual single-source wiring, the parity gates, computed values, the
programmed-learning method) and
[python-for-csharp-developers](https://github.com/konradcinkusz/python-for-csharp-developers)
(every listing a file that CI runs, exercises whose starter must fail). Where
a rule below says *inherited*, the reasoning that earned it is in those
repositories' `CLAUDE.md`, and it is not repeated here.

---

## Status

<!-- STATUS-TABLE -->

**Re-measure every row from the build in front of you** after any change,
and say which TeX installation you measured on (inherited: a bare TeX Live
and a full one paginate differently).

---

## Non-negotiable conventions

**Every number is computed, not remembered** (inherited). A number the reader
cannot do in their head is written by a script under `code/measure/` to
`figures/values/<name>.tex` as `\pyval{key}{value}` and reaches the page as
`\val{key}`. Both `figures/values/` and `figures/transcripts/` are committed,
and `make verify` fails when a script no longer produces what the book
prints. Arithmetic the reader is meant to do is written inline.

**And chaos makes that rule harder than in either sibling book.** A chaotic
system amplifies a last-bit difference between two machines' maths libraries
(`sin`, `exp`, `log` are not correctly rounded, and differ between platforms)
into a completely different trajectory within a few dozen steps. So a value
taken from a chaotic run is computed with `+ - * /` and `sqrt` only — which
IEEE 754 rounds correctly on every machine — or it is a robust summary: an
average over a long run, an exponent to two decimals, a count. A `log` at the
end of a computation is fine; a `log` or `sin` inside a chaotic loop is not,
unless what is committed is robust. Plots are not gated and may use anything.
The contract's §4 carries the rule and Chapter 16 makes it the subject.

**Every listing runs** (inherited from the Python book). Every listing is a
file under `code/chNN/`, printed with `\pyfile{}` or `\pyregion{}`, and
`code/tests/test_listings.py` runs each as a subprocess from `code/`: exit 0,
nothing on stderr. A listing's stdout becomes a committed transcript when it
carries `# transcript: chNN-name` in its first 25 lines.

**A lab is three files and the starter must fail** (inherited). Starter
`code/labs/chNN/<key>.py`, solution `solutions/<key>.py`, test
`test_<key>.py`; `CHAOS_SOLUTIONS=1` runs the solutions, `CHAOS_STARTERS=fail`
marks every lab test a strict expected failure, so a starter that passes is a
build failure. The key's second field is its position in the chapter.

**The method** (inherited from the mathematics book, lightened). Every
chapter has outcomes, `think` questions each answered at once by `\reveal`,
trap boxes that name a misconception only after a question has let the reader
walk into it, a summary, `\canyou` generated from the outcomes, and a
checkpoint whose every item carries `\answerto{}` for Appendix A.
`check_structure.py --think --skeleton` enforces the shape.

**Two editions, one source** (inherited). `body.tex` is read by both main
files; `lang/{en,pl}.tex` hold every user-visible string; `parity.py`
compares the two editions token by token, number by number and macro by
macro, **in order**. A digit stays a digit and a word stays a word.

**79 columns** under `code/`, ASCII only in listings, `ruff` clean.

**Voice.** British English and idiomatic Polish, second person, warm and
exact. No *simply*, *just*, *obviously*, *powerful*. The reader stopped doing
mathematics at school: every symbol is introduced before it is used and every
formula is said in words. History only when it is certain; never an invented
quotation.

**The title.** The repository is `chaos-theory-for-dummies`; the book is
*Chaos from Zero*, because "For Dummies" is a Wiley trademark. The title is
one line in each title page, copyright page and main file.

---

## Two editions, one source

```
main-{en,pl}.tex       \documentclass[12pt,oneside,openany]{book}, \booklang, the PDF title
body.tex               THE document body. One copy, read by both.
preamble.tex           all machinery, and the pinned versions
lang/{en,pl}.tex       every user-visible string; C3 fails if the macro sets differ
structure*.tex         GENERATED chapter and appendix sequence, from tools/chapters.json
frontmatter/{en,pl}/   title page, copyright, how to use, introduction
chapters/{en,pl}/      the only place prose is duplicated
appendices/{en,pl}/    A (answers, generated), B (misreadings, generated), C, D, E
```

The gates, all reading the source and needing no PDF:

| Tool | Checks |
|---|---|
| `tools/gen_stubs.py --check` | the manifest, the stubs and the two structure files agree |
| `tools/gen_traps.py --check` | Appendix B and `notes/02-traps.md` are what `notes/traps/*.json` generate |
| `tools/parity.py` | C1 files, C3 lang catalogue, C4 ordered structure, C5 labels, C7 values, C9 diagrams and plots, C10 notation (bare decimals in maths AND prose, bare `\log`), C11 labs, C12 numeric literals in order, C13 ASCII listings, C14 macro histogram, C15 wiring. `--only chNN` filters to one chapter |
| `tools/check_structure.py --all` | listings, labs, transcripts, plots placed and produced, 79 columns, pins, word budgets, every question answered, the chapter skeleton, the trap catalogue. `--only chNN` filters |
| `tools/checklog.py` | the build log, properly (inherited: not `grep '^!'`) |
| `tools/reflist.py` | the same label resolves to the same number in both editions |

---

## Structure

Five parts, eighteen chapters, five appendices; the briefs are in
`tools/chapters.json` and the reasoning in `notes/01-curriculum.md`.

| Part | Chapters |
|---|---|
| I — The clockwork | 1 Models · 2 Iteration · 3 Feedback · 4 Motion |
| II — Where prediction breaks | 5 Logistic map · 6 Butterfly effect · 7 Lyapunov exponent · 8 Bifurcations |
| III — The shapes of chaos | 9 Lorenz · 10 Strange attractors · 11 Fractals · 12 Mandelbrot |
| IV — Chaos in the world | 13 Mechanics · 14 Weather · 15 Chaos or noise · 16 Computers |
| V — Living with chaos | 17 Taming chaos · 18 Why you need chaos |

The companion library `code/src/chaoslab/` is pure Python with no
dependencies and a known-answer test for every function
(`code/tests/test_chaoslab.py`).

---

## Build

```bash
make              # source gates, numbers, plots, diagrams, both editions, check
make en / pl      # one edition
make chapter CH=chNN [LANG=en]   # one chapter alone, in _build/chNN-<lang>/
make code         # uv sync --locked, ruff, every listing, every lab solution, the library
make starters     # every lab starter must FAIL
make numbers      # regenerate figures/values and figures/transcripts
make verify       # fail on drift or on a never-committed computed file
make plots        # draw every plot in both editions (build output, gitignored)
make diagrams     # render every .mmd (needs mmdc and Chromium)
make traps        # regenerate Appendix B and notes/02-traps.md
make source       # the source gates, in seconds
```

**Run the source gates before a build, not inside it** (inherited).

CI (`.github/workflows/build.yml`): `code` (ruff, pytest with the solutions,
the starters, every measurement with a drift check, every plot), `parity`
(every source gate) and `diagrams` run side by side; `build` compiles both
editions on a full TeX Live and needs all three; `crossrefs` compares the
two `.aux` trees. `pages.yml` publishes both PDFs with `docs/index.html` on
every push to `main` (a repository admin must first set Settings -> Pages ->
Source to *GitHub Actions*, once); `release.yml` attaches both to a `v*` tag.

### Build traps already hit and fixed

- **A Mermaid render wider than the viewport is scaled down to fit it.** mmdc
  defaults to an 800-pixel page, so every diagram wider than 600 pt came out
  exactly 600 pt wide and its text shrank with it, which makes the natural
  width unmeasurable. The Makefile and every workflow pass `-w 1600`; measure
  with `pdfinfo` and aim for 420–620 pt (at this geometry node text then sets
  at 8–11 pt).
- **A licence name is not a decimal.** `CC BY-NC-SA 4.0` in prose trips the
  prose-decimal check, correctly by its own rule. It is the macro
  `\proselicence`, the same in both editions.
- **A layout length is not a decimal either.** `0.9\linewidth` in a
  `tabularx` argument was flagged as a bare decimal; parity now skips a
  decimal followed by a TeX length.
- **The uv shim.** In this sandbox `UV_NATIVE_TLS` is set to an empty string,
  which uv 0.12 rejects; a wrapper at `/tmp/claude-0/shim/uv` unsets it and
  sets `UV_SYSTEM_CERTS=1`. Not a repository file; recreate it if needed.
- **A description list with a long bold label overflows.** Appendix D's
  author lists are set `before=\raggedright`.
- Inherited and handled in the preamble: `amssymb` beside `newtxmath`,
  `\IfFileExists` branches needing `##1`, `babel` with a missing language,
  `upquote`, the `--` ligature in typewriter type (disabled for `tt*`), and
  `\phantomsection` before `\addcontentsline`.

---

## Resolved questions

<!-- PASS-NOTES -->
