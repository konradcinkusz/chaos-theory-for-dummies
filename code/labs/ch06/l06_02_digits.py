"""Lab 6.2 -- digits known, steps predicted.

Two numbers between 0 and 1 that share their first k binary digits stay on
the same side of one half for k steps of the doubling map, and not one step
more. Write both counts and check that they agree.

    shared_digits   compare the numbers digit by digit, without the map
    steps_together  run the map and watch which half each number is in

Hint for the first: int(x * 2**k) is the whole number made of the first k
binary digits of x, so two numbers share their first k digits exactly when
those whole numbers are equal.
"""

from chaoslab import doubling  # noqa: F401 -- you will need it


def shared_digits(a: float, b: float, limit: int = 50) -> int:
    """How many leading binary digits a and b have in common (at most
    limit)."""
    raise NotImplementedError("your turn: replace this line")


def steps_together(a: float, b: float, limit: int = 50) -> int:
    """How many steps of the doubling map keep a and b on the same side of
    one half (both below it, or both at or above it), at most limit."""
    raise NotImplementedError("your turn: replace this line")
