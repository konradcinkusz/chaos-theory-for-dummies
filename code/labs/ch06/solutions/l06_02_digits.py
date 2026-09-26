"""Reference solution for Lab 6.2."""

from chaoslab import doubling


def shared_digits(a: float, b: float, limit: int = 50) -> int:
    """How many leading binary digits a and b have in common."""
    k = 0
    while k < limit and int(a * 2 ** (k + 1)) == int(b * 2 ** (k + 1)):
        k += 1
    return k


def steps_together(a: float, b: float, limit: int = 50) -> int:
    """Steps of the doubling map that keep a and b on the same side."""
    n = 0
    while n < limit and (a >= 0.5) == (b >= 0.5):
        a, b = doubling(a), doubling(b)
        n += 1
    return n
