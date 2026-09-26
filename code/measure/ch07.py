"""Chapter 7's numbers: one number for chaos, and what it buys.

Every value is computed with the functions the chapter's listings print
(code/ch07/), so the page and the listing cannot disagree. The orbits use
only + - * /, so they are identical on every machine; math.log is applied
to each stretch along the way, and a last-bit difference in a logarithm
moves an average of a hundred thousand of them by far less than the two
decimals committed here.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch07"))

from _values import Values
from exponent import exponent
from horizon import counts, horizon
from stretch import factors, step, stretch

from chaoslab import logistic, logistic_slope, lyapunov

v = Values("ch07")
LN2 = math.log(2)

# --- 1. Eight steps at r = 4: the stretch of the gap IS the slope --------
fs = factors(4.0, 0.3, 1e-10, 8)
x = 0.3
for f in fs:
    assert abs(f - abs(stretch(4.0, x))) < 1e-5 * f, "gap growth != slope"
    x = step(4.0, x)
product = math.prod(fs)
mean = sum(fs) / len(fs)
assert max(fs) > 3.9 and min(fs) < 0.35, "the table shows big and small"
v.num("eight.product", product, ".0f")
v.num("eight.mean", mean, ".2f")
v.num("eight.meanpow", mean ** 8, ".0f")
assert mean ** 8 > 5 * product, "averaging the factors overshoots badly"
rate = math.log(product) / 8
v.num("eight.rate", rate, ".2f")
v.num("eight.geo", math.exp(rate), ".2f")
assert abs(math.exp(rate) ** 8 - product) < 1e-9 * product

# --- 2. The natural logarithm ---------------------------------------------
v.num("ln.two", LN2, ".2f")
v.num("ln.four", math.log(4), ".2f")
v.num("ln.half", math.log(0.5), ".2f")
v.num("ln.ten", math.log(10), ".2f")
v.num("ln.eight", math.log(8), ".2f")
v.num("e", math.e, ".3f")
assert abs(math.log(8) - 3 * LN2) < 1e-12

# --- 3. The exponent at four settings of r --------------------------------
lams = {r: exponent(r) for r in (2.8, 3.2, 3.5, 4.0)}
assert all(lams[r] < 0 for r in (2.8, 3.2, 3.5)) and lams[4.0] > 0
# r = 4: the exact value is ln 2, and the average agrees to a thousandth.
assert abs(lams[4.0] - LN2) < 0.001
v.num("lam.four", lams[4.0], ".2f")
v.num("ln.two.long", LN2, ".4f")
# r = 2.8: the orbit sits on the fixed point 1 - 1/r, whose slope is 2 - r,
# so every term of the average is ln 0.8.
assert abs(lams[2.8] - math.log(0.8)) < 1e-9
v.num("ln.pointeight", math.log(0.8), ".2f")
v.num("lam.twoeight", lams[2.8], ".2f")
# r = 3.2: a two-cycle, whose two slopes multiply to 4 + 2r - r*r.
assert abs(lams[3.2] - 0.5 * math.log(4 + 2 * 3.2 - 3.2 * 3.2)) < 1e-6
v.num("lam.threetwo", lams[3.2], ".2f")
v.num("lam.threefive", lams[3.5], ".2f")
# r = 3: the borderline, where the fixed point's slope is exactly -1. The
# average creeps towards zero slowly; within a thousandth is what the page
# claims.
assert abs(exponent(3.0)) < 0.001

# --- 4. The horizon -------------------------------------------------------
v.num("lyap.time", 1 / LN2, ".2f")
tol = 0.1
v.num("hz.million", horizon(LN2, 1e-6, tol), ".0f")
v.num("hz.billion", horizon(LN2, 1e-9, tol), ".0f")
v.num("ln.thousand", math.log(1000), ".2f")
gain = math.log(1000) / LN2
v.num("extra.thousand", gain, ".0f")
v.num("per.ten", math.log(10) / LN2, ".1f")
# The count agrees with the formula to within a step, and every thousandfold
# improvement buys the same ten steps, measured.
means = []
for delta in (1e-3, 1e-6, 1e-9, 1e-12):
    c = counts(4.0, delta, tol)
    means.append(sum(c) / len(c))
    assert 0 < means[-1] - horizon(LN2, delta, tol) < 1.0
diffs = [b - a for a, b in zip(means, means[1:], strict=False)]
assert all(abs(d - gain) < 0.1 for d in diffs), diffs
v.num("hz.gained", sum(diffs) / len(diffs), ".1f")
# What a double's sixteen digits buy, and what a long forecast would need.
v.num("hz.sixteen", horizon(LN2, 1e-16, tol), ".0f")
v.num("digits.hundred", math.ceil(1 + 100 * LN2 / math.log(10)))
v.num("digits.thousand", math.ceil(1 + 1000 * LN2 / math.log(10)))
# A horizon in Lyapunov times: ln of how many times the error may grow.
v.num("ln.tenbillion", math.log(1e10), ".0f")

# --- 5. The exponent across r ---------------------------------------------
sweep = {(340 + 4 * k) / 100:
         lyapunov(logistic((340 + 4 * k) / 100),
                  logistic_slope((340 + 4 * k) / 100), 0.3, 20_000)
         for k in range(16)}
assert sweep[3.56] < 0 < sweep[3.6], "chaos starts between 3.56 and 3.6"
assert sweep[3.84] < 0 < sweep[3.8] and sweep[3.88] > 0, "a window at 3.84"

v.write()
