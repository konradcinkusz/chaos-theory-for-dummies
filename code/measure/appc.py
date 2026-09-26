"""Appendix C's numbers: the few constants the toolkit quotes.

The appendix is a reference, so every value in it is either arithmetic the
reader does in their head or one of these, computed rather than remembered.
"""

from __future__ import annotations

import math

from _values import Values

v = Values("appc")

v.num("ln2", math.log(2), ".3f")
v.num("ln10", math.log(10), ".3f")
v.num("e", math.e, ".3f")
v.num("doublings.per.digit", math.log(10) / math.log(2), ".2f")
v.num("doublings.thousand", math.log(1000) / math.log(2), ".2f")


def cube(x: float) -> float:
    return x * x * x


# The slope of x cubed at x = 2 is exactly 12; the numerical recipe of
# Chapter 2 with a step of one hundredth lands close to it.
h = 0.01
approx = (cube(2 + h) - cube(2 - h)) / (2 * h)
assert abs(approx - 12) < 1e-3
v.num("slope.h", h, ".2f")
v.num("slope.approx", approx, ".4f")

v.write()
