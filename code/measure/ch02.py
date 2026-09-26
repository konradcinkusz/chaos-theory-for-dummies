"""Chapter 2's numbers: orbits, doubling times, fixed points and slopes.

Every value comes from the same rules the chapter's listings print, or from
chaoslab's `linear` and `orbit`, which those listings use -- never from a
formula written a second time. The logarithm appears only at the end of a
computation, on a number that is already fixed, so every digit here is the
same on every machine.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch02"))

from _values import Values
from doubling import doubling_time, steps_to_double
from drug import DOSE, KEPT, steady, tablets
from slope import square

from chaoslab import linear, orbit, slope

v = Values("ch02")

# --- The savings account: 1000 at 5 per cent, a year at a time. ----------
# Printed exactly: the rule keeps every digit; a bank would round to pence.
save = orbit(linear(1.05, 0.0), 1000.0, 10)
v.num("save.two", save[2], ".1f")
v.num("save.three", save[3], ".3f")
v.num("save.ten", save[10], ".2f")
# The shortcut the think box asks for: ten multiplications by 1.05.
assert abs(save[10] - 1000.0 * 1.05 ** 10) < 1e-9

# --- Two accounts: add 50 a year, or grow 2 per cent a year. -------------
adds = orbit(linear(1.0, 50.0), 1000.0, 120)
grows = orbit(linear(1.02, 0.0), 1000.0, 120)
assert adds[30] == 2500.0
v.num("acc.grows.thirty", grows[30], ".0f")
cross = next(n for n in range(121) if grows[n] > adds[n])
assert 60 < cross < 100, "the slow exponential is behind for a lifetime"
assert all(grows[n] < adds[n] for n in range(1, cross))
v.num("acc.cross", cross)

# --- How many steps until: doubling and halving. -------------------------
v.num("dbl.seven.count", steps_to_double(0.07))
v.num("dbl.seven.log", doubling_time(0.07), ".2f")
v.num("dbl.one.log", doubling_time(0.01), ".0f")
assert steps_to_double(0.07) == math.ceil(doubling_time(0.07))
assert doubling_time(0.01) > 69, "one per cent is exponential, and slow"
v.num("ln.two", math.log(2.0), ".3f")
v.num("ln.seven", math.log(1.07), ".4f")
# At 2 per cent the table says 35.00 and 36: after 35 years the balance is
# a hair short of double.
short = orbit(linear(1.02, 0.0), 1.0, 35)[-1]
assert 1.999 < short < 2.0 and steps_to_double(0.02) == 36
v.num("dbl.two.short", short, ".4f")
v.num("dbl.two.log", doubling_time(0.02), ".2f")
v.num("dbl.two.count", steps_to_double(0.02))
# The checkpoint's town at 3 per cent.
v.num("dbl.three.log", doubling_time(0.03), ".2f")
v.num("dbl.three.count", steps_to_double(0.03))
assert steps_to_double(0.03) == math.ceil(doubling_time(0.03))
# A half-life: a drug of which the body clears a fifth every hour.
half = math.log(0.5) / math.log(0.8)
assert 3 < half < 4
v.num("half.fifth", half, ".1f")

# --- One tablet a morning: the fixed point and the gap. ------------------
levels = orbit(tablets, DOSE, 40)
assert steady == 200.0
gaps = [steady - x for x in levels]
assert all(abs(gaps[n + 1] - KEPT * gaps[n]) < 1e-12 for n in range(40))
within = next(n for n, g in enumerate(gaps) if g < 1.0)
v.num("drug.within", within)
# The pharmacists' rule of thumb: four or five half-lives to steady state.
v.num("drug.four", 100 * (1 - KEPT ** 4), ".1f")
v.num("drug.five", 100 * (1 - KEPT ** 5), ".1f")

# --- The loan: 1 per cent a month, 100 a month repaid. -------------------
loan = linear(1.01, -100.0)
assert abs(loan(10000.0) - 10000.0) < 1e-9, "10000 is the fixed point"
up = orbit(loan, 11000.0, 120)
assert all(b > a for a, b in zip(up, up[1:], strict=False))
v.num("loan.up", up[-1], ".0f")
down = orbit(loan, 9000.0, 400)
payoff = next(n for n, x in enumerate(down) if x <= 0.0)
v.num("loan.payoff", payoff)
v.num("loan.years", payoff / 12, ".0f")

# --- The slope, measured by nudging. -------------------------------------
for x in (0.0, 150.0, 400.0):
    assert abs(slope(tablets, x) - KEPT) < 1e-6
assert abs(slope(square, 1.5) - 3.0) < 1e-6
exact = square(1.501) - square(1.5)
v.num("nudge.exact", exact, ".6f")
assert abs(exact - 3 * 0.001) < 2e-6

v.write()
