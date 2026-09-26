"""Reference solution for Lab 17.2."""

import math

from chaoslab import lorenz, rk4_step

SIGMA, RHO, BETA = 10.0, 28.0, 8.0 / 3.0


def start(dt: float = 0.01) -> tuple[float, ...]:
    """The original after 2000 steps from (1, 1, 1); the copy at zero."""
    s = (1.0, 1.0, 1.0)
    field = lorenz(SIGMA, RHO, BETA)
    for _ in range(2000):
        s = rk4_step(field, s, dt)
    return s + (0.0, 0.0)


def copy_field(s: tuple[float, ...]) -> tuple[float, ...]:
    """How fast each of (x, y, z, y2, z2) is changing, as five numbers."""
    x, y, z, y2, z2 = s
    return (SIGMA * (y - x),
            x * (RHO - z) - y,
            x * y - BETA * z,
            x * (RHO - z2) - y2,
            x * y2 - BETA * z2)


def error(s: tuple[float, ...]) -> float:
    """The distance between the copy (y2, z2) and the original's (y, z)."""
    dy, dz = s[3] - s[1], s[4] - s[2]
    return math.sqrt(dy * dy + dz * dz)


def sync_time(tol: float, dt: float = 0.01, limit: float = 100.0) -> float:
    """The first time, in steps of dt from `start`, at which error < tol."""
    s = start(dt)
    n = 0
    while error(s) >= tol:
        if n * dt > limit:
            raise RuntimeError(f"no agreement to {tol} by t = {limit}")
        s = rk4_step(copy_field, s, dt)
        n += 1
    return n * dt
