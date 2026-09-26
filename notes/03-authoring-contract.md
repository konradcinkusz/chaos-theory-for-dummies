# The authoring contract

How a chapter of *Chaos from Zero* / *Chaos od zera* is written. Chapter 1
(`chapters/en/ch01-models.tex` and its Polish twin) is the exemplar: when
this file and Chapter 1 disagree, Chapter 1 is what was built and checked,
so read it first and copy its shapes.

Chapters were written in parallel by separate passes that could not see each
other. Everything below exists so that they could be: each pass owns a
disjoint set of files and checks its own chapter with its own build.

---

## 1. What you own, and what you must not touch

A pass writing chapter `chNN` owns exactly these, and nothing else:

| Path | What |
|---|---|
| `chapters/en/chNN-*.tex`, `chapters/pl/chNN-*.tex` | the two editions (replace the stub entirely) |
| `code/chNN/**` | the listings the chapter prints; `_name.py` for helpers |
| `code/labs/chNN/**` | the labs: starter, `solutions/`, tests, `__init__.py` |
| `code/measure/chNN.py` | every number the page prints |
| `code/plots/chNN.py` | every plot the page places |
| `figures/mermaid/{en,pl}/chNN-*.mmd` | diagrams, one source per language |
| `figures/values/chNN.tex`, `figures/transcripts/chNN-*.txt` | generated; never edit by hand |
| `notes/traps/chNN.json` | the chapter's misreadings, for Appendix B |

**Do not edit** `preamble.tex`, `lang/*`, `body.tex`, `main-*.tex`,
`structure*.tex`, `tools/*`, `Makefile`, `code/src/chaoslab/*`,
`code/pyproject.toml`, `code/uv.lock`, `code/tests/*`, any other chapter, or
any appendix. **Run no git command that writes** (no add, commit, stash,
checkout, reset, merge). Do not run `make clean`, `make numbers` or
`make all`: other chapters are being written at the same time and those
targets touch their files.

If `chaoslab` lacks something you need, write it in `code/chNN/` (a leading
underscore marks a helper that is imported rather than run). If you believe
a shared file is wrong, say so in your final report rather than editing it.

## 2. The skeleton, in this order

1. A `%%` header comment: what the chapter is, what it deliberately does not
   say (and which chapter does), and that the Polish file is its twin.
2. `\chapter{<title from tools/chapters.json>}` then `\label{ch:...}` (the
   label in the manifest) and one or two `\index{}`.
3. An opening of one to three paragraphs, the first starting `\noindent`,
   that puts a concrete question to the reader.
4. `\begin{outcomes} \outcome{...} ... \end{outcomes}` — three to six
   outcomes. An outcome names a skill; it never states a finding the chapter
   is about to elicit.
5. Sections, each `\section{...}\label{sec:chNN-<word>}`, first paragraph
   `\noindent`.
6. Inside the sections, at least:
   - **four `think` blocks**, each answered immediately by `\reveal{...}` or
     `\begin{revealblock}...\end{revealblock}` before the next `think` or
     heading. A question the reader can answer with what the book has
     already given them. Answer, then explain.
   - **one `trapbox`** or more: the misconception, set in the reader's own
     voice as a bold `\enquote{...}`, placed AFTER a `think` has let the
     reader walk into it. A trapbox that warns before the question is a
     spoiler, not a trap.
   - **one `worldbox`** (printed "Where you meet this"): a specific, real
     place the idea shows up — a named field, device or practice.
   - **two to five listings** from `code/chNN/`, with `\pyfile` or
     `\pyregion`, and their printed output with `\transcript{}`.
   - **one to three labs** (see §5).
   - **two to four figures** in total: at least one `\plotfig`, at most two
     `\mermaidfig`.
   - optional: `note`, `warning`, `rigourbox` (what is not proved here and
     where the proof lives), `projectbox` (a piece of `chaoslab`).
