"""Lab 14.1 -- a chance of rain, and keeping score.

An ensemble forecast is a list of members, and at your town each member
either rains or it does not. `chance` turns the list into a probability.
`hit_rate` is how a probability forecast is judged: gather many
forecasts, keep the ones that gave about the same chance, and count how
often it then rained.
"""

State = tuple[float, ...]


def chance(members: list[State], level: float, site: int = 0) -> float:
    """The fraction of the members whose number at `site` is above
    `level` (strictly above: a member exactly at the level is dry)."""
    raise NotImplementedError("your turn: replace this line")


def hit_rate(chances: list[float], rained: list[bool],
             low: float, high: float) -> float:
    """Of the forecasts whose chance lies between `low` and `high` (both
    ends included), the fraction after which it rained. `rained[k]` says
    whether it rained after forecast k. Raise ValueError if no forecast
    lies in that range: a score of nothing is not a score."""
    raise NotImplementedError("your turn: replace this line")
