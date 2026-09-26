"""Chapter 4's numbers: a spring's energy under two steppers, a pendulum's
swing times, a loop that motion settles onto, and Kepler's third law.

Every value comes from the functions the chapter's listings print
(code/ch04/), so the page and the listing cannot disagree. The spring, the
settling loop and the planet use only +, -, *, / and sqrt, so their digits
are the same on every machine; the pendulum calls math.sin, but it is not
chaotic, so a last-bit difference moves its swing times in the twelfth
decimal and the page prints three.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch04"))

from _settle import swing, van_der_pol
from _values import Values
from energy_drift import FIELD, drift
from pendulum import period
from spring import energy, euler_step
from two_bodies import SPEEDS, orbit

from chaoslab import euler_step as lib_euler
from chaoslab import integrate, rk4_step

v = Values("ch04")

# --- Euler on the spring: the energy is multiplied by 1 + dt*dt per step.
DT = 0.1
x, s_v = 1.0, 0.0
factors = []
for _ in range(100):
    e0 = energy(x, s_v)
    x, s_v = euler_step(x, s_v, DT)
    factors.append(energy(x, s_v) / e0)
assert all(abs(f - (1 + DT * DT)) < 1e-12 for f in factors)
# The chapter's hand-written step is the library's step, digit for digit.
state = (1.0, 0.0)
for _ in range(100):
    state = lib_euler(FIELD, state, DT)
assert state == (x, s_v), "spring.py and chaoslab take the same step"
v.num("euler.dt", DT, ".1f")
v.num("euler.factor", 1 + DT * DT, ".2f")
v.num("euler.steps", 100)
v.num("euler.energy.ten", energy(x, s_v), ".2f")
gain = drift(lib_euler, DT, 10)
assert abs(gain - (1.01 ** 100 - 1)) < 1e-9
v.num("euler.gain.ten", 100 * gain, ".0f")

# --- A ten times smaller step: the same gain, ten times later.
small_ten = drift(lib_euler, 0.01, 10)
small_hundred = drift(lib_euler, 0.01, 100)
assert small_ten < gain / 10
assert abs(small_hundred / gain - 1) < 0.02, "same gain, ten times later"
v.num("small.dt", 0.01, ".2f")
v.num("small.gain.ten", 100 * small_ten, ".1f")
v.num("small.gain.hundred", 100 * small_hundred, ".0f")

# --- RK4 against Euler for the same work: four rule calls a step.
same = drift(lib_euler, 0.025, 10)
rk4_ten = drift(rk4_step, DT, 10)
rk4_long = drift(rk4_step, DT, 1000)
assert rk4_ten < 0.0 and rk4_long < 0.0, "RK4 loses a very little"
assert 1e-7 < -rk4_ten < 1e-5
v.num("same.dt", 0.025, ".3f")
v.num("same.gain", 100 * same, ".0f")
v.num("rk4.ppm", -1e6 * rk4_ten, ".1f")
v.num("rk4.ppm.thousand", -1e6 * rk4_long, ".0f")
better = same / -rk4_ten
assert 150_000 < better < 250_000
v.num("rk4.better", int(round(better / 10_000)) * 10_000)
# Halving the step: RK4's energy error shrinks 32-fold, Euler's gain only
# about halves (in its logarithm). Checked, not printed as a table.
assert 30 < rk4_ten / drift(rk4_step, DT / 2, 10) < 34

# --- The pendulum: swing time grows with the swing.
p10, p90, p170 = period(10), period(90), period(170)
assert p10 < p90 < p170
v.num("pend.ten", p10, ".3f")
v.num("pend.ninety", p90, ".3f")
v.num("pend.big", p170, ".3f")
v.num("pend.ninety.pct", 100 * (p90 / p10 - 1), ".0f")
v.num("pend.ratio", p170 / p10, ".1f")
v.num("pend.small", 2 * math.pi / math.sqrt(9.81), ".3f")

# --- A loop that motion settles onto, from inside and from outside.
loop = van_der_pol()
inner = integrate(loop, (0.1, 0.0), 0.01, 6000)
outer = integrate(loop, (4.0, 0.0), 0.01, 6000)
reach_in, reach_out = swing(inner, 800), swing(outer, 800)
assert abs(reach_in - reach_out) < 1e-3
assert 1.9 < reach_in < 2.1
v.num("vdp.start.in", 0.1, ".1f")
v.num("vdp.start.out", 4.0, ".0f")
v.num("vdp.reach.in", reach_in, ".2f")
v.num("vdp.reach.out", reach_out, ".2f")
v.num("vdp.time", 60)

# --- Two bodies: every lap on schedule, and Kepler's third law.
laws = []
for speed in SPEEDS:
    first, average, size = orbit(speed)
    assert abs(first - average) < 1e-9, "the tenth lap is on schedule"
    laws.append(average * average / (size * size * size))
assert max(laws) - min(laws) < 1e-6
assert abs(laws[0] - 4 * math.pi * math.pi) < 1e-6
v.num("kepler.law", laws[0], ".2f")
v.num("kepler.orbits", len(SPEEDS))

v.write()
