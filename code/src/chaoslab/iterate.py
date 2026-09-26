"""Iteration: a rule that turns this step's state into the next one's.

Everything in the first half of the book is this file. A rule is a function
`f`, a state is a number `x`, and the future is `x, f(x), f(f(x)), ...`.

Pure Python floats on purpose. Addition, subtraction, multiplication and
division are correctly rounded by the IEEE 754 standard, so the same rule
from the same start gives the same digits on every machine -- which matters
in a book about systems that amplify the last digit (Chapter 16 says why).
"""

from __future__ import annotations

from collections.abc import Callable

Rule = Callable[[float], float]


# --8<-- [start:orbit]
def orbit(f: Rule, x0: float, n: int) -> list[float]:
    """Apply the rule `f` n times to x0 and keep every state.

    The list has n + 1 entries: the start, then each step after it.
    """
    xs = [x0]
    for _ in range(n):
        xs.append(f(xs[-1]))
    return xs
# --8<-- [end:orbit]


# --8<-- [start:linear]
def linear(a: float, b: float) -> Rule:
    """The rule x -> a*x + b: interest, cooling, washing out, breeding."""

    def rule(x: float) -> float:
        return a * x + b

    return rule
# --8<-- [end:linear]


# --8<-- [start:logistic]
def logistic(r: float) -> Rule:
    """The logistic map x -> r*x*(1 - x), for x between 0 and 1."""

    def rule(x: float) -> float:
        return r * x * (1.0 - x)

    return rule
# --8<-- [end:logistic]


def logistic_slope(r: float) -> Rule:
    """How much the logistic map stretches a tiny nudge at x: r*(1 - 2x)."""

    def slope(x: float) -> float:
        return r * (1.0 - 2.0 * x)

    return slope


# --8<-- [start:slope]
def slope(f: Rule, x: float, h: float = 1e-6) -> float:
    """Measure how much f multiplies a tiny nudge at x.

    Nudge x a little to each side and see how far the output moves. No
    calculus is needed to read this: it is the stretch factor of one step.
    """
    return (f(x + h) - f(x - h)) / (2.0 * h)
# --8<-- [end:slope]


# --8<-- [start:cobweb]
def cobweb(f: Rule, x0: float, n: int) -> list[tuple[float, float]]:
    """The corners of the cobweb diagram for n steps of f from x0.

    Up (or down) to the curve, across to the diagonal, repeat: the path a
    pencil takes when you iterate a rule on its own graph.
    """
    points = [(x0, 0.0)]
    x = x0
    for _ in range(n):
        y = f(x)
        points.append((x, y))
        points.append((y, y))
        x = y
    return points
# --8<-- [end:cobweb]


# --8<-- [start:period]
def period(xs: list[float], tol: float = 1e-9,
           longest: int = 64) -> int | None:
    """The smallest p such that the tail of xs repeats every p steps.

    Returns None when no period up to `longest` fits -- which is what a
    chaotic orbit looks like, and also what a long period looks like, so
    None means "not found", never "proved chaotic".
    """
    tail = xs[-2 * longest:]
    for p in range(1, longest + 1):
        if all(abs(tail[i] - tail[i + p]) < tol
               for i in range(len(tail) - p)):
            return p
    return None
# --8<-- [end:period]
