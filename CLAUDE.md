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

| | Done | Remaining |
|---|---|---|
| Structure | `body.tex` read by both main files, shared preamble, generated `structure*.tex`, Makefile, CI, parity and structure gates, Mermaid and plot pipelines, lab mechanism | — |
| Front matter | Title page, copyright, *How to use this book*, Introduction — **both editions** | — |
| Chapters | **All 18 written, both editions** | — |
| Appendices | **All 5 written.** A and B generated; C, D, E written; E's ledger computed by `code/measure/ledgers.py` | — |
| Code | `code/` is a locked uv project: every chapter's listings and labs, `chaoslab` with known-answer tests, a measurement script and a plot script per chapter, and CI runs all of it | — |

**Two editions, one paper size**: A4 at 12pt, one-sided, read on a screen.
Measured on TeX Live 2023 (Debian) with `newtx`, `inconsolata`, `tex-gyre`
and `lmodern` installed. CI compiles on a newer full TeX Live, so its page
counts may differ by a page or two; the zeros are what must agree:

| | Pages | Errors | Unresolved | Overfull hbox | Overfull vbox |
|---|---|---|---|---|---|
| `main-en` | 269 | 0 | 0 | 0 | 0 |
| `main-pl` | 279 | 0 | 0 | 0 | 0 |

`reflist.py`: 313 labels in each edition, 0 mismatches. Appendix E prints
the book's own ledgers (listings, labs, tests, questions, values, the
`verifybox` count) from the tree, so they are not repeated here: a second
copy of a count is the next thing to go stale.

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
- **The Polish decimal comma must be braced.** `\ifpl{,}{.}` hands siunitx a
  bare comma, which maths mode sets as punctuation with a space after it:
  "9, 81". The marker is `\ifpl{{,}}{.}`.
- **A region marker starts at column 0.** An indented `# --8<-- [end:x]` is
  dropped by listings but its indentation is not, so the listing ends on an
  empty numbered line. A comment's column is free in Python and ruff does not
  mind.
- **Room before a listing is `\Needspace`, not `\needspace`.** The capital
  form measures the space left exactly; the lower-case one works through glue
  and turned pages early. `\listingpath` asks for six lines, so a path is
  never stranded at the foot of a page with its listing overleaf.
- **A box may not break straight after its title**: both box styles carry
  `lines before break=4`.
- **A generator takes argparse or nothing.** `gen_traps.py` once treated any
  argument other than `--check`, `--help` included, as write mode.
- Inherited and handled in the preamble: `amssymb` beside `newtxmath`,
  `\IfFileExists` branches needing `##1`, `babel` with a missing language,
  `upquote`, the `--` ligature in typewriter type (disabled for `tt*`), and
  `\phantomsection` before `\addcontentsline`.

---

## Resolved questions

### The first pass, September 2026 --- the whole book, written in parallel

**Chapter 1 was written first and alone, as the exemplar**, into a scaffold
that already had every gate; chapters 2 to 18 were then written at the same
time by separate passes that could not see each other, each against its brief
in `tools/chapters.json` and against `notes/03-authoring-contract.md`, which
was written for exactly that situation. The front matter and the appendices
were written by the integrating pass.

**Both sibling books paid for parallel passes in merges**, one per overtaking,
because every pass appended to the same shared files. This book was laid out
so that a chapter pass writes only files it owns: its two chapter files, its
`code/chNN/`, `code/labs/chNN/`, `code/measure/chNN.py`, `code/plots/chNN.py`,
its diagrams, its value and transcript files, and **its own trap file,
`notes/traps/chNN.json`**. Nothing a chapter pass writes is written by any
other, so the whole book merged with no conflicts at all. The two files that
are genuinely shared --- Appendix B and `notes/02-traps.md` --- are
*generated* from the per-chapter trap files by `tools/gen_traps.py`, and only
the integrator runs it.

**The trap numbering cannot collide, by construction.** The Python book's
catalogue collided three times because each pass took "the next free number"
from a maximum that was stale on its branch. Here Chapter N numbers its
entries from `10N + 1`, and `gen_traps.py` refuses an entry outside its
chapter's block. It is the Python book's final fix applied before the first
chapter rather than after the third collision.

#### The determinism rule, which neither sibling book needed

