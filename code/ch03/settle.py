"""Chapter 3 -- where the crowding rule settles, and whether it stays.

A fixed point is a population the rule leaves unchanged. Whether the
population stays there depends on what one step does to a tiny nudge away
from it, and that is measured here rather than worked out with calculus.
"""
# transcript: ch03-settle

from crowding import next_gen

# --8<-- [start:slope]
H = 1e-6  # the nudge: a millionth of the room


def slope_at(x: float, r: float) -> float:
    """How much one generation multiplies a tiny nudge at x: nudge x by H
    to each side and see how far apart the next generations land."""
    return (next_gen(x + H, r) - next_gen(x - H, r)) / (2 * H)
# --8<-- [end:slope]


def main() -> None:
    # --8<-- [start:table]
    for r in (1.5, 2.0):
        for x in (0.0, 1 - 1 / r):
            print(f"r = {r}: at x = {x:.4f} the slope is"
                  f" {slope_at(x, r):6.3f}")
    # --8<-- [end:table]


if __name__ == "__main__":
    main()
