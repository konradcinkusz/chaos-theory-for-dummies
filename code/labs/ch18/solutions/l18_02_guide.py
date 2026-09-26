"""Reference solution for Lab 18.2."""

import math
from collections.abc import Callable

Rule = Callable[[float], float]


def error_grows(rule: Rule, x0: float, delta: float = 1e-9,
                steps: int = 30) -> bool:
    """True if two runs delta apart end further apart than delta."""
    a, b = x0, x0 + delta
    for _ in range(steps):
        a, b = rule(a), rule(b)
    return abs(b - a) > delta


def growth_rate(rule: Rule, x0: float, delta: float = 1e-12,
                steps: int = 20) -> float:
    """ln(gap after `steps` / delta) / steps."""
    a, b = x0, x0 + delta
    for _ in range(steps):
        a, b = rule(a), rule(b)
    return math.log(abs(b - a) / abs((x0 + delta) - x0)) / steps


def long_run_fraction(rule: Rule, x0: float, low: float, high: float,
                      steps: int = 100_000) -> float:
    """The fraction of steps at which low <= x < high."""
    x, inside = x0, 0
    for _ in range(steps):
        if low <= x < high:
            inside += 1
        x = rule(x)
    return inside / steps


def tent(x: float) -> float:
    """A rule of my own: a tent with a slope of 1.9. (A slope of exactly 2
    collapses to zero on a computer, for the reason Chapter 16 gives.)"""
    return 1.9 * min(x, 1.0 - x)


if __name__ == "__main__":
    print(error_grows(tent, 0.3), round(growth_rate(tent, 0.3), 3),
          round(long_run_fraction(tent, 0.3, 0.0, 0.5), 2))
