"""Chapter 1 -- a cup of tea cooling, one minute at a time.

A model that steps: the rule does not say where the temperature will be at
any time you like; it says how to get from this minute to the next one.
"""
# transcript: ch01-cooling-cup

# --8<-- [start:rule]
ROOM = 20.0   # degrees Celsius
K = 0.1       # the fraction of the gap to the room lost each minute


def next_minute(temp: float) -> float:
    """The temperature one minute later."""
    return temp - K * (temp - ROOM)
# --8<-- [end:rule]


def main() -> None:
# --8<-- [start:run]
    temp = 90.0
    for minute in range(31):
        if minute % 5 == 0:
            print(f"minute {minute:2d}: {temp:5.1f} C")
        temp = next_minute(temp)
# --8<-- [end:run]


if __name__ == "__main__":
    main()
