"""Chapter 16's numbers: what a computer keeps, and what it does to chaos.

Everything here uses +, -, * and / on floats, exact Fractions, Decimals
(whose arithmetic, square root included, is correctly rounded by its own
standard) and struct's rounding to single precision -- all identical on
every machine. The one call to the maths library, the exact fraction of
time the logistic map spends below 0.1, is made once at the end and
printed to three decimals, where its last bit cannot reach.
"""

from __future__ import annotations

import math
import struct
import sys
from collections import Counter
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch16"))

from _machine import bits_kept, find_loop, rule_single, to_single
from _values import Values
from doubling import exact_doubling
from more_digits import orbit, right_for
from shadow import computed, exact_orbit, fraction_below, shadow
from two_formulas import rule_a, rule_b, truth

from chaoslab import doubling

v = Values("ch16")

# --- What a computer keeps -------------------------------------------------
bits_d = bits_kept(lambda x: x)
bits_s = bits_kept(to_single)
assert (bits_d, bits_s) == (53, 24)
v.num("bits.double", bits_d)
v.num("bits.single", bits_s)
v.num("decimal.double", bits_d * math.log10(2), ".0f")
v.num("decimal.single", bits_s * math.log10(2), ".0f")
err = Decimal(0.1) - Decimal(1) / 10
assert 0 < err < Decimal("1e-17")
v.num("tenth.err", float(err), ".2e")
num, den = (0.1).as_integer_ratio()
power = den.bit_length() - 1
assert den == 2**power and num % 2 == 1
v.num("tenth.power", power)
assert 0.1 + 0.2 != 0.3 and (0.1 + 0.2) + 0.3 != 0.1 + (0.2 + 0.3)

# --- The doubling map ------------------------------------------------------


def collapse(x: float, limit: int = 2000) -> int:
    n = 0
    while x != 0.0:
        x, n = doubling(x), n + 1
        assert n < limit
    return n


# The computer's doubling map makes NO rounding error: its orbit is exactly
# the true orbit of the number it stored. Checked, not assumed.
x, f = 0.1, Fraction(0.1)
for _ in range(60):
    assert Fraction(x) == f
    x, f = doubling(x), exact_doubling(f)
v.num("collapse.tenth", collapse(0.1))
assert collapse(0.1) == power
# The true orbit of one tenth: a loop of four that never reaches zero.
t = Fraction(1, 10)
seen = [t]
for _ in range(8):
    t = exact_doubling(t)
    seen.append(t)
assert seen[1] == seen[5] and 0 not in seen
steps = [collapse(k / 997) for k in range(1, 997)]
v.num("collapse.starts", len(steps))
v.num("collapse.min", min(steps))
v.num("collapse.max", max(steps))
v.num("collapse.mode", Counter(steps).most_common(1)[0][0])
assert collapse(0.3) == (0.3).as_integer_ratio()[1].bit_length() - 1
v.num("collapse.three", collapse(0.3))

# --- One rule, two programs ------------------------------------------------
N = 80
a, b, s = [0.1], [0.1], [to_single(0.1)]
for _ in range(N):
    a.append(rule_a(a[-1]))
    b.append(rule_b(b[-1]))
    s.append(rule_single(s[-1]))
true = [float(t) for t in truth(N)]
# The truth is carried far enough: a hundred digits agree with two hundred.
assert all(abs(p - q) < Decimal("1e-60")
           for p, q in zip(truth(N), truth(N, 200), strict=True))


def first(cond) -> int:
    return next(n for n in range(N + 1) if cond(n))


v.num("formulas.first", first(lambda n: a[n] != b[n]))
v.num("formulas.apart", first(lambda n: abs(a[n] - b[n]) > 0.1))
wrong_a = first(lambda n: abs(a[n] - true[n]) > 0.1)
wrong_b = first(lambda n: abs(b[n] - true[n]) > 0.1)
wrong_s = first(lambda n: abs(s[n] - true[n]) > 0.1)
v.num("wrong.a", wrong_a)
v.num("wrong.b", wrong_b)
v.num("wrong.single", wrong_s)
# The prediction: rounding leaves an error of about 2**-bits, the map
# doubles it every step, and the question is when it reaches 0.1.
pred_d = math.log2(0.1 * 2**bits_d)
pred_s = math.log2(0.1 * 2**bits_s)
v.num("predict.double", pred_d, ".0f")
v.num("predict.single", pred_s, ".0f")
assert abs(wrong_a - pred_d) < 10 and abs(wrong_b - pred_d) < 10
assert abs(wrong_s - pred_s) < 5 and wrong_s < min(wrong_a, wrong_b)

