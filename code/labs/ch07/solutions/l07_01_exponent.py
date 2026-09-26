"""Reference solution for Lab 7.1."""

import math


def stretch(r: float, x: float) -> float:
    """The slope of the logistic map at x: r*(1 - 2x)."""
    return r * (1.0 - 2.0 * x)


def exponent(r: float, x0: float = 0.3, steps: int = 100_000,
             burn: int = 1000) -> float:
    """The average of ln|stretch(r, x)| over `steps` points of the orbit
    from x0, after throwing away the first `burn` steps."""
    x = x0
    for _ in range(burn):
        x = r * x * (1.0 - x)
    total = 0.0
    for _ in range(steps):
        total += math.log(abs(stretch(r, x)))
        x = r * x * (1.0 - x)
    return total / steps
