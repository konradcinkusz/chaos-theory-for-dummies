"""Chapter 3's numbers: doubling, crowding, the slope at a fixed point, and
the overshoot.

Every value comes from the same functions the chapter's listings print
(code/ch03/), never from a formula written a second time, and every claim
the page makes about a value is asserted here first, so a changed number
fails loudly instead of quietly changing the sentence around it. Only
+, -, * and / are used, so every digit is the same on every machine.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch03"))

from _values import Values
from crowding import next_gen
from doubling import CELL, EARTH, MINUTES, doublings_to_outweigh
from overshoot import in_instalments
from settle import slope_at

v = Values("ch03")

# --- Doubling: one bacterium against the Earth ----------------------------
n = doublings_to_outweigh(EARTH)
assert 2 ** n * CELL > EARTH >= 2 ** (n - 1) * CELL
hours = n * MINUTES / 60
assert 24 < hours < 48, "the page says: under two days"
v.num("earth.doublings", n)
v.num("earth.hours", hours, ".1f")
day = 2 ** (24 * 60 // MINUTES) * CELL / 1e6      # grams to tonnes
v.num("day.tonnes", int(round(day, -2)))
assert 4000 < day < 5000

# --- Doubling against crowding, both from a thousandth, r = 2 -------------
R = 2.0
free, crowded = [0.001], [0.001]
for _ in range(40):
    free.append(R * free[-1])
    crowded.append(next_gen(crowded[-1], R))
full = next(g for g, x in enumerate(free) if x > 1.0)
v.num("exp.full", full)
assert crowded[full] < 0.5, "crowded still below its level when doubling"
# The generation in which the crowded population adds the most.
gains = [b - a for a, b in zip(crowded, crowded[1:], strict=False)]
best = max(range(len(gains)), key=lambda g: gains[g])
v.num("fast.from", best)
v.num("fast.to", best + 1)
assert crowded[best] < 0.25 < crowded[best + 1], "straddles half of 0.5"
# And over every level at once: the gain r*x*(1-x) - x, scanned on a fine
# grid, is largest at exactly half the settled level 1 - 1/r.
for r in (1.5, 2.0, 2.8):
    grid = [i / 100_000 for i in range(100_001)]
    top = max(grid, key=lambda x, r=r: next_gen(x, r) - x)
    assert abs(top - (1 - 1 / r) / 2) < 1e-4
v.num("fast.level", (1 - 1 / R) / 2, ".2f")
v.num("fast.gain", gains[best], ".2f")

# --- Where it settles, and the slope there ---------------------------------
for r in (1.5, 2.0, 2.8, 3.1):
    level = 1 - 1 / r
    assert abs(next_gen(level, r) - level) < 1e-15, "a fixed point"
    assert next_gen(0.0, r) == 0.0
s0 = slope_at(0.0, 1.5)
s15 = slope_at(1 - 1 / 1.5, 1.5)
s20 = slope_at(0.5, 2.0)
assert abs(s0 - 1.5) < 1e-6 and abs(s15 - 0.5) < 1e-6
assert abs(s20) < 1e-6, "the flat top of the hump"
v.num("slope.zero", s0, ".3f")
v.num("slope.third", s15, ".3f")
v.num("slope.half", abs(s20), ".3f")
# The slope IS the multiplier: a nudge of a thousandth from 1/3 at r = 1.5,
# after one generation, is half as large (to within the curve's bend).
nudge = next_gen(1 / 3 + 0.001, 1.5) - (1 - 1 / 1.5)
assert abs(nudge / 0.001 - 0.5) < 0.01

# --- Overshoot at r = 2.8, once a generation and in ten instalments --------
R28 = 2.8
level28 = 1 - 1 / R28
once, paid = [0.01], [0.01]
for _ in range(200):
    once.append(next_gen(once[-1], R28))
    paid.append(in_instalments(paid[-1], R28))
peak = max(range(len(once)), key=lambda g: once[g])
assert once[peak] > level28 + 0.04, "a real overshoot"
assert once[peak + 1] < level28 - 0.04, "and a real fall below"
assert max(paid) <= level28 + 1e-12, "in instalments: never above"
assert abs(once[-1] - level28) < 1e-9 and abs(paid[-1] - level28) < 1e-12
# Early on the instalment population grows FASTER, and still does not
# overshoot: what matters is not speed but how late the brakes act.
assert paid[1] > once[1]
s28 = slope_at(level28, R28)
assert abs(s28 + 0.8) < 1e-6
v.num("over.level", level28, ".3f")
v.num("over.peak", once[peak], ".3f")
v.num("over.peakgen", peak)
v.num("over.fall", once[peak + 1], ".3f")
v.num("slope.over", s28, ".3f")

# --- Past three: the settling stops ---------------------------------------
R31 = 3.1
level31 = 1 - 1 / R31
s31 = slope_at(level31, R31)
assert abs(s31 + 1.1) < 1e-6
x = 0.01
for _ in range(1000):
    x = next_gen(x, R31)
pair = sorted((x, next_gen(x, R31)))
assert abs(next_gen(next_gen(x, R31), R31) - x) < 1e-12, "a two-cycle"
assert pair[0] < level31 - 0.1 and pair[1] > level31 + 0.08
y = 0.01
for _ in range(1000):
    y = in_instalments(y, R31)
assert abs(y - level31) < 1e-12, "in instalments it still settles"
v.num("two.level", level31, ".3f")
v.num("slope.two", s31, ".3f")
v.num("two.low", pair[0], ".3f")
v.num("two.high", pair[1], ".3f")

v.write()