# --- Why more digits cannot save you --------------------------------------
x = Fraction(1, 10)
digits = []
for _ in range(13):
    digits.append(len(str(x.denominator)))
    x = 4 * x * (1 - x)
# Each step squares the bottom of the fraction: 10, then 5**2, 5**4, ...
assert all(digits[n] == math.floor(2**n * math.log10(5)) + 1
           for n in range(1, 13))
v.num("exact.ten", digits[10])
v.num("exact.twenty", math.floor(2**20 * math.log10(5)) + 1)
v.num("exact.fifty", 2**50 * math.log10(5), ".1e")
v.num("exact.fifty.tb", 2**50 * math.log2(5) / 8 / 1e12, ".0f")
long_truth = orbit(1000, 600)
right = {d: right_for(d, long_truth) for d in (16, 32, 64, 128)}
assert all(3.2 < right[d] / d < 3.5 for d in right)
v.num("right.sixteen", right[16])
v.num("right.per.digit", math.log2(10), ".1f")

# --- Wrong path, right picture --------------------------------------------
xs = computed(rule_a, 1000)
ys = shadow(xs)
tr = exact_orbit(ys[0], 1000)
# The backward orbit IS an exact orbit: forwards from its start, with enough
# digits, it reproduces every backward value.
assert max(abs(p - q) for p, q in zip(ys, tr, strict=True)) < Decimal("1e-90")
gap = max(abs(t - Decimal(x)) for t, x in zip(tr, xs, strict=True))
v.num("shadow.steps", len(xs) - 1)
v.num("shadow.start", abs(float(ys[0] - Decimal(1) / 10)), ".1e")
v.num("shadow.gap", float(gap), ".1e")
assert gap < Decimal("1e-13")
STATS = 1_000_000
frac_a = fraction_below(computed(rule_a, STATS)[1:], 0.1)
frac_b = fraction_below(computed(rule_b, STATS)[1:], 0.1)
xsingle, below = to_single(0.1), 0
for _ in range(STATS):
    xsingle = rule_single(xsingle)
    below += xsingle < 0.1
frac_s = below / STATS
exact = 2 / math.pi * math.asin(math.sqrt(0.1))
v.num("stats.a", frac_a, ".3f")
v.num("stats.b", frac_b, ".3f")
v.num("stats.exact", exact, ".3f")
v.num("stats.single", frac_s, ".3f")
assert abs(frac_a - exact) < 0.002 and abs(frac_b - exact) < 0.002
assert frac_s - exact > 0.01

# --- Machines that repeat --------------------------------------------------


def count_up_to_one(fmt: str, ifmt: str) -> int:
    """How many non-negative numbers of this format are <= 1: the bit
    pattern of 1.0 read as a whole number, plus one for zero."""
    return struct.unpack(ifmt, struct.pack(fmt, 1.0))[0] + 1


v.num("count.single", count_up_to_one("<f", "<I"))
v.num("count.double", count_up_to_one("<d", "<Q"))
tail, length = find_loop(rule_single, to_single(0.1))
v.num("loop.tail", tail)
v.num("loop.length", length)
loops = set()
for k in range(1, 200):
    tl, ln = find_loop(rule_single, to_single(k / 200))
    y = to_single(k / 200)
    for _ in range(tl):
        y = rule_single(y)
    members = [y]
    for _ in range(ln - 1):
        members.append(rule_single(members[-1]))
    loops.add(min(members))
v.num("loop.starts", 199)
v.num("loop.kinds", len(loops))
assert length == max(find_loop(rule_single, to_single(k / 200))[1]
                     for k in range(1, 200))

v.write()
