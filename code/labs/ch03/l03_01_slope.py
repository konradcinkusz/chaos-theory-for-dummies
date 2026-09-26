"""Lab 3.1 -- measure a slope, and let it tell you whether a fixed point
holds.

The chapter measured the slope of one rule, the crowding rule. Here you
write the measurement for ANY rule: `f` is a function, and f(x) is the
value one step after x. A fixed point is a value the rule leaves
unchanged; it is stable when a tiny nudge away from it shrinks, which for
a slope s means that s is between -1 and 1.
"""


def slope(f, x: float, h: float = 1e-6) -> float:
    """How much one step of f multiplies a tiny nudge at x.

    Nudge x by h to each side, run f on both, and divide how far apart
    the two answers land by how far apart the two starts were.
    """
    raise NotImplementedError("your turn: replace this line")


def fixed_points(r: float) -> list[float]:
    """The two fixed points of the crowding rule x -> r*x*(1 - x), smaller
    first: the empty place, and the level at which each individual is
    exactly replaced."""
    raise NotImplementedError("your turn: replace this line")


def is_stable(f, x: float) -> bool:
    """True when a tiny nudge away from the fixed point x of f shrinks."""
    raise NotImplementedError("your turn: replace this line")
