"""Reference solution for Lab 7.2."""

import math


def horizon(lam: float, delta: float, tol: float) -> float:
    """Steps until an error delta grows to tol, at lam per step."""
    return math.log(tol / delta) / lam


def extra_steps(lam: float, factor: float) -> float:
    """Steps gained by measuring the start `factor` times more precisely."""
    return math.log(factor) / lam


def digits_needed(lam: float, steps: int, tol: float) -> int:
    """Decimal places of the start needed to stay under tol for `steps`."""
    # the error allowed at the start: tol shrunk by e**(lam * steps)
    return math.ceil(-math.log10(tol) + lam * steps / math.log(10))
