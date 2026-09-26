"""Reference solution for Lab 13.1."""

import math

G = 9.81


def heights(state: tuple[float, ...]) -> tuple[float, float]:
    """The heights of the upper and lower bob above the pivot, in metres."""
    upper, lower = state[0], state[1]
    first = -math.cos(upper)
    return first, first - math.cos(lower)


def energy(state: tuple[float, ...]) -> float:
    """Kinetic plus potential energy of the pendulum, in joules."""
    upper, lower, w1, w2 = state
    h1, h2 = heights(state)
    v2_squared = w1 * w1 + w2 * w2 + 2 * w1 * w2 * math.cos(upper - lower)
    kinetic = 0.5 * w1 * w1 + 0.5 * v2_squared
    return kinetic + G * (h1 + h2)
