"""Chapter 8's numbers: the forks, the landmarks, Feigenbaum's ratio for two
maps, and the period-three window.

Every value comes from the functions the chapter's listings print
(code/ch08/), so the page and the listings cannot disagree. The logistic
map uses only + - * and /, so its digits are the same on every machine. The
sine map calls math.sin, whose last digit may differ between machines, so
what is committed from it is rounded far above that digit, and the rounding
is checked not to sit on a boundary a last digit could tip.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch08"))

from _values import Values
from bifurcation import long_run
from doublings import forks, settled_period
from superstable import LOGISTIC, from_top, landmarks, ratios
from two_maps import SINE

from chaoslab import logistic, logistic_slope, orbit, period

v = Values("ch08")


def clear_of_boundary(x: float, decimals: int, margin: float = 1e-6) -> None:
    """Fail if x lies within `margin` of a place where rounding to
    `decimals` places would flip: a value computed with math.sin must not."""
    scaled = x * 10 ** decimals
    distance = abs(scaled - math.floor(scaled) - 0.5)
    assert distance > margin * 10 ** decimals, (x, decimals)


# --- one picture for every r ------------------------------------------------
# Above r = 2.8 every kept value is the same: Chapter 5's fixed point 1 - 1/r.
tail = long_run(2.8)
assert max(tail) - min(tail) < 1e-12
assert abs(tail[0] - (1 - 1 / 2.8)) < 1e-12
v.num("fixed", tail[0], ".4f")
assert period(long_run(3.9)) is None       # the smear at 3.9 never repeats

# --- the forks, watched and bisected ----------------------------------------
rs = forks()
assert rs[0] < 3.0, "watching settles too slowly: the first fork reads early"
v.num("fork.one", rs[0], ".4f")
v.num("fork.two", rs[1], ".4f")
v.num("fork.three", rs[2], ".4f")
v.num("fork.four", rs[3], ".4f")
# The ratios of the gaps AS PRINTED, so a reader who divides the printed
# gaps gets the printed ratio.
gaps = [round(b - a, 4) for a, b in zip(rs, rs[1:], strict=False)]
v.num("gap.one", gaps[0], ".4f")
v.num("gap.two", gaps[1], ".4f")
v.num("gap.three", gaps[2], ".4f")
v.num("ratio.one", gaps[0] / gaps[1], ".2f")
v.num("ratio.two", gaps[1] / gaps[2], ".2f")
assert 4.5 < gaps[0] / gaps[1] < 5.0 and 4.5 < gaps[1] / gaps[2] < 5.0

# The second fork exactly. Round the two-cycle a nudge is multiplied by the
# slope at each of its two points; that product is 4 + 2r - r*r. Checked on a
# real two-cycle, not trusted.
r = 3.3
cycle = orbit(logistic(r), 0.5, 2000)[-2:]
product = logistic_slope(r)(cycle[0]) * logistic_slope(r)(cycle[1])
assert abs(product - (4 + 2 * r - r * r)) < 1e-12
exact_two = 1 + math.sqrt(6)            # where 4 + 2r - r*r = -1
assert abs(4 + 2 * exact_two - exact_two ** 2 + 1) < 1e-12
assert 0 < exact_two - rs[1] < 5e-4     # the watched fork reads early
v.num("fork.two.exact", exact_two, ".4f")

# Just below the first fork the orbit truly settles to one value, but a
# nudge is multiplied by 2 - r each step -- close to -1 -- so it dies so
# slowly that twenty thousand steps are not enough to see it.
assert settled_period(2.9998) == 2

# --- the superstable landmarks ---------------------------------------------
found = landmarks(*LOGISTIC, count=11)
assert found[0] == 2.0 or abs(found[0] - 2.0) < 1e-15
assert abs(from_top(logistic(2.0), 1)) == 0.0
assert abs(found[1] - (1 + math.sqrt(5))) < 1e-12   # where 4 + 2r - r*r = 0
v.num("super.two", found[1], ".4f")
v.num("super.four", found[2], ".4f")
v.num("landmark.count", len(found))
delta = ratios(found)[-1]
assert abs(delta - 4.6692016) < 1e-5
v.num("delta", delta, ".4f")
# Where the landmarks are heading: every later gap is the last one divided
# by delta, and so on, which adds up to the last gap divided by (delta - 1).
end = found[-1] + (found[-1] - found[-2]) / (delta - 1)
assert abs(end - 3.5699456) < 1e-6
v.num("end", end, ".4f")
# The forks and the landmarks interleave: fork, landmark, fork, landmark...
assert rs[0] < found[1] < rs[1] < found[2] < rs[2] < found[3] < rs[3]

# --- the sine map -----------------------------------------------------------
sine = landmarks(*SINE, count=11)
sine_ratios = ratios(sine)
for x in sine_ratios:
    clear_of_boundary(x, 2)             # the transcript prints two decimals
clear_of_boundary(sine[-1], 4)          # ... and the last landmark to four
assert abs(sine_ratios[-1] - delta) < 1e-3
v.num("sine.first", sine_ratios[0], ".2f")
v.num("sine.delta", sine_ratios[-1], ".2f")
sine_end = sine[-1] + (sine[-1] - sine[-2]) / (sine_ratios[-1] - 1)
clear_of_boundary(sine_end, 3)
v.num("sine.end", sine_end, ".3f")

# --- the period-three window -----------------------------------------------
opens = 1 + math.sqrt(8)
assert settled_period(opens - 1e-4) is None
assert settled_period(opens + 1e-4) == 3
v.num("window.open", opens, ".4f")
window = landmarks(logistic, (3.82, 3.84), (3.84, 3.848), 9, base=3)
v.num("super.three", window[0], ".4f")
v.num("window.delta", ratios(window)[-1], ".3f")
assert abs(ratios(window)[-1] - delta) < 1e-3

v.write()