7. `\begin{summarybox} \begin{itemize} ... \end{itemize} \end{summarybox}`,
   one bullet per section, key terms in `\textbf{}`.
8. `\canyou` (generated from the outcomes; write nothing else).
9. `\begin{checkpoint} \item ... \answerto{...} ... \end{checkpoint}` — five
   to seven questions in the order the chapter taught them, each item
   followed by `\answerto{<the answer>}`, which is printed in Appendix A.

`python3 tools/check_structure.py --skeleton --think --only chNN` checks
this order and the counts.

## 3. Voice

- The reader is a curious adult who stopped doing mathematics at school.
  Assume arithmetic, fractions, percentages and reading a graph; **introduce
  every symbol before using it**, and say every formula in words too.
  "For dummies" is a promise about the reader's starting point, never about
  their intelligence.
- British English, second person, warm and exact. Short sentences where the
  idea is hard. No *simply*, *just*, *obviously*, *clearly*, *powerful*, no
  marketing register, no exclamation marks.
- Show, then name. Put the concrete case (a number, a run, a picture) before
  the general statement.
- **Prefer measurements to assertions.** A claim that code can check is
  checked by code in this chapter, and the page prints the result.
- **History only when you are sure.** Names, years and who-did-what must be
  well established (Lorenz 1963, May 1976, Feigenbaum 1978, Mandelbrot 1980,
  Poincaré 1890, Hénon 1976, Ott–Grebogi–Yorke 1990, Pecora–Carroll 1990,
  Li–Yorke 1975 are safe). Never invent a quotation; paraphrase instead. If
  a detail is uncertain, leave it out rather than hedging it.
- The book's argument (see `tools/chapters.json`, `parts` and every brief):
  mathematics describes the world astonishingly well (Part I); even an exact
  rule can make long-range prediction impossible, and that limit is
  measurable (Part II); chaos has structure and shape (Part III); it is in
  real systems (Part IV); and knowing it changes what you should believe and
  do (Part V). Your chapter carries its part of that argument and does not
  spend another chapter's payoff.

## 4. Numbers, and why this book's numbers must not move

**Every number a reader cannot do in their head comes from
`code/measure/chNN.py`** and reaches the page as `\val{chNN.key}`. Arithmetic
the reader is meant to do (`3 \times 3 = 9`) is written inline.

```python
from _values import Values
v = Values("chNN")
v.num("key", 34)               # integer: no format
v.num("rate", 0.69314, ".3f")  # float: format required
v.text("name", "x86_64")       # text, TeX-escaped
v.write()
```

The measurement script imports the SAME functions the listings print (put
`code/chNN` on `sys.path` as `code/measure/ch01.py` does), so the page and
the listing cannot disagree. Assert the property you are about to claim
(`assert steps < 50`), so a changed number fails loudly rather than
silently changing the sentence around it.

Every emitted value must be used by the page, in BOTH editions, and every
`\val{}` must be emitted (parity C7).

**Determinism is a hard requirement, and chaos makes it hard.** `make
verify` re-runs every measurement on every CI build and fails if a single
character of `figures/values/` or `figures/transcripts/` changes. Python
floats computed with `+ - * /` and `math.sqrt` are correctly rounded and
identical on every machine. `math.sin`, `cos`, `exp`, `log`, `atan2` and
non-integer `**` come from the platform maths library and may differ in the
last bit between machines — and a chaotic system amplifies the last bit
until the whole trajectory differs. So:

- a value taken from a chaotic trajectory after more than a few dozen steps
  must be computed with `+ - * /` and `sqrt` only (logistic, tent, Hénon,
  Lorenz, Lorenz-96 all qualify), **or**
- be a robust summary: a long-run average, a Lyapunov exponent to two
  decimals, a count, a fraction rounded to two figures — something the last
  bit cannot move;
- a `log` applied at the END of a computation (to a number that is already
  determined) is fine; a `log` or `sin` inside a chaotic loop is not, unless
  the committed value is robust as above.

