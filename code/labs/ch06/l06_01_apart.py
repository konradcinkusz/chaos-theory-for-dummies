"""Lab 6.1 -- when do two runs part company?

Run one rule from two starts, a and b, side by side. `gaps` keeps the
distance between the two runs at every step; `first_apart` answers the
question a forecaster asks: at which step does the forecast stop being good
enough? Both take the rule as a function, so they work for Chapter 1's tea
as well as for the logistic map. Step 0 is the two starts themselves.
"""

from collections.abc import Callable

Rule = Callable[[float], float]


def gaps(rule: Rule, a: float, b: float, steps: int) -> list[float]:
    """The distance between the two runs at step 0, 1, ..., steps.

    The distance is always positive: use abs(). The list has steps + 1
    entries.
    """
    raise NotImplementedError("your turn: replace this line")


def first_apart(rule: Rule, a: float, b: float, tol: float,
                limit: int = 1000) -> int | None:
    """The first step at which the two runs differ by more than tol.

    Return None if they are still within tol after `limit` steps.
    """
    raise NotImplementedError("your turn: replace this line")
