"""Reference solution for Lab 12.2."""

import math

DOUBLINGS = (3.0, 1 + math.sqrt(6), 3.544090, 3.564407, 3.569946)


def r_to_c(r: float) -> float:
    """The c at which z -> z*z + c is the logistic map at r."""
    return r / 2 - r * r / 4


def c_to_r(c: float) -> float:
    """The r, at least 1, that r_to_c turns into c (c at most 1/4)."""
    return 1 + math.sqrt(1 - 4 * c)


def to_z(x: float, r: float) -> float:
    """Where the logistic state x sits on the z line."""
    return r * (0.5 - x)


def doublings_in_c() -> list[float]:
    """Every r in DOUBLINGS, turned into c."""
    return [r_to_c(r) for r in DOUBLINGS]
