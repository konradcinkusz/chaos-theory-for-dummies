"""Chapter 9's numbers: Lorenz's fixed points, the butterfly, two runs a
hair apart, the exponent of the flow, and two statistics of the attractor.

Every run here uses only +, -, * and / (and one sqrt per distance), so the
trajectories are the same on every machine; the one sum of logarithms (the
exponent) is committed to two decimals, which the last bit cannot move.
Each value is computed with the SAME functions the chapter's listings
print, imported from code/ch09.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch09"))

from _values import Values
from averages import STARTS, fraction_right, mean_height
from cloud import corners, room
from exponent import STARTS as LAMBDA_STARTS
from lorenz_run import DT, loops, path
from two_runs import a, b, first_apart

from chaoslab import horizon, integrate, lorenz, lyapunov_flow, rk4_step

v = Values("ch09")
SIGMA, RHO, BETA = 10.0, 28.0, 8.0 / 3.0


def away_from_rounding(x: float, digits: int) -> None:
    """A value about to be committed rounded must not sit on a boundary."""
    scaled = x * 10 ** digits
    assert abs(scaled - math.floor(scaled) - 0.5) > 1e-6, x


# The fixed points. The rest state and two steady rolls, x = y = +-sqrt(72),
# z = 27: every rate is exactly zero there (8/3 * 27 = 72).
xy = math.sqrt(BETA * (RHO - 1))
field = lorenz()
for s in [(0.0, 0.0, 0.0), (xy, xy, RHO - 1), (-xy, -xy, RHO - 1)]:
    assert all(abs(r) < 1e-12 for r in field(s)), s
v.num("fixed.xy", xy, ".2f")

# The run from (1, 1, 1): how many loops on the left wing before the first
# flip to the right (the first letter is the start's own rise, skipped).
seq = loops(path[100:])
first_run = len(seq) - len(seq.lstrip("L"))
assert seq[first_run] == "R" and first_run > 10
v.num("loops.left", first_run)

# Turn the heating down to 20 and the same start settles on a steady roll.
rest = integrate(lorenz(rho=20.0), (1.0, 1.0, 1.0), DT, 10_000)[-1]
steady = math.sqrt(BETA * (20.0 - 1))
assert abs(abs(rest[0]) - steady) < 1e-3 and abs(rest[2] - 19.0) < 1e-3
v.num("steady.x", steady, ".2f")
# The heating at which the steady rolls stop being stable (not derived here).
hopf = SIGMA * (SIGMA + BETA + 3) / (SIGMA - BETA - 1)
assert abs(hopf - 470 / 19) < 1e-12
v.num("rho.hopf", hopf, ".2f")

# Two runs a hair apart: the listing's pair, then fifty pairs along the
# attractor, split every two time units, to show how much the moment varies.
first = first_apart(a, b)
v.num("apart.first", first, ".1f")
times = []
state = a
for _ in range(50):
    for _ in range(200):
        state = rk4_step(field, state, DT)
    times.append(first_apart(state, (state[0] + 1e-8, state[1], state[2])))
v.num("apart.pairs", len(times))
v.num("apart.min", min(times), ".0f")
v.num("apart.max", max(times), ".0f")
v.num("apart.mean", sum(times) / len(times), ".0f")

# The exponent from the listing's three starts, and Chapter 7's horizon.
lams = [lyapunov_flow(field, s, DT, 50_000) for s in LAMBDA_STARTS]
for lam in lams:
    away_from_rounding(lam, 2)
    assert round(lam, 1) == 0.9, lam
v.num("lambda.lo", min(lams), ".2f")
v.num("lambda.hi", max(lams), ".2f")
v.num("lambda", 0.9, ".1f")
# The page divides the printed ln(10^8) by the printed 0.9, so the horizon
# is committed at a precision that division reproduces.
v.num("ln.eight", math.log(1e8), ".1f")
v.num("stretch", math.exp(0.9), ".1f")
hor = horizon(0.9, 1e-8, 1.0)
assert round(hor) == round(round(math.log(1e8), 1) / 0.9)
v.num("horizon", hor, ".0f")
assert min(times) < hor < max(times)
v.num("gain.thousand", horizon(0.9, 1e-3, 1.0), ".0f")

# The cloud: eight far-away corners, all living in the same room.
# (Checked against the long run's room further down.)
rooms = [room(c) for c in corners]

# Statistics that do not care about the start: 500 time units from each of
# the listing's five starts, and then 2000 to show the spread shrinking.
fracs, heights = [], []
for s in STARTS:
    p = integrate(field, s, DT, 51_000)[1000:]
    fracs.append(fraction_right(p))
    heights.append(mean_height(p))
for x in fracs + heights:
    away_from_rounding(x, 2)
v.num("frac.lo", min(fracs), ".2f")
v.num("frac.hi", max(fracs), ".2f")
v.num("height.lo", min(heights), ".2f")
v.num("height.hi", max(heights), ".2f")
assert max(fracs) - min(fracs) < 0.05
assert max(heights) - min(heights) < 0.2

# How much a finite run's fraction wobbles: chop one run of 20,000 time
# units into pieces, and measure the spread (standard deviation) of the
# fraction from piece to piece. Longer pieces, smaller wobble.
long = integrate(field, (1.0, 1.0, 1.0), DT, 2_001_000)[1000:-1]
right = [1 if p[0] > 0 else 0 for p in long]
v.num("long.time", len(right) // 100)
# The room the long run lives in, rounded outwards.
v.num("long.x", math.ceil(max(abs(p[0]) for p in long)))
v.num("long.zlo", math.floor(min(p[2] for p in long)))
v.num("long.zhi", math.ceil(max(p[2] for p in long)))
assert max(r[0] for r in rooms) < max(abs(p[0]) for p in long)
assert min(r[1] for r in rooms) > min(p[2] for p in long)
assert max(r[2] for r in rooms) < max(p[2] for p in long)
v.num("long.frac", sum(right) / len(right), ".2f")


def wobble(units: int) -> float:
    n = units * 100
    pieces = [sum(right[i:i + n]) / n for i in range(0, len(right), n)]
    m = sum(pieces) / len(pieces)
    return math.sqrt(sum((q - m) * (q - m) for q in pieces) / len(pieces))


short, longer = wobble(100), wobble(2000)
assert longer < short / 3
for x in (short, longer):
    away_from_rounding(x, 2)
v.num("wobble.short", short, ".2f")
v.num("wobble.long", longer, ".2f")

v.write()
