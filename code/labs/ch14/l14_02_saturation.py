"""Lab 14.2 -- when does the ensemble stop spreading?

At first the members of an ensemble agree, and their spread grows. Later
they disagree about as much as two unrelated days of weather, and the
spread levels off. The level it settles at is the plateau. Write
`spread`, then `saturation_lead`: the first lead at which the spread has
reached a given fraction of its plateau.
"""

State = tuple[float, ...]


def spread(members: list[State]) -> float:
    """How far the members typically sit from their mean. For every site
    take the members' average; square each member's distance from that
    average; average those squares over every member and every site;
    and take the square root."""
    raise NotImplementedError("your turn: replace this line")


def saturation_lead(leads: list[float], spreads: list[float],
                    fraction: float = 0.9) -> float:
    """The first lead at which the spread is at least `fraction` of its
    plateau. The plateau is the average of the last quarter of the
    spreads (the last len(spreads) // 4 of them)."""
    raise NotImplementedError("your turn: replace this line")
