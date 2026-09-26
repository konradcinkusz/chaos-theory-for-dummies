"""Lab 16.2 -- single against double precision, on the logistic map.

A double keeps 53 significant binary digits; a single keeps 24. Python's
float is a double, but you can round any number to the nearest single by
packing it into the four bytes of a single and reading it back:

    struct.unpack("f", struct.pack("f", x))[0]

Run the logistic map at r = 4 both ways from the same start and find the
step at which the two runs first differ by more than a tolerance. The
chapter predicts roughly how many steps that will be; check it.
"""

import struct  # noqa: F401 -- you will need it


def to_single(x: float) -> float:
    """The nearest single-precision number to x."""
    raise NotImplementedError("your turn: replace this line")


def rule_single(x: float) -> float:
    """4x(1 - x), with 4x, 1 - x and their product each rounded to single."""
    raise NotImplementedError("your turn: replace this line")


def parting_step(x0: float, tol: float) -> int:
    """The first step n at which the double run 4x(1 - x) from x0 and the
    single run from to_single(x0) differ by more than tol."""
    raise NotImplementedError("your turn: replace this line")
