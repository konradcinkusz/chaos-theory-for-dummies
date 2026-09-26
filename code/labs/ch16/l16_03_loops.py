"""Lab 16.3 -- every orbit on a computer ends in a loop.

A computer holds finitely many numbers, so an orbit on it must, sooner or
later, meet a value it has met before -- and from then on it goes round the
same loop for ever. Write a linear congruential generator, the simplest
kind of random-number generator, and a function that finds where any orbit
enters its loop and how long the loop is.
"""

from collections.abc import Callable


def lcg(a: int, c: int, m: int) -> Callable[[int], int]:
    """The rule x -> (a*x + c) mod m, as a function of x."""
    raise NotImplementedError("your turn: replace this line")


def find_loop(rule: Callable, x0) -> tuple[int, int]:
    """(steps before the loop, length of the loop) for the orbit of x0.

    Hint: keep a dictionary from each value to the step at which you first
    saw it. The first value you see twice tells you both numbers.
    """
    raise NotImplementedError("your turn: replace this line")
