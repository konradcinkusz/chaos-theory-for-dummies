"""Lab 5.1 -- where the steady state lets go.

The logistic map x -> r*x*(1 - x) has a fixed point other than zero, which
the chapter found by algebra. Whether it HOLDS is a measurement: nudge x a
tiny amount each way, take one step, and see how much the nudge has been
multiplied. That multiplier is the slope of the rule there. The fixed point
holds when the slope lies strictly between -1 and 1.

Write the four functions below, in order; each one uses the one before.
"""


def fixed_point(r: float) -> float:
    """The value, other than zero, that r*x*(1 - x) leaves unchanged."""
    raise NotImplementedError("your turn: replace this line")


def slope_at(r: float, x: float, h: float = 1e-6) -> float:
    """How much one step of the map multiplies a tiny nudge at x.

    Nudge x by h to each side, take one step from each, and divide how far
    apart the two answers are by how far apart the two starts were (2*h).
    """
    raise NotImplementedError("your turn: replace this line")


def holds(r: float) -> bool:
    """True when a nudge at the fixed point shrinks, step after step."""
    raise NotImplementedError("your turn: replace this line")


def lets_go(lo: float, hi: float, tol: float = 1e-9) -> float:
    """The r between lo and hi at which the fixed point stops holding.

    holds(lo) is True and holds(hi) is False. Try the middle of the
    interval, keep the half in which the answer changes, and repeat until
    the interval is shorter than tol.
    """
    raise NotImplementedError("your turn: replace this line")
