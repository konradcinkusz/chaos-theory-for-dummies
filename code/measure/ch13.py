"""Chapter 13's numbers: a double pendulum's energy, its parting, its calm
and wild releases, and the arithmetic of Laskar's five million years.

The pendulums call math.sin and math.cos, whose last binary digit may differ
between machines, and a chaotic pendulum amplifies a last digit until the
whole swing differs. So nothing is committed from late in a chaotic run: the
parting time is a moment long before a last-digit difference could matter,
and every printed number is checked twice before it is written -- once with
the step size changed, once with the release moved by a millionth of a
millionth of a radian. If either moves a printed digit, this script fails
rather than write a number that another machine might not reproduce.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch13"))

from _values import Values
from gentle_wild import SECONDS, fate
from release import DT, RULE, release
from step_check import STEPS, parting
from two_releases import APART, NUDGE, gap

from chaoslab import double_pendulum_energy, rk4_step

SHAKE = 1e-12   # radians: far larger than any last-digit difference


def steady(value: float, fmt: str, rel: float = 1e-6) -> str:
    """Format `value`, refusing if a relative wobble of `rel` could change
    the printed digits (a number sitting on a rounding boundary)."""
    out = format(value, fmt)
    for k in (1 - rel, 1 + rel):
        if format(value * k, fmt) != out:
            raise AssertionError(f"{value!r} prints on a boundary as {fmt}")
    return out


def shaken_parting(dt: float, shake: float) -> float:
    """parting(dt), but with both releases moved round by `shake`: the
    listing's loop again, for a robustness check only."""
    a = release(120, 120)
    a = (a[0] + shake, a[1], a[2], a[3])
    b = (a[0] + NUDGE, a[1], a[2], a[3])
    step = 0
    while gap(a, b) <= APART:
        a, b = rk4_step(RULE, a, dt), rk4_step(RULE, b, dt)
        step += 1
    return step * dt


v = Values("ch13")
v.num("dt", DT, ".3f")

# ---- the release, and its energy ------------------------------------------
start = release(120, 120)
e0 = double_pendulum_energy(start)
# Held up above the pivot by half an arm and a whole arm: 9.81 * 1.5.
assert abs(e0 - 1.5 * 9.81) < 1e-9
v.num("energy.start", e0, ".1f")

# The table release.py prints must survive a shaken release, digit for digit.
def release_table(shake: float) -> list[str]:
    s = release(120, 120)
    s = (s[0] + shake, s[1], s[2], s[3])
    rows = []
    for step in range(10_001):
        if step % 2000 == 0:
            rows.append(f"{math.degrees(s[0]):.1f} {math.degrees(s[1]):.1f} "
                        f"{double_pendulum_energy(s):.8f}")
        s = rk4_step(RULE, s, DT)
    return rows


assert release_table(0.0) == release_table(SHAKE) == release_table(-SHAKE)

# ---- the parting, with every step size ------------------------------------
results = {dt: parting(dt) for dt in STEPS}
times = {steady(t, ".2f") for t, _ in results.values()}
assert len(times) == 1, f"the parting moves with the step: {results}"
seconds, worst = results[DT]
assert {steady(shaken_parting(DT, s), ".2f") for s in (SHAKE, -SHAKE)} \
    == times
for _, w in results.values():
    steady(w, ".1e")           # the energy column of step_check.py
v.num("apart.seconds", float(steady(seconds, ".1f")), ".1f")

# The energy moved by about one part in 10**8 of itself before the parting.
parts = math.log10(e0 / worst)
assert 7.6 < parts < 8.4, parts
v.num("energy.moved", float(steady(worst, ".0e")), ".0e")
v.num("energy.parts", 10.0 ** round(parts), ".0e")

# Halving the step divides the energy error by about sixteen (RK4's order).
shrink = results[DT][1] / results[DT / 2][1]
assert 14 < shrink < 18, shrink
v.num("energy.shrink", float(steady(shrink, ".0f")), ".0f")

# The gap two-releases.py prints each second, checked against a shake.
def gap_table(shake: float) -> list[str]:
    a = release(120, 120)
    a = (a[0] + shake, a[1], a[2], a[3])
    b = (a[0] + NUDGE, a[1], a[2], a[3])
    rows, step = [], 0
    while gap(a, b) <= APART:
        if step % 1000 == 0:
            rows.append(steady(gap(a, b), ".0e", rel=1e-4))
        a, b = rk4_step(RULE, a, DT), rk4_step(RULE, b, DT)
        step += 1
    return rows


assert gap_table(0.0) == gap_table(SHAKE) == gap_table(-SHAKE)

# ---- the stepper's own errors are a nudge too, and a smaller one ----------
# The SAME release stepped at DT and at DT/2: when do the two computations
# of one pendulum differ by a visible tenth of a radian?
a = b = release(120, 120)
step = 0
while gap(a, b) <= APART:
    a = rk4_step(RULE, a, DT)
    b = rk4_step(RULE, rk4_step(RULE, b, DT / 2), DT / 2)
    step += 1
self_split = step * DT
assert self_split > seconds + 3, (self_split, seconds)
v.num("stepper.apart", float(steady(self_split, ".0f")), ".0f")

# ---- gentle and wild releases ---------------------------------------------
def shaken_fate(angle: float, shake: float) -> str:
    """The line gentle_wild.py prints for `angle`, from a shaken release:
    the listing's loop again, for a robustness check only."""
    a = release(angle, angle)
    a = (a[0] + shake, a[1], a[2], a[3])
    b = (a[0] + NUDGE, a[1], a[2], a[3])
    largest = gap(a, b)
    for step in range(1, round(SECONDS / DT) + 1):
        a, b = rk4_step(RULE, a, DT), rk4_step(RULE, b, DT)
        if gap(a, b) > APART:
            return f"apart after {step * DT:4.1f} s"
        largest = max(largest, gap(a, b))
    return f"largest gap {steady(largest, '.0e', rel=1e-4)} rad"


fates = {angle: fate(angle) for angle in range(10, 180, 20)}
calm = [a for a, (t, _) in fates.items() if t is None]
wild = [a for a, (t, _) in fates.items() if t is not None]
assert calm and wild and max(calm) < min(wild), fates
for angle in fates:
    lines = {shaken_fate(angle, s) for s in (0.0, SHAKE, -SHAKE)}
    assert len(lines) == 1, (angle, lines)
v.num("calm.upto", max(calm))
v.num("wild.from", min(wild))
v.num("window", round(SECONDS))
top_gap = fates[max(calm)][1]
assert top_gap < 1e-4, "the calm releases barely drift"
v.num("calm.gap", float(steady(top_gap, ".0e")), ".0e")

# ---- the solar system: Laskar's five million years, as arithmetic --------
# An error multiplied by e every five million years, for a hundred million.
growth = math.exp(100 / 5)
v.num("solar.factor", float(steady(growth, ".1e")), ".1e")
km = round(1.0 * growth / 1000, -4)     # one metre today, in kilometres
assert 384_400 < km < 1_000_000, "more than the distance to the Moon"
v.num("solar.km", int(km))

v.write()
