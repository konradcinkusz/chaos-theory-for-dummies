"""Lab 8.2 -- Feigenbaum's ratio, and where the doublings end.

You are given a list of landmarks, one for each period 1, 2, 4, 8, ... in
order. The gaps between neighbours shrink. Write `ratios`, which divides
each gap by the next one, and `where_it_ends`, which adds up every gap
still to come, on the assumption that each is the one before divided by the
last ratio you measured.
"""


def ratios(landmarks: list[float]) -> list[float]:
    """For landmarks a, b, c, d, ...: [(b - a)/(c - b), (c - b)/(d - c), ...].
    The list is two shorter than `landmarks`."""
    raise NotImplementedError("your turn: replace this line")


def where_it_ends(landmarks: list[float]) -> float:
    """The last landmark plus every gap still to come. With the last gap g
    and the last ratio d, those gaps are g/d, g/d/d, ..., and they add up
    to g/(d - 1)."""
    raise NotImplementedError("your turn: replace this line")
