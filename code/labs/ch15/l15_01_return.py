"""Lab 15.1 -- a return-map test: curve or cloud?

Plot each value of a series against the next. A series made by a rule
lands on the graph of that rule, a curve; shuffled numbers spread over the
whole square. Turn the picture into a test a program can run: cut the unit
square into k by k little squares and count how many the pairs land in.
"""


def return_pairs(xs: list[float]) -> list[tuple[float, float]]:
    """Each value paired with the one after it: (x0, x1), (x1, x2), ..."""
    raise NotImplementedError("your turn: replace this line")


def squares_touched(xs: list[float], k: int = 10) -> int:
    """How many of the k by k little squares the return map lands in.

    The square for a value v is number int(v * k) along its side, except
    that a value of 1 or more belongs to the last one (k - 1) and a value
    below 0 to the first (0).
    """
    raise NotImplementedError("your turn: replace this line")


def verdict(xs: list[float], k: int = 10) -> str:
    """"curve" if the return map lands in fewer than half of the k * k
    squares, "cloud" otherwise."""
    raise NotImplementedError("your turn: replace this line")
