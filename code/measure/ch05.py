"""Chapter 5's numbers: four settings of the knob, a fixed point, a cycle
detector, a window of order and an orbit that never comes back.

Every value is computed from the functions the chapter's listings print
(code/ch05/) or from chaoslab, which the listings call. The logistic map
uses only multiplication and subtraction, which are correctly rounded, so
every value here -- even those taken from a chaotic orbit -- is identical on
every machine. Each claim the page makes is asserted before its number is
written, so a changed number fails here rather than silently changing the
sentence around it.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch05"))

from _values import Values
from fixed_point import fixed_point
from four_rates import after, step

from chaoslab import logistic, orbit, period, slope

v = Values("ch05")

# The chapter's own one-line rule and the library's are the same arithmetic,
# digit for digit, so the listings that use either print the same numbers.
for r in (2.8, 3.2, 3.5, 3.83, 3.9, 4.0):
    for x in (0.1, 0.2, 0.5, 0.7, 0.93):
        assert step(r, x) == logistic(r)(x)

# The think box in section 1: x1 and x2 at r = 2.8 from 0.5, done by hand.
assert abs(step(2.8, 0.5) - 0.7) < 1e-12
assert abs(step(2.8, step(2.8, 0.5)) - 0.588) < 1e-12

# Section 2: the printout of four_rates.py, steps 200 to 207 from 0.2.
rest = after(2.8, 0.2, 200, 8)
assert max(rest) - min(rest) < 1e-9, "r = 2.8 has come to rest"
assert abs(rest[0] - fixed_point(2.8)) < 1e-9, "...on the fixed point"
v.num("fp.28", fixed_point(2.8), ".3f")

two = after(3.2, 0.2, 200, 8)
assert period(two, longest=4) == 2
v.num("two.lo", min(two), ".3f")
v.num("two.hi", max(two), ".3f")

four = after(3.5, 0.2, 200, 8)
assert period(four, longest=4) == 4
v.num("four.lo", min(four), ".3f")
v.num("four.hi", max(four), ".3f")

wild = after(3.9, 0.2, 200, 8)
assert len({round(x, 3) for x in wild}) == 8, "no value repeats in the row"

# Section 3: the fixed point 1 - 1/r, and the slope there, which is 2 - r.
v.num("fp.32", fixed_point(3.2), ".3f")
assert min(two) < fixed_point(3.2) < max(two), "the 2-cycle straddles it"
for r in (2.8, 3.2, 3.5, 3.9):
    x = fixed_point(r)
    assert abs(step(r, x) - x) < 1e-12, "the rule leaves it unchanged"
    assert abs(slope(logistic(r), x) - (2.0 - r)) < 1e-6
assert step(2.0, 0.5) == 0.5 and step(4.0, 0.75) == 0.75  # the think box

# Where the fixed point lets go, found by halving an interval (the first
# lab does the same). The page derives it by hand: 2 - r = -1 at r = 3.
lo, hi = 2.5, 3.5
while hi - lo > 1e-9:
    mid = (lo + hi) / 2
    if abs(slope(logistic(mid), fixed_point(mid))) < 1:
        lo = mid
    else:
        hi = mid
assert abs(lo - 3.0) < 1e-6

# Section 4: the cobweb's first corner is 2.8 * 0.2 * 0.8 = 0.448.
assert abs(step(2.8, 0.2) - 0.448) < 1e-12

# Section 5: the detector's verdicts, as periods.py prints them.
for r, want in ((2.8, 1), (3.2, 2), (3.5, 4), (3.9, None), (4.0, None)):
    assert period(orbit(logistic(r), 0.2, 2000)) == want, r

# ...and a hundred thousand steps in which no value comes back, run twice.
steps = 100_000
for r in (3.9, 4.0):
    xs = orbit(logistic(r), 0.2, steps)
    assert len(set(xs)) == steps + 1, r
    assert xs == orbit(logistic(r), 0.2, steps), "same start, same orbit"
v.num("never.steps", steps)
v.num("never.values", steps + 1)

# The window: at r = 3.83 the orbit locks into a cycle of three after a
# short scramble (the page says "short"; here it is under forty steps).
w = orbit(logistic(3.83), 0.2, 2000)
assert period(w) == 3
cycle = sorted(w[-3:])
far = [n for n, x in enumerate(w) if min(abs(x - c) for c in cycle) > 1e-3]
assert max(far) < 40, "the scramble before the window's cycle is short"
v.num("win.a", cycle[0], ".3f")
v.num("win.b", cycle[1], ".3f")
v.num("win.c", cycle[2], ".3f")

# Section 6, the teaser figure: two starts a millionth apart at r = 3.9 lie
# on top of each other at first and then part completely. No number reaches
# the page -- counting the steps is Chapter 6's measurement.
a = orbit(logistic(3.9), 0.2, 60)
b = orbit(logistic(3.9), 0.200001, 60)
gaps = [abs(p - q) for p, q in zip(a, b, strict=True)]
assert max(gaps[:12]) < 1e-3, "indistinguishable on the plot at first"
assert max(gaps) > 0.5, "and then unrelated"

v.write()
