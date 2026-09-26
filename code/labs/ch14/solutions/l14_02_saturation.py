"""Reference solution for Lab 14.2."""

import math

State = tuple[float, ...]


def spread(members: list[State]) -> float:
    """How far the members typically sit from their mean."""
    m, n = len(members), len(members[0])
    centre = [sum(state[i] for state in members) / m for i in range(n)]
    total = 0.0
    for state in members:
        for x, c in zip(state, centre, strict=True):
            total += (x - c) * (x - c)
    return math.sqrt(total / (m * n))


def saturation_lead(leads: list[float], spreads: list[float],
                    fraction: float = 0.9) -> float:
    """The first lead at which the spread is at least `fraction` of its
    plateau, the average of the last quarter of the spreads."""
    tail = spreads[-(len(spreads) // 4):]
    plateau = sum(tail) / len(tail)
    for lead, s in zip(leads, spreads, strict=True):
        if s >= fraction * plateau:
            return lead
    raise ValueError("the spread never reached its plateau")
