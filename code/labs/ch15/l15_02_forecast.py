"""Lab 15.2 -- a forecaster that asks several analogues.

The chapter's forecaster finds the one past value most like now and says
that what followed it then will follow now. With noise in the record, the
single closest analogue may be close by accident. Ask several instead: find
the `count` closest past values and average what came after them.
"""


def nearest(library: list[float], x: float, count: int,
            h: int) -> list[int]:
    """The positions j of the `count` values closest to x, closest first,
    among the positions that have a value h steps after them (that is,
    j from 0 up to len(library) - h - 1)."""
    raise NotImplementedError("your turn: replace this line")


def forecast(library: list[float], x: float, h: int,
             count: int = 1) -> float:
    """The average of library[j + h] over the `count` nearest positions."""
    raise NotImplementedError("your turn: replace this line")


def mean_error(xs: list[float], h: int, split: int,
               count: int = 1) -> float:
    """The average size of the miss h steps ahead, learning from
    xs[:split] and testing on every value after it that has a value h
    steps later."""
    raise NotImplementedError("your turn: replace this line")
