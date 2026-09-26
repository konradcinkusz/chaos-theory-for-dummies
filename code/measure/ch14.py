"""Chapter 14's numbers: an ensemble forecast on Lorenz's toy atmosphere,
its spread and its skill, the chance of rain it gives and how often that
chance comes true, and the climate of two long runs and of a hotter one.

Every value comes from the functions the chapter's listings print
(code/ch14/), and every trajectory is stepped with + - * / only, so the
page and the listings cannot disagree and no digit depends on the
machine. The one logarithm inside a loop is lyapunov_flow's, which sums
logs without feeding them back into the run, and its result is quoted
to two decimals.
"""

from __future__ import annotations

import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch14"))

from _skill import CASES, average_scores, single_errors, truths
from _values import Values
from chance_of_rain import RAIN, chance
from climate import HOT, climate
from ensemble import (
    DT,
    ERROR,
    FORCING,
    MEMBERS,
    N,
    ensemble,
    run,
    spin_up,
)

from chaoslab import lorenz96, lyapunov_flow

v = Values("ch14")
v.num("members", MEMBERS)
v.num("error", ERROR, ".1f")
v.num("dt", DT, ".2f")
v.num("rain", RAIN, ".0f")
v.num("forcing", FORCING, ".0f")
v.num("hot", HOT, ".0f")
v.num("cases", CASES)

# How fast errors grow in the toy atmosphere: Chapter 7's exponent.
lam = lyapunov_flow(lorenz96(FORCING), spin_up(), DT, 20000, burn=0)
assert 1.6 < lam < 1.8, lam
v.num("lambda", lam, ".2f")
v.num("double", math.log(2) / lam, ".2f")

# The climate: two long runs from different starts agree to two figures;
# a run with the forcing turned up does not.
a = climate(FORCING, 0.01)
b = climate(FORCING, 1.0)
hot = climate(HOT, 0.01)
for i, fmt in ((0, ".1f"), (1, ".1f"), (2, ".2f")):
    assert format(a[i], fmt) == format(b[i], fmt), (i, a[i], b[i])
assert abs(a[3] - b[3]) > 1.0, "their weather on the last day must differ"
assert hot[1] > a[1] and hot[2] > a[2], "a stronger drive, a wilder climate"
v.num("clim.average", a[0], ".1f")
v.num("clim.swing", a[1], ".1f")
v.num("clim.rain", round(100 * a[2]))
v.num("hot.average", hot[0], ".1f")
v.num("hot.swing", hot[1], ".1f")
v.num("hot.rain", round(100 * hot[2]))
sigma = a[1]   # the error of always forecasting the climate average

# The ensemble, averaged over CASES forecasts: spread tracks the error of
# the mean; a single run ends up worse than the climate average.
leads, sp, e_mean, e_one = average_scores()
one, three = 20, 60                     # leads of 1 and 3 time units
for k in (one, three):
    assert abs(sp[k] - e_mean[k]) < 0.25 * e_mean[k], (k, sp[k], e_mean[k])
v.num("sp.one", sp[one], ".2f")
v.num("err.one", e_mean[one], ".2f")
v.num("sp.three", sp[three], ".2f")
v.num("err.three", e_mean[three], ".2f")

tail = range(120, 161)                  # leads 6 to 8: long past the horizon
sat_spread = sum(sp[k] for k in tail) / len(tail)
sat_mean = sum(e_mean[k] for k in tail) / len(tail)
sat_one = sum(e_one[k] for k in tail) / len(tail)
assert abs(sat_one - math.sqrt(2) * sigma) < 0.3, (sat_one, sigma)
assert abs(sat_mean - sigma) < 0.3 and sat_mean < sat_one
v.num("sat.spread", sat_spread, ".1f")
v.num("sat.mean", sat_mean, ".1f")
v.num("sat.one", sat_one, ".1f")

horizon = next(t for t, e in zip(leads, e_one, strict=True) if e > sigma)
assert 2.0 < horizon < 4.0, horizon
assert all(e < sigma for e in e_mean[: leads.index(horizon) + 1])
v.num("horizon", horizon, ".2f")

saturate = next(t for t, s in zip(leads, sp, strict=True)
                if s >= 0.9 * sat_spread)
v.num("saturate", saturate, ".2f")

# Chapter 7's rule on the toy: each tenfold improvement in the analysis
# buys about the same extra lead, ln(10) / lambda.
check = single_errors(ERROR)
alone = next(k * DT for k, e in enumerate(check) if e > sigma)
assert abs(alone - horizon) < 0.3, (alone, horizon)
law = [horizon]
for size in (ERROR / 10, ERROR / 100):
    errs = single_errors(size)
    law.append(next(k * DT for k, e in enumerate(errs) if e > sigma))
gains = [law[1] - law[0], law[2] - law[1]]
step = math.log(10) / lam
for g in gains:
    assert abs(g - step) < 0.5 * step, (gains, step)
v.num("law.two", law[1], ".2f")
v.num("law.three", law[2], ".2f")
v.num("law.gain.a", gains[0], ".2f")
v.num("law.gain.b", gains[1], ".2f")
v.num("law.step", step, ".2f")

# Keeping score: of all the times the ensemble gave a chance near 30 or
# near 70 per cent, how often did it rain?
rng = random.Random(1401)
state = spin_up()
pairs = []
for _ in range(150):
    state = run(state, 30)
    _, members = ensemble(state, rng)
    members = [run(m, 40) for m in members]
    later = run(state, 40)
    for site in range(N):
        pairs.append((chance(members, site), later[site] > RAIN))


def kept(low: float, high: float) -> tuple[int, int]:
    hits = [rained for p, rained in pairs if low <= p <= high]
    return len(hits), round(100 * sum(hits) / len(hits))


n_low, low = kept(0.25, 0.35)
n_high, high = kept(0.65, 0.75)
assert abs(low - 30) <= 8 and abs(high - 70) <= 8, (low, high)
v.num("rel.pairs", len(pairs))
v.num("rel.low.n", n_low)
v.num("rel.low", low)
v.num("rel.high.n", n_high)
v.num("rel.high", high)

assert len(truths()) == CASES
v.write()
