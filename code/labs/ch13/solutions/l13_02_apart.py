"""Reference solution for Lab 13.2."""

from __future__ import annotations

from chaoslab import double_pendulum, rk4_step


def seconds_until_apart(first: tuple[float, ...],
                        second: tuple[float, ...],
                        tol: float = 0.1, dt: float = 0.001,
                        limit: float = 30.0) -> float | None:
    """Seconds until the two pendulums differ by more than tol, or None."""
    rule = double_pendulum()
    a, b = first, second
    for step in range(1, round(limit / dt) + 1):
        a, b = rk4_step(rule, a, dt), rk4_step(rule, b, dt)
        if max(abs(a[0] - b[0]), abs(a[1] - b[1])) > tol:
            return step * dt
    return None
