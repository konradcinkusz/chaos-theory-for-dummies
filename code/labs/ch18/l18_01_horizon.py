"""Lab 18.1 -- the horizon calculator.

If an error is multiplied by the factor e**exponent every step, it grows
from `error` to `tolerance` in ln(tolerance / error) / exponent steps. Write
three functions that turn that one line into the answers people actually
want: how far ahead, what better data would buy, and how good the data
would have to be.

Use math.log (the natural logarithm, ln) and math.ceil.
"""

import math  # noqa: F401 -- you will need it


def forecast_length(exponent: float, digits: int,
                    tolerance: float = 0.1) -> float:
    """Steps before the forecast's error exceeds `tolerance`, when the start
    is right to `digits` decimal places (an error of 10**-digits)."""
    raise NotImplementedError("your turn: replace this line")


def extra_steps(exponent: float, factor: float) -> float:
    """How many more steps a measurement `factor` times as precise buys."""
    raise NotImplementedError("your turn: replace this line")


def digits_needed(exponent: float, steps: int,
                  tolerance: float = 0.1) -> int:
    """The fewest correct decimal places in the start for the forecast to
    stay within `tolerance` for `steps` steps (a whole number)."""
    raise NotImplementedError("your turn: replace this line")
