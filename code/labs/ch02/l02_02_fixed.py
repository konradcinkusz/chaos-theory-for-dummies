"""Lab 2.2 -- where the rule stands still, and whether it stays there.

The rule is x -> a * x + b. A fixed point is a number the rule leaves
unchanged; it is stable when a small nudge away from it shrinks step by
step, and unstable when the nudge grows.
"""


def fixed_point(a: float, b: float) -> float:
    """The x with a * x + b == x. Raise ValueError when a == 1, where
    there is none (or, if b == 0, every x is one)."""
    raise NotImplementedError("your turn: replace this line")


def is_stable(a: float, b: float) -> bool:
    """True when a nudge away from the fixed point shrinks. Decide it by
    experiment if you like: start a little off the fixed point, take one
    step, and compare the gap before and after."""
    raise NotImplementedError("your turn: replace this line")


def steps_to_settle(a: float, b: float, x0: float, tol: float) -> int:
    """Steps from x0 until x is within `tol` of the fixed point. Raise
    ValueError if the fixed point is not stable: it would never happen."""
    raise NotImplementedError("your turn: replace this line")
