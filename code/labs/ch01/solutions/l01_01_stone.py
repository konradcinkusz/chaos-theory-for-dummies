"""Reference solution for Lab 1.1."""

import math

G = 9.81


def distance(t: float, g: float = G) -> float:
    """Metres fallen after t seconds."""
    return 0.5 * g * t * t


def fall_time(height: float, g: float = G) -> float:
    """Seconds to fall `height` metres."""
    return math.sqrt(2 * height / g)


def estimate_g(height: float, seconds: float) -> float:
    """The g that would make a stone fall `height` metres in `seconds`."""
    return 2 * height / (seconds * seconds)
