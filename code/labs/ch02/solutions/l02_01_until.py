"""Reference solution for Lab 2.1."""

import math


def steps_until(a: float, ratio: float) -> int:
    """Whole steps of x -> a * x, from x = 1, until x has reached `ratio`."""
    x, steps = 1.0, 0
    if ratio >= 1.0:
        while x < ratio:
            x = a * x
            steps += 1
    else:
        while x > ratio:
            x = a * x
            steps += 1
    return steps


def time_until(a: float, ratio: float) -> float:
    """The n for which a ** n equals ratio."""
    return math.log(ratio) / math.log(a)


def half_life(cleared: float) -> float:
    """Steps until half is left when `cleared` is removed every step."""
    return time_until(1.0 - cleared, 0.5)
