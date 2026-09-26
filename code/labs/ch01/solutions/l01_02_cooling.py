"""Reference solution for Lab 1.2."""


def cool(start: float, room: float, k: float, minutes: int) -> list[float]:
    """Temperatures at minute 0, 1, ..., minutes (minutes + 1 values)."""
    temps = [start]
    for _ in range(minutes):
        t = temps[-1]
        temps.append(t - k * (t - room))
    return temps


def minutes_until(start: float, room: float, k: float,
                  target: float) -> int:
    """The first whole minute at which the tea is below `target`."""
    minute, t = 0, start
    while t >= target:
        t = t - k * (t - room)
        minute += 1
    return minute
