"""Lab 11.1 -- the Cantor set, and its dimension from counting copies.

Start with the line from 0 to 1. Every round, cut every piece into three
equal parts and throw away the middle one. Write the rule, measure the
length that is left, and turn "two copies, each a third the size" into a
dimension.
"""


def cantor(rounds: int) -> list[tuple[float, float]]:
    """The pieces (start, end) left after `rounds` rounds, left to right.

    cantor(0) is [(0.0, 1.0)]; cantor(1) is [(0.0, 1/3), (2/3, 1.0)].
    """
    raise NotImplementedError("your turn: replace this line")


def length_left(rounds: int) -> float:
    """The total length of the pieces after `rounds` rounds."""
    raise NotImplementedError("your turn: replace this line")


def similarity_dimension(copies: int, shrink: float) -> float:
    """The D for which shrink ** D == copies.

    A shape made of `copies` copies of itself, each shrunk by the factor
    `shrink`, has this dimension. A square is 9 copies shrunk by 3, so the
    answer for (9, 3) is 2. Use math.log.
    """
    raise NotImplementedError("your turn: replace this line")
