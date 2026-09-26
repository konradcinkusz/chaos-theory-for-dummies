"""Chapter 12's numbers: angles that add, orbits that linger, the area nobody
knows, and Chapter 8's cascade found again on the real axis.

Every value comes from the same functions the listings print (code/ch12/)
or from chaoslab, which the listings import. Escape times and bulb centres
use only +, - and *, so they are the same on every machine; the one angle
is printed to two decimals, which the last bit of atan2 cannot move, and
the areas are counts rounded to two figures.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parents[1] / "ch12"
sys.path.insert(0, str(HERE))

from _values import Values
from ascii_mandelbrot import LIMIT as ASCII_LIMIT
from chaoslab import escape_time, logistic, r_to_c
from complex_numbers import degrees, times
from slow_escape import LIMIT as SLOW_LIMIT

v = Values("ch12")

# --- Section 1: lengths multiply, angles add -------------------------------
z = 3 + 4j
assert times(3, 4, 3, 4) == (-7, 24) and z * z == -7 + 24j
assert abs(z) == 5.0 and abs(z * z) == 25.0
angle, twice = degrees(z), degrees(z * z)
assert abs(twice - 2 * angle) < 1e-9, "angles add"
v.num("angle", angle, ".2f")
v.num("angle.twice", twice, ".2f")

# --- Section 2: the orbit of 0, and how long a near miss lingers ----------
assert escape_time(1) == 3                      # 0, 1, 2, 5: gone
assert escape_time(-2, 1000) == 1000            # 0, -2, 2, 2, ... for ever
assert escape_time(0.25, SLOW_LIMIT) == SLOW_LIMIT
slow = {c: escape_time(c, SLOW_LIMIT) for c in (0.3, 0.26, 0.251, 0.2501)}
steps = list(slow.values())
assert steps == sorted(steps), "closer to 1/4 must linger longer"
# Ten times closer to 1/4 costs about three times the steps (sqrt 10).
assert all(2.8 < b / a < 3.4 for a, b in zip(steps[1:], steps[2:],
                                               strict=False))
v.num("slow.300", slow[0.3])
v.num("slow.260", slow[0.26])
v.num("slow.251", slow[0.251])
v.num("slow.2501", slow[0.2501])

# --- Section 3: the drawing, and the area ---------------------------------
src = (HERE / "ascii_mandelbrot.py").read_text(encoding="utf8").splitlines()
start = src.index("# --8<-- [start:draw]")
end = src.index("# --8<-- [end:draw]")
code_lines = [s for s in src[start + 1:end] if s.strip()]
v.num("draw.lines", len(code_lines))
v.num("draw.limit", ASCII_LIMIT)


def area(limit: int, h: float = 0.005) -> float:
    """Count grid cells of side h whose centre c has not escaped after
    `limit` steps. The upper half is counted and doubled, since the set is
    its own mirror image in the real axis."""
    xs = -2.0 + h * (np.arange(round(2.5 / h)) + 0.5)
    ys = h * (np.arange(round(1.25 / h)) + 0.5)
    cx, cy = (a.ravel() for a in np.meshgrid(xs, ys))
    x, y = np.zeros_like(cx), np.zeros_like(cy)
    for _ in range(limit):
        x, y = x * x - y * y + cx, 2.0 * x * y + cy
        keep = x * x + y * y <= 4.0
        x, y, cx, cy = x[keep], y[keep], cx[keep], cy[keep]
    return 2 * x.size * h * h


areas = {n: area(n) for n in (50, 200, 1000)}
assert areas[50] > areas[200] > areas[1000] > 1.5, "the count only falls"
for n, a in areas.items():
    v.num(f"area.{n}", a, ".2f")

# --- Section 4: a Julia set whose c is outside --------------------------
dust = escape_time(complex(-0.8, 0.2), 1000)
assert dust < 1000
v.num("dust.escape", dust)


# --- Section 5: Chapter 8's cascade on the real axis -----------------------
def c_to_r(c: float) -> float:
    """The r >= 1 with r/2 - r*r/4 = c."""
    return 1.0 + math.sqrt(1.0 - 4.0 * c)


for r in (1.0, 2.0, 3.0, 3.5, 4.0):
    assert abs(c_to_r(r_to_c(r)) - r) < 1e-12
assert r_to_c(3.0) == -0.75
v.num("c.two", r_to_c(1 + math.sqrt(6)), ".2f")      # 2 -> 4 at 1 + sqrt 6
v.num("c.window", r_to_c(1 + math.sqrt(8)), ".2f")   # period 3 opens


def orbit_of_zero(c: float, n: int) -> tuple[float, float]:
    """z after n steps from 0, and how fast it moves as c moves."""
    zn, dz = 0.0, 0.0
    for _ in range(n):
        zn, dz = zn * zn + c, 2.0 * zn * dz + 1.0
    return zn, dz


def centre(p: int, guess: float) -> float:
    """The c near `guess` at which the orbit of 0 is back at 0 after p
    steps: the centre of a bulb. Newton's method, + - * / only."""
    c = guess
    for _ in range(100):
        zn, dz = orbit_of_zero(c, p)
        c, shift = c - zn / dz, zn / dz
        if abs(shift) < 1e-15:
            break
    return c


centres = [0.0, -1.0]                 # periods 1 and 2: by hand
for k in range(2, 11):
    gap = centres[-1] - centres[-2]
    ratio = 4.0 if k == 2 else (centres[-3] - centres[-2]) / -gap
    centres.append(centre(2 ** k, centres[-1] + gap / ratio))
for k, c in enumerate(centres):
    period = 2 ** k
    assert abs(orbit_of_zero(c, period)[0]) < 1e-9
    assert k < 1 or abs(orbit_of_zero(c, period // 2)[0]) > 1e-3
    # The same parameter, seen from the logistic side: the cycle passes
    # through x = 1/2, which is where z = 0 sits.
    r = c_to_r(c)
    x = 0.5
    for _ in range(period):
        x = logistic(r)(x)
    assert abs(x - 0.5) < 1e-8, (period, x)
ratios = [(centres[i - 2] - centres[i - 1]) / (centres[i - 1] - centres[i])
          for i in range(2, len(centres))]
a, b, c = centres[-3:]
limit_c = c - (c - b) ** 2 / ((c - b) - (b - a))     # Aitken's extrapolation
assert abs(limit_c - centres[-1]) < 1e-5 and ratios[-1] > 4.6

v.num("centre.4", centres[2], ".4f")
v.num("centre.8", centres[3], ".4f")
v.num("rc.2", c_to_r(centres[1]), ".4f")
v.num("rc.4", c_to_r(centres[2]), ".4f")
v.num("rc.8", c_to_r(centres[3]), ".4f")
v.num("feig.ratio", ratios[-1], ".3f")
v.num("feig.c", limit_c, ".3f")
v.num("feig.r", c_to_r(limit_c), ".4f")

v.write()