Transcripts obey the same rule. Plots are not gated and may use anything.

**Keep every script fast**: a listing under five seconds, a measurement or
plot script under thirty. Pure-Python loops of a few hundred thousand steps
are fine. `numpy` is available and fine in `measure/` and `plots/`; in a
listing prefer plain Python (or `chaoslab`) so the reader sees the
arithmetic, except where the chapter is about many points at once.

## 5. Code conventions

- **Listings** live in `code/chNN/` and are run by CI as
  `uv run python chNN/file.py` from `code/`: exit 0, **nothing on stderr**.
  `from chaoslab import ...` works (the package is installed); sibling
  modules import by bare name. **79 columns maximum** everywhere under
  `code/`, ASCII only in `.py` files, `ruff` clean.
- **Regions**: `# --8<-- [start:name]` ... `# --8<-- [end:name]` and
  `\pyregion{chNN/file.py}{name}{caption}{lst:chNN-name}` print just that
  part with the file's own line numbers. `\pyfile{chNN/file.py}{caption}{lst:...}`
  prints the whole file. Paths are relative to `code/`.
- **Transcripts**: put `# transcript: chNN-name` in the first 25 lines of a
  listing; its stdout becomes `figures/transcripts/chNN-name.txt` and
  `\transcript{chNN-name}` prints it. Output ≤ 79 columns, ASCII, no memory
  addresses, deterministic. Print few lines (≤ 20) and round what you print.
- **Labs** — a lab is three files and the starter must FAIL:
  - key `lNN_KK_word`, where `KK` is the lab's position in the chapter
    (the first lab printed is `_01_`);
  - `code/labs/chNN/<key>.py`: the starter, whose functions have docstrings
    and bodies of `raise NotImplementedError("your turn: replace this line")`;
  - `code/labs/chNN/solutions/<key>.py`: the reference solution;
  - `code/labs/chNN/test_<key>.py`: tests using
    `from labs._loader import load` then `lab = load("chNN", "<key>")`;
  - `code/labs/chNN/__init__.py` (empty docstring file);
  - every test must depend on the reader's answer (a test the untouched
    starter passes breaks the build);
  - on the page: `\begin{lab}{<key>}{<title>} <what to do> \end{lab}`.
- **Plots**: `code/plots/chNN.py`, modelled on `code/plots/ch01.py`:
  `@plot("chNN-name")` functions taking `lang`, labels through
  `T(lang, en, pl)`, `new(height=...)` for the figure, `main()` at the end.
  Polish decimal commas are applied automatically. Place with
  `\plotfig{chNN-name}{caption}{manifest copy}`. Manifest copy is a short
  noun phrase (under 45 characters); the caption is one or two sentences
  that say what to look at.
- **Diagrams**: `figures/mermaid/{en,pl}/chNN-name.mmd`. `flowchart LR`,
  three nodes, labels of two short lines (`"TITLE<br/>four or five words"`),
  at most one dashed edge. Polish diacritics are fine. Measure the render
  with `pdfinfo figures/diagrams/en/chNN-name.pdf`: **the width must be
  between about 420 and 620 pt**; wider sets the text too small, narrower
  too large. No computed numbers in a diagram. Place with
  `\mermaidfig{chNN-name}{caption}{manifest copy}`.
- **Rule 2**: a figure, listing or transcript may not show the answer to a
  `think` that comes before its `\reveal`. Place figures after the reveal
  they illustrate.

## 6. LaTeX conventions

- `\code{}` for code in prose, `\api{}` for a function name, `\pkg{}` for a
  package; write `\_` for an underscore inside them.
- `\enquote{...}` for quotation marks (both editions; straight quotes in
  Polish prose fail parity). `\dash{}` for a spaced dash.
- Decimals in prose or maths are `\num{0.5}` or `\val{}` — **a bare decimal
  like `0.5` fails parity in both editions** (the Polish edition owes a
  comma). Integers may be bare. Write `$r = \num{3.2}$`.
