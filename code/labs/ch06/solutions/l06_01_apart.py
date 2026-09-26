"""Reference solution for Lab 6.1."""

from collections.abc import Callable

Rule = Callable[[float], float]


def gaps(rule: Rule, a: float, b: float, steps: int) -> list[float]:
    """The distance between the two runs at step 0, 1, ..., steps."""
    out = [abs(b - a)]
    for _ in range(steps):
        a, b = rule(a), rule(b)
        out.append(abs(b - a))
    return out


def first_apart(rule: Rule, a: float, b: float, tol: float,
                limit: int = 1000) -> int | None:
    """The first step at which the two runs differ by more than tol."""
    for n in range(limit + 1):
        if abs(b - a) > tol:
            return n
        a, b = rule(a), rule(b)
    return None
