"""Measurements: turning "it is sensitive" and "it is a fractal" into numbers.

Chapters 6 and 7 measure how fast nearby starts separate; Chapter 11
measures a dimension. Each function here is short enough to read in one go,
because a measurement you cannot read is one you cannot trust.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Iterable

from .flows import Field, State, Stepper, rk4_step

Rule = Callable[[float], float]


# --8<-- [start:separation]
def separation(f: Rule, x0: float, delta: float, n: int) -> list[float]:
    """Run two copies of f from x0 and x0 + delta; return their distance
    after each of n steps (the first entry is delta itself)."""
    a, b = x0, x0 + delta
    gaps = [abs(b - a)]
    for _ in range(n):
        a, b = f(a), f(b)
        gaps.append(abs(b - a))
    return gaps
# --8<-- [end:separation]


# --8<-- [start:apart]
def steps_until_apart(f: Rule, x0: float, delta: float, tol: float,
                      limit: int = 10_000) -> int:
    """The first step at which two runs delta apart differ by more than tol."""
    a, b = x0, x0 + delta
    for n in range(1, limit + 1):
        a, b = f(a), f(b)
        if abs(b - a) > tol:
            return n
    raise RuntimeError(f"still within {tol} after {limit} steps")
# --8<-- [end:apart]


# --8<-- [start:lyapunov]
def lyapunov(f: Rule, stretch: Rule, x0: float, n: int,
             burn: int = 1000) -> float:
    """The average of log|stretch| along an orbit of f: the Lyapunov exponent.

    `stretch(x)` is how much one step multiplies a tiny nudge at x. The
    first `burn` steps are thrown away so the orbit has settled onto
    wherever it is going before anything is averaged.
    """
    x = x0
    for _ in range(burn):
        x = f(x)
    total = 0.0
    for _ in range(n):
        total += math.log(abs(stretch(x)))
        x = f(x)
    return total / n
# --8<-- [end:lyapunov]


# --8<-- [start:horizon]
def horizon(exponent: float, error: float, tolerance: float) -> float:
    """Steps (or time) until an error of size `error` grows to `tolerance`,
    if it grows by the factor e**exponent per step."""
    return math.log(tolerance / error) / exponent
# --8<-- [end:horizon]


def _distance(a: State, b: State) -> float:
    return math.sqrt(sum((x - y) * (x - y) for x, y in zip(a, b, strict=True)))


# --8<-- [start:flowexp]
def lyapunov_flow(field: Field, state: State, dt: float, steps: int,
                  delta: float = 1e-8, burn: int = 1000,
                  stepper: Stepper = rk4_step) -> float:
    """The largest Lyapunov exponent of a flow, per unit of time.

    Follow two runs delta apart; after every step measure how far apart
    they have drifted, add the log of the growth, and pull the second run
    back to distance delta along the same direction. Pulling back is what
    keeps the gap small enough to measure the stretching rather than the
    size of the attractor.
    """
    for _ in range(burn):
        state = stepper(field, state, dt)
    other = (state[0] + delta,) + tuple(state[1:])
    total = 0.0
    for _ in range(steps):
        state = stepper(field, state, dt)
        other = stepper(field, other, dt)
        d = _distance(state, other)
        total += math.log(d / delta)
        other = tuple(s + (o - s) * delta / d
                      for s, o in zip(state, other, strict=True))
    return total / (steps * dt)
# --8<-- [end:flowexp]


# --8<-- [start:boxes]
def box_count(points: Iterable[tuple[float, float]], size: float) -> int:
    """How many squares of side `size` does the set touch?"""
    return len({(math.floor(x / size), math.floor(y / size))
                for x, y in points})
# --8<-- [end:boxes]


# --8<-- [start:fit]
def fit_slope(xs: list[float], ys: list[float]) -> float:
    """The slope of the straight line that best fits the points (least
    squares). A dimension is the slope of a log-log plot."""
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True))
    den = sum((x - mx) * (x - mx) for x in xs)
    return num / den
# --8<-- [end:fit]
