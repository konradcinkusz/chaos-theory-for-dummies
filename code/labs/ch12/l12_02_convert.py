"""Lab 12.2 -- from the logistic map's r to the Mandelbrot set's c, and back.

The change of variables z = r * (1/2 - x) turns x -> r*x*(1 - x) into
z -> z*z + c with c = r/2 - r*r/4. Write the conversion both ways, check it
by running the two rules side by side, then send the period-doubling points
across and see where on the real axis they land.
"""

import math

# Where the logistic map's cycle doubles: 1 -> 2 at r = 3, 2 -> 4 at
# 1 + sqrt(6), 4 -> 8 and 8 -> 16 a little later, and the point where the
# doublings pile up. The last three to six decimals.
DOUBLINGS = (3.0, 1 + math.sqrt(6), 3.544090, 3.564407, 3.569946)


def r_to_c(r: float) -> float:
    """The c at which z -> z*z + c is the logistic map at r."""
    raise NotImplementedError("your turn: replace this line")


def c_to_r(c: float) -> float:
    """The r, at least 1, that r_to_c turns into c (c at most 1/4).

    Undo r_to_c: r*r - 2*r + 4*c = 0, and of its two roots keep the one
    that is at least 1. Python spells a square root math.sqrt.
    """
    raise NotImplementedError("your turn: replace this line")


def to_z(x: float, r: float) -> float:
    """Where the logistic state x sits on the z line: z = r * (1/2 - x)."""
    raise NotImplementedError("your turn: replace this line")


def doublings_in_c() -> list[float]:
    """Every r in DOUBLINGS, turned into c."""
    raise NotImplementedError("your turn: replace this line")
