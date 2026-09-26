# The curriculum, and why it is in this order

The briefs themselves live in `tools/chapters.json`, one per chapter, and
print in each stub until the chapter is written. This file carries only the
reasoning that sits between them: the arc, the order, and the rules that
keep eighteen chapters from spending each other's payoffs. It deliberately
does not repeat the briefs — a second copy of a brief is the next thing to
go stale.

## 1. The reader and the promise

The reader stopped doing mathematics at school and is curious about what
people mean by chaos. The book assumes arithmetic, fractions, percentages
and reading a graph, and nothing else. Every symbol is introduced before it
is used and every formula is said in words.

The promise is two-sided, and the order of the parts follows it:

1. **Mathematics describes the world astonishingly well** (Part I). A model
   is a machine for predicting; a rule stepped forward in time is how almost
   every model works; feedback is why nothing grows for ever; motion is a
   rule of change drawn as arrows over a map of every state.
2. **Even an exact rule can make long-range prediction impossible, and the
   limit is measurable** (Part II). The logistic map shows every kind of
   behaviour; the butterfly effect is measured rather than told; the
   Lyapunov exponent turns it into one number and a horizon; the
   period-doubling road ends in a constant nobody put there.
3. **Chaos has shape** (Part III): the Lorenz attractor, stretch-and-fold,
   fractals and their dimension, and the Mandelbrot set, which turns out to
   contain Part II's road.
4. **Chaos is in the world** (Part IV): mechanics and the solar system,
   weather and climate, living systems and markets (with the honest caveat
   that irregular is not the same as chaotic), and the computer itself.
5. **Knowing it changes what you believe and do** (Part V): chaos can be
   steered with tiny nudges, and the book ends with a field guide to judging
   any prediction.

The introduction states the argument for learning chaos at all; Chapter 18
returns to it as a checklist the reader can use on any forecast.

## 2. The question that runs through the book

Chapter 1 ends on Laplace (1814): if the rule is exact and the present is
known, is the future known? The book answers it in stages, and a chapter
may not answer it ahead of its stage:

| Chapter | What it may say about the question |
|---|---|
| 1 | Only for gentle models: an error in the start shrinks or stays the same |
| 2 | An error is multiplied by the slope each step; steep means growth |
| 5 | Chaos appears; the orbit looks random but is exact |
| 6 | The error grows, measured; each digit of precision buys a few steps |
| 7 | The horizon grows only like the logarithm of the precision |
| 14 | What IS predictable beyond the horizon: statistics, probabilities |
| 18 | The answer, as a field guide |

## 3. The determinism rule

Every number is computed by a script under `code/measure/` and checked for
drift by CI. Chaos makes that hard in a way no sibling book faced: a chaotic
trajectory amplifies a last-bit difference between two machines' maths
libraries into a completely different number. So committed values from
chaotic runs use only `+ - * /` and `sqrt` (which are correctly rounded
everywhere) or are robust summaries — averages, exponents to two decimals,
counts. The contract (`notes/03-authoring-contract.md` §4) states the rule;
Chapter 16 makes it the subject.

## 4. The companion library

`code/src/chaoslab/` is a few hundred lines of pure Python that the listings
share: iteration and cobwebs, two steppers for flows, the systems the book
studies, the measurements (separation, Lyapunov exponents, box counting),
and the fractals. It has no dependencies, so every listing that uses it runs
anywhere Python does, and every function in it is tested against a known
answer in `code/tests/test_chaoslab.py` before any chapter relies on it.

## 5. Overlap with the companion volumes

This book shares its machinery with *Mathematics from Zero for the AI
Engineer* and *Python for .NET Engineers* but not its subjects. The one
genuine overlap is floating point: the mathematics volume treats it as a
question of precision and cost for machine learning; Chapter 16 here treats
it as what chaos does to a computed orbit, and says so rather than
repeating the other book's account of the format.

## 6. Open decisions

- **The title.** The repository is called `chaos-theory-for-dummies`; the
  book is titled *Chaos from Zero* / *Chaos od zera*, because "For Dummies"
  is a registered trademark of John Wiley & Sons and this book is not part of
  that series. The title is one line in each title page and main file.
- **Print.** The book is laid out for a screen (A4, one-sided). A print
  edition would need a second geometry and has not been attempted.