A chaotic run amplifies the last-bit differences between two machines'
`sin`, `exp` and `log` (which are not correctly rounded, and differ between
libm implementations) into a different trajectory within a few dozen steps.
So a committed value taken from a chaotic run uses only `+ - * /` and `sqrt`,
which IEEE 754 rounds correctly everywhere, or it is a robust summary: an
average over a long run, an exponent to two decimals, a count. Several
chapter passes went further and **tested their values for robustness** ---
Chapter 13 nudged every start by 10^-12 rad, changed the step size and added
random one-ulp noise to `sin` and `cos`, and every committed value survived.
That is the right test, and it is worth copying: the rule says what not to
do, and the perturbation says whether you did it.

#### Build traps met in this pass

Recorded in *Build traps* above, with the fixes; the list here is what was
learnt from them.

- **A diagram render is clamped to mmdc's viewport**, so every wide diagram
  came out exactly 600 pt and its text shrank to fit. The natural width was
  unmeasurable until `-w 1600` was passed.
- **The Polish decimal comma printed as "9, 81".** `\ifpl{,}{.}` strips the
  argument's braces, so siunitx received a bare comma, which in maths mode is
  punctuation and gets a thin space after it. `\ifpl{{,}}{.}` keeps it an
  ordinary symbol. Visible only on the page, in one edition, and in every
  decimal that edition prints.
- **A listing's path could be stranded at the foot of a page** with the
  listing overleaf. `\listingpath` now asks for six lines with `\needspace`.
- **An indented `# --8<-- [end:x]` marker ends the listing on an empty
  numbered line**: listings drops the marker text and keeps the indentation.
  Every region marker under `code/` starts at column 0, which Python allows
  for a comment anywhere and ruff does not flag.
- **A breakable box could break straight after its title**, leaving a think
  question's heading at the foot of one page and its question on the next.
  Both box styles now carry `lines before break=4`.
- **`tools/gen_traps.py --help` regenerated the shared files**, because its
  only argument test was `"--check" in sys.argv`, so anything else meant
  write mode. It uses argparse now and refuses an unknown argument.
- **A single-chapter Polish build printed "Answers"**; `build_chapter.py`
  localises the heading.

#### Overlap between chapters written at the same time

Two passes written in parallel will each introduce what they both need.
Chapter 2 and Chapter 3 both introduced the slope, used different arrows for
a rule, and Chapter 2's text printed the answer to Chapter 3's first lab. The
owner is the earlier chapter: Chapter 3 was rewritten to refer back to
Chapter 2's slope, to use `\mapsto` throughout, and to replace its first lab.
**The contract's ownership table is what made this decidable**, and a brief
that says "introduce X" in two chapters is the thing to look for first when
the next chapter is revised.

#### Where the chapters departed from their briefs, and why

Each departure was made because the brief would have printed something the
pass could not verify or that was not true as stated:

- Chapter 8 finds Feigenbaum's delta from the *superstable* parameters (where
  the orbit passes through the top of the map), by bisection with `+ - * /`
  only, because split points found by watching an orbit settle come out
  early, and says why in the chapter.
- Chapter 12 computes the Mandelbrot bulb centres itself and checks each
  against the logistic map rather than reading Chapter 8's values; the gap
  ratio comes out at 4.669 and the Feigenbaum point at c = -1.401. The area
  of the set is given as grid estimates, because it is not known exactly;
  why 2 is the escape radius is a sketch in a rigour box.
- Chapter 11 measured the Hénon attractor's box-counting dimension at 1.23
  with a million points, and lower with fewer, against the published figure
  of about 1.26. The chapter quotes the published value, prints its own and
  says why a finite cloud of points reads low, rather than tuning the
  measurement until it agreed.
- Chapter 13 hedged "the release angle grows chaotic with energy" to "higher
  up", which is what the measurements support, and says that conserved energy
  does not prove a computed path right: the same release at two step sizes
  parts after about fifteen seconds.
- Chapter 3 reads "continuous growth stepped finely" as one law paid in ten
  instalments, which keeps Euler's method for Chapter 4.

**No history was written from memory that could not be checked.** Where a
pass was unsure of a date (Shishikura's result, in Chapter 12) it left the
date out rather than guessing.

