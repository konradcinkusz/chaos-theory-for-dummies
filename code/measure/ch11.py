"""Chapter 11's numbers: rulers, the Koch curve, the Cantor set, and two
box-counting dimensions.

Every value comes from the same functions the chapter's listings print
(code/ch11/), so the page and the listing cannot disagree. The Henon points
use only +, - and *, and the boxes are powers of two, so every count is
identical on every machine; a logarithm is taken only at the end, of counts
that are already fixed, and the dimensions are committed to two decimals.
"""

from __future__ import annotations

import math
import sys
from itertools import pairwise
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch11"))

from _ruler import length
from _values import Values
from henon_boxes import SIZES as HENON_SIZES
from henon_boxes import attractor
from koch_boxes import POINTS as KOCH_POINTS
from koch_boxes import SIZES as KOCH_SIZES
from koch_boxes import counts, dimension
from koch_length import area
from semicircle import rounds

from chaoslab import cantor, koch

v = Values("ch11")

# --- A smooth curve settles: half a circle measured with shorter rulers.
semi = [length(p) for p in rounds(8)]
gains = [b - a for a, b in pairwise(semi)]
assert all(g > 0 for g in gains), "a shorter ruler never measures less"
assert abs(semi[-1] - math.pi) < 1e-4
ratio = gains[-1] / gains[-2]
assert abs(ratio - 0.25) < 0.01, "each round adds a quarter of the last"
v.num("pi", math.pi, ".5f")
v.num("semi.gain", ratio, ".2f")

# --- The Koch curve: length times 4/3 every round, height and area fixed.
H = math.sqrt(3.0) / 6.0           # the height of the first tent
LIMIT = math.sqrt(3.0) / 20.0      # the area the rounds settle towards
for n in range(8):
    pts = koch(n)
    assert abs(length(pts) - (4 / 3) ** n) < 1e-9
    if n:
        assert abs(max(y for _, y in pts) - H) < 1e-15
        assert area(pts) < LIMIT
assert LIMIT - area(koch(7)) < 0.005 * LIMIT
v.num("koch.six", length(koch(6)), ".3f")
v.num("koch.twenty", (4 / 3) ** 20, ".0f")
v.num("koch.height", H, ".4f")
v.num("koch.area", LIMIT, ".4f")

# --- The Cantor set: two pieces a third as long, every round.
pieces = cantor(20)
left = sum(b - a for a, b in pieces)
assert len(pieces) == 2**20
assert abs(left / (2 / 3) ** 20 - 1) < 1e-6   # b - a near 1 rounds
v.num("cantor.pieces", len(pieces))
v.num("cantor.left", left, ".4f")

# --- Dimensions from counting copies.
KOCH_D = math.log(4) / math.log(3)
CANTOR_D = math.log(2) / math.log(3)
assert 1 < KOCH_D < 2 and 0 < CANTOR_D < 1
v.num("koch.dim", KOCH_D, ".2f")
v.num("cantor.dim", CANTOR_D, ".2f")
v.num("koch.halve", 2**KOCH_D, ".1f")

# --- Box counting on the Koch curve: all ten sizes, and any five in a row.
ns = counts(KOCH_POINTS, KOCH_SIZES)
kd = dimension(KOCH_SIZES, ns)
fives = [dimension(KOCH_SIZES[i:i + 5], ns[i:i + 5]) for i in range(6)]
assert abs(kd - KOCH_D) < 0.01
assert min(fives) < KOCH_D < max(fives)
v.num("koch.corners", len(KOCH_POINTS))
v.num("koch.boxdim", kd, ".2f")
v.num("koch.five.lo", min(fives), ".2f")
v.num("koch.five.hi", max(fives), ".2f")

# --- Box counting on the Henon attractor, with few and with many points.
FEW, MANY = 100_000, 1_000_000
few = counts(attractor(FEW), HENON_SIZES)
many = counts(attractor(MANY), HENON_SIZES)
d_few = dimension(HENON_SIZES, few)
d_many = dimension(HENON_SIZES, many)
fives = [dimension(HENON_SIZES[i:i + 5], many[i:i + 5]) for i in range(5)]
assert 1.2 < d_few < d_many < 1.3, "more points find more small boxes"
assert all(1.2 < d < 1.3 for d in fives)
v.num("henon.few", FEW)
v.num("henon.many", MANY)
v.num("henon.dim.few", d_few, ".2f")
v.num("henon.dim", d_many, ".2f")
v.num("henon.five.lo", min(fives), ".2f")
v.num("henon.five.hi", max(fives), ".2f")

v.write()