- `\ln` for the natural logarithm; never a bare `\log` (it is refused).
- Cross-reference other chapters as `Chapter~\ref{ch:lorenz}` (labels in
  `tools/chapters.json`). Never reference another chapter's section, figure
  or listing: it may not exist yet. Parts are `Part~II` etc.
- `\index{term}` and `\index{term!subterm}`; in Polish, Polish terms.
- `\[ ... \]` for displayed maths. `\tfrac` inline. No `\dfrac` inline.
- Avoid long `\code{}` runs mid-sentence (they cannot hyphenate and cause
  overfull lines); start a sentence with them or put them in a listing.

## 7. The two editions

The Polish edition is a twin, not a paraphrase: the same sections in the
same order, the same boxes, labels, listings, figures, labs, `\val{}`s,
maths spans and numerals **in the same order**. `tools/parity.py` compares
them token by token. What the translator must carry:

- a digit stays a digit and a word stays a word (English `three` → Polish
  `trzy`, English `$3$` → Polish `$3$`);
- a sentence with two maths spans or a number and a reference keeps them in
  the same order — rebuild the Polish sentence rather than swap them;
- listing comments stay English (they are shared code);
- idiomatic Polish with full diacritics; established Polish terms: *atraktor
  dziwny*, *wykładnik Lapunowa*, *bifurkacja podwojenia okresu*, *efekt
  motyla*, *odwzorowanie logistyczne*, *przestrzeń fazowa*, *fraktal*,
  *zbiór Mandelbrota*, *prognoza zespołowa*, *wrażliwość na warunki
  początkowe*.

## 8. Misreadings for Appendix B

Write `notes/traps/chNN.json`, one entry per `trapbox` (and optionally other
misreadings the chapter corrects). Chapter N numbers its entries
`10*N + 1` upwards (Chapter 5: 51, 52, ...). Each entry:

```json
[
  {"n": 51, "label": "sec:ch05-logistic",
   "en": {"habit": "A simple rule gives simple behaviour.",
          "truth": "One line of algebra ... (one or two sentences, LaTeX allowed)"},
   "pl": {"habit": "Prosta reguła daje proste zachowanie.",
          "truth": "..."}}
]
```

`label` is the section where the trap is elicited. The habit is in the
reader's voice; the truth is one or two sentences.

## 9. The verification loop

```bash
export PATH=/tmp/claude-0/shim:$PATH         # the uv shim (TLS settings)
cd /home/user/chaos-theory-for-dummies/code
uv run ruff check chNN labs/chNN measure/chNN.py plots/chNN.py
CHAOS_SOLUTIONS=1 uv run pytest tests/test_listings.py labs/chNN -q -k "chNN or lNN_"
CHAOS_STARTERS=fail uv run pytest labs/chNN -q
cd ..
python3 tools/build_chapter.py chNN       # measure, transcripts, plots, diagrams, both PDFs
python3 tools/parity.py --only chNN
python3 tools/check_structure.py --all --only chNN
```

`build_chapter.py` must report, for both editions, 0 errors, no overfull box
over 15 pt, no overfull vbox, no unresolved reference of your own. Then
**look at the pages**: `pdftoppm -r 50 -png _build/chNN-en/main.pdf
/tmp/claude-0/chNN-en` and read a few of the PNGs — figures placed near
their text, no box stranded, the lab boxes and the checkpoint intact.

Prose budget: 3,500 words per edition (`check_structure.py --words --only
chNN`); aim for 2,800–3,400 in English. Listings and labs do not count.

## 10. What to report when you finish

In under 250 words: the files you created; words per edition; values,
listings, labs and figures; anything in the brief that turned out to be
wrong once the code ran (and what you did instead); anything you believe is
wrong in a shared file (without editing it); and any claim you make that
depends on another chapter delivering something.
