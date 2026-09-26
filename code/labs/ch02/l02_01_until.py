"""Lab 2.1 -- how many steps until?

A quantity that is multiplied by the same number `a` every step -- a
balance growing at interest, a drug washing out of the blood -- reaches any
target you name eventually, if the target lies in the direction it is
moving. Answer the question two ways: by counting steps, and by asking the
logarithm, which Python spells math.log (the natural logarithm, ln).
"""

import math  # noqa: F401 -- you will need it


def steps_until(a: float, ratio: float) -> int:
    """Whole steps of x -> a * x, from x = 1, until x has reached `ratio`.

    Growth (a > 1) reaches a ratio above 1: stop once x >= ratio.
    Decay (0 < a < 1) reaches a ratio below 1: stop once x <= ratio.
    """
    raise NotImplementedError("your turn: replace this line")


def time_until(a: float, ratio: float) -> float:
    """The same question asked of the logarithm, in fractions of a step:
    the n for which a ** n equals ratio."""
    raise NotImplementedError("your turn: replace this line")


def half_life(cleared: float) -> float:
    """Steps until half is left, when the fraction `cleared` of what is
    there is removed every step (0.2 means a fifth goes each step)."""
    raise NotImplementedError("your turn: replace this line")
