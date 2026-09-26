"""Chapter 6's numbers: two runs peeling apart, and what a digit is worth.

Every value comes from the functions the chapter's listings print (code/
ch06/), imported rather than written a second time. The logistic map at
r = 4 and the doubling map use only +, - and *, so every count here is the
same on every machine: a count of steps is exact, and the one average is
of numbers that are themselves exact.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch06"))

from _values import Values
from digits import binary_digits, sides
from printout import FULL, PRINTED, again, first, rounded
from twins import NUDGE, START, rule, twin_runs
from worth import ERRORS, TOL, average_steps

from chaoslab import separation, steps_until_apart

v = Values("ch06")

v.num("start", START, ".1f")
v.num("tol", TOL, ".1f")

# The twins: how long they agree to a millionth, and when they are apart.
million = steps_until_apart(rule, START, NUDGE, 1e-6)
apart = steps_until_apart(rule, START, NUDGE, TOL)
a, b = twin_runs(60)
assert all(abs(y - x) <= 1e-6 for x, y in zip(a[:million], b[:million],
                                                strict=True))
assert abs(b[apart] - a[apart]) > TOL
assert apart < 50, "the twins part within a few dozen steps"
v.num("twins.million", million)
v.num("twins.apart", apart)

# Over the whole run the gap grows by about a factor of two a step: from
# 1e-10 past 0.1 is a billionfold, and 2**30 is about a billion.
assert 2 ** (apart - 1) < TOL / NUDGE < 2 ** (apart + 1)

# The ceiling: once apart, the gap wanders; its long-run average is a robust
# summary, and every term in it was computed with + - * only.
g = separation(rule, START, NUDGE, 100_100)
ceiling = sum(g[100:]) / len(g[100:])
assert 0.3 < ceiling < 0.5
assert max(g) < 1.0
v.num("ceiling", ceiling, ".1f")

# The doubling map: the side at each step IS the next binary digit, and two
# starts stay on the same side exactly as long as they share digits.
for x in (START, START + NUDGE):
    assert sides(x, 50) == binary_digits(x, 50)
da, db = binary_digits(START, 50), binary_digits(START + NUDGE, 50)
shared = next(i for i in range(50) if da[i] != db[i])
sa, sb = sides(START, 50), sides(START + NUDGE, 50)
assert shared == next(i for i in range(50) if sa[i] != sb[i])
v.num("digits.shared", shared)

# What a digit is worth: the average number of steps a forecast survives,
# for starts known to 2, 4, ... 12 decimal places.
steps = {d: average_steps(e) for d, e in ERRORS.items()}
per_digit = (steps[12] - steps[2]) / 10
assert all(steps[d] < steps[d + 2] for d in (2, 4, 6, 8, 10))
assert 3.0 < per_digit < 3.6, "a decimal digit is a little over 3 binary"
v.num("worth.two", steps[2], ".1f")
v.num("worth.ten", steps[10], ".1f")
v.num("worth.twelve", steps[12], ".1f")
v.num("worth.per", per_digit, ".1f")

# Lorenz's printout: the full start reruns identically; the rounded one
# does not, and parts company well before the twins did.
assert again == first
lorenz = steps_until_apart(rule, FULL, PRINTED - FULL, TOL)
assert all(abs(y - x) <= TOL for x, y in zip(first[:lorenz],
                                              rounded[:lorenz], strict=True))
assert abs(rounded[lorenz] - first[lorenz]) > TOL
assert lorenz < apart
v.num("lorenz.apart", lorenz)

v.write()
