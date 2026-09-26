"""Chapter 18 -- the three exponents the horizon table is built from.

A helper, imported by horizon.py and by code/measure/ch18.py, so the page and
the listing measure the same thing. Each exponent is the average rate at
which a tiny difference grows, per step or per unit of time.

The trajectories themselves use only +, -, * , / and sqrt, so they are the
same on every machine; the logarithm is only ever added up, never fed back
into the motion, so the two-decimal averages below cannot move.
"""

from __future__ import annotations

import math

from chaoslab import logistic, logistic_slope, lorenz, lyapunov, lyapunov_flow


def logistic_exponent(r: float = 4.0, steps: int = 100_000) -> float:
    """Lyapunov exponent of the logistic map, per step."""
    return lyapunov(logistic(r), logistic_slope(r), 0.3, steps)


def henon_exponent(a: float = 1.4, b: float = 0.3,
                   steps: int = 100_000, burn: int = 1000) -> float:
    """Largest Lyapunov exponent of the Henon map, per step.

    A tiny arrow (vx, vy) rides along with the point. Each step stretches
    and turns it; its new length is the stretch, and it is shrunk back to
    length one so that it never overflows.
    """
    x, y = 0.1, 0.1
    for _ in range(burn):
        x, y = 1.0 - a * x * x + y, b * x
    vx, vy = 1.0, 0.0
    total = 0.0
    for _ in range(steps):
        vx, vy = -2.0 * a * x * vx + vy, b * vx
        length = math.sqrt(vx * vx + vy * vy)
        total += math.log(length)
        vx, vy = vx / length, vy / length
        x, y = 1.0 - a * x * x + y, b * x
    return total / steps


def lorenz_exponent(dt: float = 0.01, steps: int = 20_000) -> float:
    """Largest Lyapunov exponent of Lorenz's 1963 system, per unit time."""
    return lyapunov_flow(lorenz(), (1.0, 1.0, 1.0), dt, steps)
