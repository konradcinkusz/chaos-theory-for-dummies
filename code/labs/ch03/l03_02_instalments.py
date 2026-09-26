"""Lab 3.2 -- the same law of growth, applied late and applied often.

Over one generation the crowding rule changes the population by
next_gen(x, r) - x. Applied all at once, that is the rule of the chapter.
Applied in k equal instalments, each worked out from the population as it
stands after the one before, it is the same law reacting k times as often.
Write both and find out which one overshoots.
"""


def next_gen(x: float, r: float) -> float:
    """The crowding rule: r * x times the share of room still free."""
    raise NotImplementedError("your turn: replace this line")


def in_instalments(x: float, r: float, k: int) -> float:
    """One generation of the crowding rule, paid in k instalments."""
    raise NotImplementedError("your turn: replace this line")


def run(r: float, k: int, x0: float, generations: int) -> list[float]:
    """The population at the end of each generation, starting with x0:
    generations + 1 values. Each generation is paid in k instalments, so
    k = 1 is the chapter's rule applied once a generation."""
    raise NotImplementedError("your turn: replace this line")


def overshoots(r: float, k: int, x0: float = 0.01,
               generations: int = 100) -> bool:
    """True if, over `generations` generations from x0, the population is
    ever above its settled level 1 - 1/r by more than a millionth."""
    raise NotImplementedError("your turn: replace this line")
