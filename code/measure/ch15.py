"""Chapter 15's numbers: two series with one histogram, a return map, a
forecast by analogues, noise, and an epidemic with a school year.

Every value comes from the chapter's own listings (code/ch15/), imported
rather than written a second time. The series are made with +, -, * and /
only, and the randomness comes from Python's Mersenne Twister with named
seeds, so every number here is the same on every machine. Forecast errors
are rounded to two significant figures, which is all the page claims.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch15"))

import epidemic
from _values import Values
from analogues import mean_error
from noisy import right_answers, with_noise
from return_map import squares_touched
from twins import N, histogram, rule_series, shuffled

v = Values("ch15")

# --- Two series, one histogram --------------------------------------------
rule = rule_series()
shuf = shuffled(rule)
assert sorted(rule) == sorted(shuf), "a shuffle keeps every value"
assert histogram(rule) == histogram(shuf)
assert len(set(rule)) == N, "the orbit never repeats a value"
v.num("n", N)
# The first four values of each, for the question "which is the rule?".
# Series A on the page is the SHUFFLED one, series B the rule's.
for k in range(4):
    v.num(f"a.{k + 1}", shuf[k], ".4f")
    v.num(f"b.{k + 1}", rule[k], ".4f")
# 4 x 0.2 x 0.8, which the reader checks by hand
assert abs(rule[1] - 0.64) < 1e-12
hist = histogram(rule)
v.num("hist.low", hist[0])
v.num("hist.mid", hist[2])
assert hist[0] > 2 * hist[2], "the edges are the commonest values"

# --- The return map --------------------------------------------------------
sq_rule, sq_shuf = squares_touched(rule), squares_touched(shuf)
v.num("sq.rule", sq_rule)
v.num("sq.shuf", sq_shuf)
assert sq_rule < 35 and sq_shuf > 95
# Every pair of the rule's series lies exactly on its graph.
on_curve = sum(1 for a, b in zip(rule[:-1], rule[1:], strict=True)
               if b == 4.0 * a * (1.0 - a))
assert on_curve == N - 1

# --- Forecasting by analogues ------------------------------------------------
err_rule = [mean_error(rule, h) for h in range(1, 13)]
err_shuf = [mean_error(shuf, h) for h in range(1, 13)]
v.num("fc.rule", err_rule[0], ".2g")
v.num("fc.shuf", err_shuf[0], ".2g")
# How many times smaller the rule's one-step miss is, to two figures; the
# two printed errors divide to the same figure.
times = int(float(f"{err_shuf[0] / err_rule[0]:.2g}"))
assert times == int(float(f"{0.42 / 0.00099:.2g}"))
v.num("fc.times", times)
# The error roughly doubles each step: the average ratio of successive
# errors over the first seven steps, before the error nears its ceiling.
ratios = [err_rule[h + 1] / err_rule[h] for h in range(6)]
double = sum(ratios) / len(ratios)
v.num("fc.double", double, ".1f")
assert 1.8 < double < 2.2
# The first step at which the rule's forecast misses by more than half as
# much as a forecast of the shuffled numbers.
half = next(h + 1 for h in range(12) if err_rule[h] > 0.5 * err_shuf[h])
v.num("fc.half", half)
assert 8 <= half <= 10
assert all(e > 0.35 for e in err_shuf), "noise is unforecastable"
assert err_rule[-1] > 0.35, "and so is chaos, far enough ahead"

# --- Real data is a mix ------------------------------------------------------
small, big = with_noise(rule, 0.01), with_noise(rule, 0.2)
v.num("noise.small", 0.01, ".2f")
v.num("noise.big", 0.2, ".1f")
v.num("noise.small.err", mean_error(small, 1), ".2g")
v.num("noise.big.err", mean_error(big, 1), ".2g")
v.num("noise.big.sq", squares_touched(big))
assert mean_error(small, 1) > 10 * err_rule[0]
assert mean_error(big, 1) < 0.75 * err_shuf[0], "still told apart"
f10, s10 = right_answers(10, 0.2)
f40, _ = right_answers(40, 0.2)
v.num("short.sq", s10)
v.num("short.fc", f10)
v.num("short.fc.forty", f40)
assert s10 < 50, "worse than tossing a coin"
assert f40 >= 90

# --- An epidemic with a school year ----------------------------------------
v.num("sir.r0", epidemic.R0, ".0f")
v.num("sir.days", epidemic.DAYS_ILL, ".0f")
v.num("sir.life", epidemic.LIFE / 365.0, ".0f")
flat, two, four, wild = (epidemic.yearly_cases(s) for s in epidemic.SEASONS)
v.num("sir.two", epidemic.SEASONS[1], ".1f")
v.num("sir.four", epidemic.SEASONS[2], ".1f")
v.num("sir.wild", epidemic.SEASONS[3], ".1f")
v.num("sir.steady", flat[0], ".0f")


def repeats(xs: list[float], p: int) -> bool:
    """Does the list repeat every p years, to a millionth of a case?"""
    return all(abs(xs[k] - xs[k + p]) < 1e-6 for k in range(len(xs) - p))


assert repeats(flat, 1), "no school year: the same every year"
assert repeats(two, 2) and not repeats(two, 1), "every other year"
assert repeats(four, 4) and not repeats(four, 2), "every fourth year"
assert not any(repeats(wild, p) for p in (1, 2, 3, 4)), "no repeat"


def deepest(season: float) -> float:
    """The smallest fraction infectious in the last eight of the years."""
    s, i = 0.06, 0.001
    births, recover = 1.0 / epidemic.LIFE, 1.0 / epidemic.DAYS_ILL
    beta0, dt = epidemic.R0 * (recover + births), 1.0 / epidemic.STEPS
    low = 1.0
    for year in range(epidemic.YEARS):
        for day in range(365):
            beta = beta0 * epidemic.contact(day, season)
            for _ in range(epidemic.STEPS):
                new = beta * s * i
                s = s + dt * (births - new - births * s)
                i = i + dt * (new - (recover + births) * i)
                if year >= epidemic.YEARS - 8:
                    low = min(low, i)
    return low


low = deepest(epidemic.SEASONS[3])
power = 0
while low * 10 ** (power + 1) < 1.0:
    power += 1
v.num("sir.trough", power)
assert power >= 9, "far below one person in a large city"

v.write()
