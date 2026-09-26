"""Chapter 17's numbers: holding the logistic map at its unstable fixed
point, what that costs, and two Lorenz systems falling into step.

Every value comes from the functions the chapter's listings print
(code/ch17/), so the page and the listing cannot disagree. The chaotic runs
use only +, -, * and /, so every step count and every error printed here is
the same on every machine; the one logarithm is taken at the end, of numbers
already fixed.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch17"))

from _values import Values
from control import LEVER, R0, STRETCH, TARGET, nudge, step
from hidden import POINT, rule, visits
from sync import DT, ORIGINAL, drive_and_copy, gap, start
from waiting import wait

from chaoslab import rk4_step

v = Values("ch17")

# --- The unstable fixed point, and a chaotic orbit that keeps visiting it.
assert POINT == TARGET
assert abs(rule(POINT) - POINT) < 1e-15
assert abs(STRETCH - (2.0 - R0)) < 1e-12 and abs(STRETCH) > 1.0
close = visits(0.2, 10_000, 0.01)
v.num("point", POINT, ".3f")
v.num("stretch", STRETCH, ".1f")
v.num("visits", len(close))
v.num("first.visit", close[0])
assert close[0] < 100 and len(close) > 50

# --- The controller: the lever, the gain, and how close is close enough.
largest = 0.01 * R0
gain = -STRETCH / LEVER
v.num("lever", LEVER, ".2f")
v.num("gain", gain, ".2f")
v.num("reach", largest / gain, ".4f")
assert 9.5 < gain < 10.5

# The run the listing prints: chaos for 100 steps, then the controller.
ON = 100
x, xs, changes = 0.2, [], []
for n in range(301):
    change = nudge(x, largest) if n >= ON else 0.0
    xs.append(x)
    changes.append(change)
    x = step(x, change)
catch = next(n for n, c in enumerate(changes) if c != 0.0)
big = [n for n, c in enumerate(changes) if abs(c) > 1e-9 * R0]
settle = big[-1] + 1 - catch             # steps until every nudge is tiny
biggest = max(abs(c) for c in changes)
v.num("catch", catch)
v.num("waited", catch - ON)
v.num("largest.pct", 100 * biggest / R0, ".2f")
v.num("settle", settle)
assert biggest < 0.01 * R0 and settle <= 5
assert all(abs(x - TARGET) < 1e-12 for x in xs[catch + settle:])
total = sum(abs(c) for c in changes)
v.num("total", total, ".3f")

# Brute force: turn r down below 3, where the fixed point is stable, for good.
R_CALM = 2.9
y = 0.2
for _ in range(2000):
    y = R_CALM * y * (1.0 - y)
assert abs(y - (1.0 - 1.0 / R_CALM)) < 1e-12
v.num("brute.point", y, ".3f")
v.num("brute.pct", 100 * (R0 - R_CALM) / R0, ".0f")
assert total * 30 < R0 - R_CALM        # all nudges < one step of force

# --- The price of small nudges: a longer wait. The same thousand starts.
starts = [k / 1001 for k in range(1, 1001)]
means = {}
for percent in (10.0, 1.0, 0.1):
    waits = [wait(x0, percent / 100 * R0) for x0 in starts]
    means[percent] = sum(waits) / len(waits)
    if percent == 1.0:
        v.num("wait.longest", max(waits))
    # Every one of those catches then holds: check a few hundred of them.
    for x0 in starts[::5]:
        xw = x0
        for _ in range(wait(x0, percent / 100 * R0) + 60):
            xw = step(xw, nudge(xw, percent / 100 * R0))
        assert abs(xw - TARGET) < 1e-12
v.num("wait.big", means[10.0], ".0f")
v.num("wait.mid", means[1.0], ".0f")
v.num("wait.small", means[0.1], ".0f")
assert 7 < means[1.0] / means[10.0] < 14
assert 7 < means[0.1] / means[1.0] < 14

# --- Synchronisation: the driven copy against a copy left alone.
s = start()
alone = (s[0], s[3], s[4])
e0 = gap(s[1:3], s[3:5])
t_tol, t_exact, free_min = None, None, math.inf
errs = []
for n in range(4001):
    t = n * DT
    e = gap(s[1:3], s[3:5])
    errs.append(e)
    assert e <= e0 * math.exp(-t) * (1 + 1e-9) + 1e-300, "the bound e**-t"
    if t_tol is None and e < 1e-6:
        t_tol = t
    if t_exact is None and e == 0.0:
        t_exact = n
    if t_exact is not None:
        assert e == 0.0, "once identical, always identical"
    if t >= 5.0:
        free_min = min(free_min, gap(s[0:3], alone))
    s = rk4_step(drive_and_copy, s, DT)
    alone = rk4_step(ORIGINAL, alone, DT)
assert t_tol is not None and t_exact is not None
# The rate of fall between t = 5 and t = 15, a straight line on a log plot.
rate = math.log(errs[500] / errs[1500]) / 10.0
v.num("sync.start", e0, ".1f")
v.num("sync.tol", t_tol, ".1f")
v.num("sync.factor", math.exp(rate), ".0f")
v.num("sync.exact", t_exact * DT, ".1f")
v.num("free.min", free_min, ".1f")
assert rate > 1.0 and free_min > 1.0

v.write()
