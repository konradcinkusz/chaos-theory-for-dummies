"""Lab 3.1 -- read a fixed point's fate off its slope.

Chapter 2 measured slopes by nudging, and chaoslab's `slope` does it for
any rule you hand it. chaoslab's `logistic(r)` is the crowding rule
x |-> r * x * (1 - x). Measure its slope at the settled level 1 - 1/r and
turn the number into a verdict about a population that starts a little off
that level:

    "creeps in"    the nudge shrinks and keeps its side  (0 <= s < 1)
    "swings in"    it shrinks and changes side each time (-1 < s < 0)
    "pushed away"  it grows, whichever its side           (size of s >= 1)

The tests then run the rule for two thousand generations and check that
your verdict is what actually happens.
"""

from chaoslab import logistic, slope  # noqa: F401 -- you will need them


def fixed_points(r: float) -> list[float]:
    """The two fixed points of the crowding rule, smaller first: the empty
    place, and the level at which each individual is exactly replaced."""
    raise NotImplementedError("your turn: replace this line")


def level_slope(r: float) -> float:
    """The slope of the crowding rule at its settled level 1 - 1/r,
    measured with chaoslab's slope on chaoslab's logistic(r)."""
    raise NotImplementedError("your turn: replace this line")


def verdict(r: float) -> str:
    """"creeps in", "swings in" or "pushed away": what the settled level
    does to a population nudged a little off it, read from level_slope."""
    raise NotImplementedError("your turn: replace this line")
