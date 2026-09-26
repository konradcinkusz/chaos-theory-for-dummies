"""Reference solution for Lab 14.1."""

State = tuple[float, ...]


def chance(members: list[State], level: float, site: int = 0) -> float:
    """The fraction of the members whose number at `site` is above
    `level` (strictly above: a member exactly at the level is dry)."""
    wet = sum(1 for state in members if state[site] > level)
    return wet / len(members)


def hit_rate(chances: list[float], rained: list[bool],
             low: float, high: float) -> float:
    """Of the forecasts whose chance lies between `low` and `high` (both
    ends included), the fraction after which it rained."""
    kept = [r for p, r in zip(chances, rained, strict=True)
            if low <= p <= high]
    if not kept:
        raise ValueError(f"no forecast gave a chance in [{low}, {high}]")
    return sum(kept) / len(kept)
