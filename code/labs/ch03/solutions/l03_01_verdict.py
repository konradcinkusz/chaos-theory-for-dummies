"""Reference solution for Lab 3.1."""

from chaoslab import logistic, slope


def fixed_points(r: float) -> list[float]:
    """The two fixed points of the crowding rule, smaller first."""
    return sorted([0.0, 1 - 1 / r])


def level_slope(r: float) -> float:
    """The slope of the crowding rule at its settled level 1 - 1/r."""
    return slope(logistic(r), 1 - 1 / r)


def verdict(r: float) -> str:
    """What the settled level does to a population nudged off it."""
    s = level_slope(r)
    if abs(s) >= 1:
        return "pushed away"
    if s < 0:
        return "swings in"
    return "creeps in"
