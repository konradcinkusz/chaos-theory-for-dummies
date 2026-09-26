"""Chapter 1's numbers: the stone, the tea, and the gap between two cups.

Each value is computed from the same rule the chapter's listings print, not
from a formula written a second time, so the page and the listing cannot
disagree about what the model says.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch01"))

from _values import Values
from cooling_cup import ROOM, K, next_minute
from falling_stone import G, distance

v = Values("ch01")

v.num("g", G, ".2f")
v.num("stone.three", distance(3), ".1f")
v.num("stone.five", distance(5), ".1f")
v.num("stone.ten.time", math.sqrt(2 * 10 / G), ".2f")

# The tea: start, one minute, and the first minute below sixty degrees.
temps = [90.0]
for _ in range(60):
    temps.append(next_minute(temps[-1]))
v.num("tea.start", temps[0], ".0f")
v.num("tea.room", ROOM, ".0f")
v.num("tea.k", K, ".1f")
v.num("tea.one", temps[1], ".0f")
drinkable = next(n for n, t in enumerate(temps) if t < 60.0)
v.num("tea.drinkable", drinkable)
assert temps[1] == 83.0, "the rule is 90 - 0.1 * 70"

# Two cups one degree apart: the gap is multiplied by (1 - K) every minute,
# so it SHRINKS. Checked against the closed form rather than trusted.
a, b = 90.0, 91.0
for _ in range(30):
    a, b = next_minute(a), next_minute(b)
gap30 = b - a
assert abs(gap30 - (1 - K) ** 30) < 1e-12
v.num("gap.factor", 1 - K, ".1f")
v.num("gap.thirty", gap30, ".3f")
v.num("gap.hundredth", math.ceil(math.log(0.01) / math.log(1 - K)))

v.write()
