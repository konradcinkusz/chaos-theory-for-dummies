"""Chapter 10 -- a cloud of starting points, and where they all end up.

A grid of 1600 starts covers a square around the origin. After a few steps
some have left for good and every one of the rest sits on the same thin set
that a single long run of the map draws. "On the set" is decided the plain
way: one long run marks every little square it ever visits.
"""
# transcript: ch10-cloud

import math

from henon import henon

CELL = 0.01           # side of the little squares the long run marks
REFERENCE = 500_000   # steps in that long run


def square_of(x: float, y: float) -> tuple[int, int]:
    """Which little square the point (x, y) is in."""
    return math.floor(x / CELL), math.floor(y / CELL)


# --8<-- [start:cloud]
def marked_squares() -> set[tuple[int, int]]:
    """Every little square that one long run of the map visits."""
    x, y = 0.0, 0.0
    for _ in range(1000):                  # let it settle first
        x, y = henon(x, y)
    marked = set()
    for _ in range(REFERENCE):
        x, y = henon(x, y)
        marked.add(square_of(x, y))
    return marked


def main() -> None:
    marked = marked_squares()
    cloud = [(-0.5 + (i + 0.5) / 40, -0.5 + (j + 0.5) / 40)
             for i in range(40) for j in range(40)]
    start = len(cloud)
    print("step  left for good  on the attractor")
    for step in range(31):
        if step in (0, 1, 2, 3, 5, 10, 20, 30):
            on = sum(square_of(x, y) in marked for x, y in cloud)
            print(f"{step:4d}  {start - len(cloud):13d}  "
                  f"{on:6d} of {len(cloud)}")
        cloud = [henon(x, y) for x, y in cloud]
        cloud = [(x, y) for x, y in cloud if abs(x) + abs(y) < 10]
# --8<-- [end:cloud]


if __name__ == "__main__":
    main()
