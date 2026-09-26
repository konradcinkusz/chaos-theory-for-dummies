"""Lab 1.2 -- the cooling cup, as a model you can ask questions.

`cool` runs the chapter's rule and keeps every minute; `minutes_until`
answers the question a person actually asks: how long until I can drink it?
The rule, from the chapter: each minute the tea loses the fraction k of the
gap between itself and the room.
"""


def cool(start: float, room: float, k: float, minutes: int) -> list[float]:
    """Temperatures at minute 0, 1, ..., minutes (minutes + 1 values)."""
    raise NotImplementedError("your turn: replace this line")


def minutes_until(start: float, room: float, k: float,
                  target: float) -> int:
    """The first whole minute at which the tea is below `target`."""
    raise NotImplementedError("your turn: replace this line")
