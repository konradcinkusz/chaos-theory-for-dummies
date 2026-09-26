"""Lab 11.2 -- box counting, the dimension of a shape nobody built by rule.

Lay a grid of squares of side `size` over the plane, with a corner at
(0, 0). A point (x, y) is in the square with column floor(x / size) and row
floor(y / size). The box count is how many different squares hold at least
one point. The dimension is the slope of ln N against ln(1/s).
"""


def count_boxes(points: list[tuple[float, float]], size: float) -> int:
    """How many squares of side `size` hold at least one of the points.

    Use math.floor, not int(): int(-0.5) is 0, which would put a point just
    left of 0 in the same column as a point just right of it.
    """
    raise NotImplementedError("your turn: replace this line")


def box_dimension(points: list[tuple[float, float]],
                  sizes: list[float]) -> float:
    """The slope of ln N against ln(1/s) over the given box sizes.

    Count the boxes at every size, take logarithms, and fit a straight line;
    `from chaoslab import fit_slope` does the fitting.
    """
    raise NotImplementedError("your turn: replace this line")
