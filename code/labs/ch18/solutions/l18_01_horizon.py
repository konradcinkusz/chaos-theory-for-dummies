"""Reference solution for Lab 18.1."""

import math


def forecast_length(exponent: float, digits: int,
                    tolerance: float = 0.1) -> float:
    """Steps before the forecast's error exceeds `tolerance`."""
    error = 1 / 10**digits
    return math.log(tolerance / error) / exponent


def extra_steps(exponent: float, factor: float) -> float:
    """How many more steps a measurement `factor` times as precise buys."""
    return math.log(factor) / exponent


def digits_needed(exponent: float, steps: int,
                  tolerance: float = 0.1) -> int:
    """The fewest correct decimal places for `steps` steps of forecast."""
    # The error may grow by e**(exponent * steps) and still end below
    # tolerance, so it must start below tolerance / e**(exponent * steps).
    digits = (steps * exponent - math.log(tolerance)) / math.log(10)
    return math.ceil(digits - 1e-9)
