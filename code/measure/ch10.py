"""Chapter 10's numbers: kneading, Henon's map, area and stretch.

Every value comes from the functions the chapter's listings print (code/ch10),
so the page and the listing cannot disagree. The Henon and tent maps use only
+, - and *, so every trajectory here is bit-for-bit the same on every
machine; the one logarithm inside a loop (the Lyapunov exponent) is only
summed, never fed back into the orbit, and is printed to two decimals.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch10"))

from _values import Values
from area import area, length, outline
from cloud import CELL, REFERENCE, marked_squares, square_of
from henon import A, B, henon
from kneading import knead
from stretch import exponent, settle

from chaoslab import henon as lab_henon
from chaoslab import tent

v = Values("ch10")

# --- The rules on the page agree with the shared library's. -------------
lab_rule, lab_tent = lab_henon(A, B), tent(2.0)
x, y = 0.0, 0.0
k = 0.2345
for _ in range(40):
    assert henon(x, y) == lab_rule((x, y))
    assert knead(k) == lab_tent(k)
    x, y = henon(x, y)
    k = knead(k)
v.num("a", A, ".1f")
v.num("b", B, ".1f")

# --- Kneading: the gap doubles until the fold catches one raisin. --------
a, b = 0.2345, 0.2355
gaps = []
for _ in range(14):
    gaps.append(abs(b - a))
    a, b = knead(a), knead(b)
doubled = [n for n in range(1, 14)
           if abs(gaps[n] - 2 * gaps[n - 1]) < 1e-9]
first_fold = next(n for n in range(1, 14) if n not in doubled)
assert doubled[:first_fold - 1] == list(range(1, first_fold)), \
    "it doubles every knead until the fold first catches one raisin"
assert first_fold == 10, "0.001 * 2**10 is past the end of the strip"
assert gaps[10] < 1.0 and gaps[11] < 0.05
v.num("knead.ten", gaps[10], ".2f")
v.num("knead.eleven", gaps[11], ".3f")
v.num("knead.lambda", math.log(2), ".2f")   # every knead stretches by 2

# --- A cloud of starts collapses onto one set. ---------------------------
marked = marked_squares()
cloud = [(-0.5 + (i + 0.5) / 40, -0.5 + (j + 0.5) / 40)
         for i in range(40) for j in range(40)]
n_start = len(cloud)
on_at: dict[int, int] = {}
for step in range(31):
    on_at[step] = sum(square_of(px, py) in marked for px, py in cloud)
    cloud = [henon(px, py) for px, py in cloud]
    cloud = [(px, py) for px, py in cloud if abs(px) + abs(py) < 10]
kept = len(cloud)
settled = next(s for s in (0, 1, 2, 3, 5, 10, 20, 30)
               if on_at[s] == kept and all(on_at[t] == kept
                                           for t in range(s, 31)))
assert settled == 10 and on_at[0] < n_start // 10
v.num("cloud.n", n_start)
v.num("cloud.left", n_start - kept)
v.num("cloud.kept", kept)
v.num("cloud.zero", on_at[0])
v.num("cloud.settled", settled)
v.num("cloud.cell", CELL, ".2f")
v.num("cloud.reference", REFERENCE)

# --- Area shrinks by b every step; the outline grows. --------------------
edge = outline(0.1, 4000)
area0, length0 = area(edge), length(edge)
for step in range(1, 7):
    edge = [henon(px, py) for px, py in edge]
    ratio = area(edge) / area0
    assert abs(ratio - B ** step) < 1e-3 * B ** step, "area times b"
v.num("area.six", ratio, ".5f")
v.num("outline.six", length(edge) / length0, ".1f")
assert length(edge) / length0 > 9
v.num("area.ten", B ** 10, ".7f")

# The area factor of one step, as a tiny parallelogram, is b everywhere.
for px, py in [(0.0, 0.0), (0.5, -0.2), (-1.0, 0.3), (1.2, 0.1)]:
    h = 1e-7
    f0 = henon(px, py)
    fx = henon(px + h, py)
    fy = henon(px, py + h)
    det = ((fx[0] - f0[0]) * (fy[1] - f0[1])
           - (fy[0] - f0[0]) * (fx[1] - f0[1])) / (h * h)
    assert abs(abs(det) - B) < 1e-6

# --- Bounded, and still sensitive. ---------------------------------------
x1, y1 = settle()
x2, y2 = x1 + 1e-10, y1
widest = 0.0
for _ in range(2000):
    x1, y1 = henon(x1, y1)
    x2, y2 = henon(x2, y2)
    dx, dy = x2 - x1, y2 - y1
    widest = max(widest, math.sqrt(dx * dx + dy * dy))
xs = []
x, y = settle()
for _ in range(200_000):
    x, y = henon(x, y)
    xs.append(x)
assert widest < (max(xs) - min(xs)) * 1.1
v.num("gap.widest", widest, ".1f")
v.num("attractor.left", min(xs), ".2f")
v.num("attractor.right", max(xs), ".2f")

lam = exponent()
assert 0.40 < lam < 0.44, "Henon's exponent is about 0.42"
v.num("lambda", lam, ".2f")
v.num("stretch", math.exp(lam), ".2f")
v.num("squeeze", B / math.exp(lam), ".2f")
assert abs(math.exp(lam) * (B / math.exp(lam)) - B) < 1e-12

v.write()
