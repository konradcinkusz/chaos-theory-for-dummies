"""Chapter 1 -- the falling stone, the first model in the book.

The state is one number (how long the stone has been falling), the rule is
one formula, and the prediction is a table.
"""
# transcript: ch01-falling-stone

# --8<-- [start:model]
G = 9.81  # metres per second, per second, near the Earth's surface


def distance(t: float) -> float:
    """How far a dropped stone has fallen after t seconds, air ignored."""
    return 0.5 * G * t * t
# --8<-- [end:model]


def main() -> None:
    # --8<-- [start:table]
    print(" t (s)   fallen (m)")
    for t in range(6):
        print(f"{t:5d}   {distance(t):10.2f}")
    # --8<-- [end:table]


if __name__ == "__main__":
    main()
