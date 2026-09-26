"""Reference solution for Lab 11.1."""

import math


def cantor(rounds: int) -> list[tuple[float, float]]:
    """The pieces (start, end) left after `rounds` rounds, left to right."""
    pieces = [(0.0, 1.0)]
    for _ in range(rounds):
        nxt = []
        for a, b in pieces:
            third = (b - a) / 3
            nxt += [(a, a + third), (b - third, b)]
        pieces = nxt
    return pieces


def length_left(rounds: int) -> float:
    """The total length of the pieces after `rounds` rounds."""
    return sum(b - a for a, b in cantor(rounds))


def similarity_dimension(copies: int, shrink: float) -> float:
    """The D for which shrink ** D == copies."""
    return math.log(copies) / math.log(shrink)
