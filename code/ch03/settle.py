"""Chapter 3 -- where the crowding rule settles, and whether it stays.

A fixed point is a population the rule leaves unchanged. Whether the
population stays there depends on what one step does to a tiny nudge away
from it: the slope, measured by nudging with chaoslab's slope exactly as
in Chapter 2, and here applied to a curved rule at its fixed points.
"""
# transcript: ch03-settle

from crowding import next_gen

from chaoslab import slope


# --8<-- [start:measure]
def slope_at(x: float, r: float) -> float:
    """The slope of the crowding rule at x, measured by nudging."""
    return slope(lambda y: next_gen(y, r), x)


def main() -> None:
    for r in (1.5, 2.0):
        for x in (0.0, 1 - 1 / r):
            print(f"r = {r}: at x = {x:.4f} the slope is"
                  f" {slope_at(x, r):6.3f}")
# --8<-- [end:measure]


if __name__ == "__main__":
    main()
