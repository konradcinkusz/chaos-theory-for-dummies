"""Chapter 3 -- turned up past three, the settling stops.

The settled level still exists; the population will not stay at it. A
nudge from it grows instead of dying away, and the population ends up
swinging between two values that are not the settled level at all.
"""
# transcript: ch03-two-cycle

from crowding import next_gen
from overshoot import compare


def main() -> None:
    # --8<-- [start:nudge]
    r = 3.1
    level = 1 - 1 / r
    x = level + 0.001
    for gen in range(6):
        print(f"gen {gen}: {x - level:+.5f} from the settled level")
        x = next_gen(x, r)
    # --8<-- [end:nudge]
    print()
    # --8<-- [start:run]
    compare(3.1, range(60, 66))
    # --8<-- [end:run]


if __name__ == "__main__":
    main()
