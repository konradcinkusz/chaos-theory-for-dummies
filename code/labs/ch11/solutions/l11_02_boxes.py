"""Reference solution for Lab 11.2."""

import math

from chaoslab import fit_slope


def count_boxes(points: list[tuple[float, float]], size: float) -> int:
    """How many squares of side `size` hold at least one of the points."""
    return len({(math.floor(x / size), math.floor(y / size))
                for x, y in points})


def box_dimension(points: list[tuple[float, float]],
                  sizes: list[float]) -> float:
    """The slope of ln N against ln(1/s) over the given box sizes."""
    xs = [math.log(1 / s) for s in sizes]
    ys = [math.log(count_boxes(points, s)) for s in sizes]
    return fit_slope(xs, ys)
