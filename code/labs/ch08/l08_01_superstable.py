"""Lab 8.1 -- find a superstable landmark yourself.

A landmark is a value of r at which the top of the hump, x = 0.5, comes
back to exactly 0.5 after a given number of steps of the logistic map
x -> r*x*(1 - x). Write the three pieces: how far from the top you are after
`steps` steps, a bisection that finds where a function changes sign, and
the two put together. Use only + - * and /.
"""


def from_top(r: float, steps: int) -> float:
    """Start at x = 0.5 and apply r*x*(1 - x) `steps` times; return how far
    the result is from 0.5 (negative if it ended below 0.5)."""
    raise NotImplementedError("your turn: replace this line")


def bisect(g, lo: float, hi: float, rounds: int = 60) -> float:
    """A point between lo and hi where g changes sign. g(lo) and g(hi) have
    opposite signs; halve the interval `rounds` times, each time keeping the
    half whose ends still have opposite signs, and return its middle."""
    raise NotImplementedError("your turn: replace this line")


def superstable(steps: int, lo: float, hi: float) -> float:
    """The r between lo and hi at which 0.5 returns to 0.5 after `steps`."""
    raise NotImplementedError("your turn: replace this line")
