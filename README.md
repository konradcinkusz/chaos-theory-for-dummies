# Chaos from Zero

*How mathematics describes the world, and where it stops predicting it.*
Also in Polish: *Chaos od zera. Jak matematyka opisuje świat i gdzie przestaje
go przewidywać.*

The total eclipse of 12 August 2026 was in the astronomers' tables before
anyone who watched it was born; nobody could have said a month earlier
whether the sky would be clear. Both forecasts use the same kind of
mathematics. This book explains why one works for millennia and the other for
about a week — and why that difference, called **chaos**, is something
everyone who reads a forecast should understand.

It starts from school arithmetic. Every idea is built step by step, the reader
is asked questions before being told the answers, and **every number the book
prints that you could not work out in your head was computed by a short
Python program that the book prints and the build runs on every change.**

> **About the name.** The repository is called `chaos-theory-for-dummies`, but
> the book is titled *Chaos from Zero*. "For Dummies" is a registered trademark
> of John Wiley & Sons, and this book is not part of that series. The title is
> one line in each title page and main file if that ever needs to change.

## What is in it

| Part | Chapters |
|---|---|
| I — The clockwork: how mathematics describes the world | 1 Models · 2 Iteration · 3 Feedback · 4 Motion |
| II — Where prediction breaks | 5 The logistic map · 6 The butterfly effect, measured · 7 The Lyapunov exponent · 8 Bifurcations and Feigenbaum's constant |
| III — The shapes of chaos | 9 The Lorenz attractor · 10 Strange attractors · 11 Fractals · 12 Julia and Mandelbrot |
| IV — Chaos in the world | 13 Pendulums and planets · 14 Weather, climate and ensembles · 15 Telling chaos from chance · 16 Chaos inside the computer |
| V — Living with chaos | 17 Taming chaos · 18 Why you need chaos: a field guide to prediction |
| Appendices | A Answers · B Misreadings · C The mathematics you need · D Further reading · E Manifest |

Each chapter: a question put to the reader, learning outcomes, short sections
with *stop and think* questions answered directly below, listings that run,
labs (a starter that fails and a test that tells you when it passes), plots
drawn from the same code, a summary, a self-rating table and a checkpoint
answered in Appendix A.

## Reading it

Both editions are built and published on every push to `main`:

- **English:** [Chaos-from-Zero.pdf](https://konradcinkusz.github.io/chaos-theory-for-dummies/Chaos-from-Zero.pdf)
- **Polski:** [Chaos-od-zera.pdf](https://konradcinkusz.github.io/chaos-theory-for-dummies/Chaos-od-zera.pdf)
- The book's page: <https://konradcinkusz.github.io/chaos-theory-for-dummies/>

The links work once GitHub Pages is switched on for this repository, which
only a repository admin can do, once: **Settings → Pages → Build and
deployment → Source → GitHub Actions**. After that every push to `main`
republishes both PDFs, and the Pages workflow's summary says so if the switch
has not been made. Every tagged release (`v*`) also attaches both editions to
the release page, and every CI run on a pull request keeps the two PDFs as
downloadable artefacts for fourteen days. To build locally, see below.

## Running the laboratory

The code is one [uv](https://docs.astral.sh/uv/) project under `code/`,
locked to the versions on the title page:

```bash
cd code
uv sync
uv run python ch01/falling_stone.py      # a listing from Chapter 1
uv run pytest -k l01_01                  # the test of Chapter 1's first lab
```

`code/src/chaoslab/` is the book's small library of chaos — iteration,
steppers, the systems the book studies, the measurements and the fractals —
in pure Python with no dependencies, tested against known answers.

## Building the book

```bash
make              # numbers, plots, diagrams, both editions, then every gate
make en / pl      # one edition
make chapter CH=ch05          # one chapter alone, in _build/ch05-<lang>/
make code         # lint, run every listing, every lab solution, the library tests
make starters     # every lab starter must still FAIL its test
make numbers      # regenerate every computed value and printed output
make verify       # fail if any committed number no longer matches its script
make source       # the source-level gates: manifest, traps, parity, structure
```

A full build needs TeX Live (`latexmk` plus the `latex-extra`, `fonts-extra`,
`science`, `lang-polish` and `plain-generic` collections and `tex-gyre`),
Node with `@mermaid-js/mermaid-cli` for the diagrams, and uv.

## How it is kept honest

- **Two editions, one source.** English and Polish share one document body,
  one preamble and one list of chapters; `tools/parity.py` compares the two
  editions section by section, number by number and macro by macro, in order.
- **Every number is computed.** A value reaches the page as `\val{key}` from a
  file written by `code/measure/`; `make verify` fails when a script no longer
  produces what the book prints. Because chaos amplifies last-bit differences
  between machines, committed values from chaotic runs are computed with
  correctly rounded arithmetic or are robust summaries (see
  `notes/03-authoring-contract.md`).
- **Every listing runs.** CI runs every listing, every lab solution, and every
  lab starter (which must fail).
- **Structure is gated.** `tools/check_structure.py` checks that every
  question is answered, every checkpoint item has an answer, every lab has
  its three files, every plot is placed, and every code line fits the page.

## Repository layout

```
main-{en,pl}.tex, body.tex, preamble.tex, lang/{en,pl}.tex
structure*.tex               generated from tools/chapters.json
frontmatter/{en,pl}/         title page, how to use, introduction
chapters/{en,pl}/            the eighteen chapters
appendices/{en,pl}/          A-E (B is generated from notes/traps/)
code/                        the laboratory: listings, labs, measurements, plots, chaoslab
figures/mermaid/{en,pl}/     diagram sources; figures/values, figures/transcripts: computed
notes/                       the curriculum, the trap catalogue, the authoring contract
tools/                       the gates and generators
```

## Licence

The prose is [CC BY-NC-SA 4.0](LICENSE-CONTENT); the code is [MIT](LICENSE).
