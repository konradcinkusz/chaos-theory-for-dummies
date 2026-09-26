"""Chapter 10 -- what one step of Henon's map does to an area.

A small square of starting points is represented by its outline: thousands
of points round its edge. Each step moves every one of them. The area inside
the outline is measured with the surveyor's shoelace formula, and the length
of the outline by adding up the little straight pieces between neighbours.
"""
# transcript: ch10-area

import math

from henon import B, henon

Point = tuple[float, float]


def outline(side: float, per_edge: int) -> list[Point]:
    """Points round the edge of a square of this side, centred on (0, 0)."""
    h = side / 2
    ts = [-h + side * k / per_edge for k in range(per_edge)]
    return ([(t, -h) for t in ts] + [(h, t) for t in ts]
            + [(-t, h) for t in ts] + [(-h, -t) for t in ts])


def area(points: list[Point]) -> float:
    """The area inside a closed outline (the shoelace formula)."""
    total = 0.0
    for (x1, y1), (x2, y2) in zip(points, points[1:] + points[:1],
                                  strict=True):
        total += x1 * y2 - x2 * y1
    return abs(total) / 2


def length(points: list[Point]) -> float:
    """The length of a closed outline: the sum of its little pieces."""
    total = 0.0
    for (x1, y1), (x2, y2) in zip(points, points[1:] + points[:1],
                                  strict=True):
        total += math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
    return total


def main() -> None:
    # --8<-- [start:area]
    edge = outline(0.1, 4000)            # a square a tenth on a side
    area0, length0 = area(edge), length(edge)
    print("step   area / start   0.3 ** step   outline / start")
    for step in range(1, 7):
        edge = [henon(x, y) for x, y in edge]
        print(f"{step:4d}  {area(edge) / area0:13.5f}  "
              f"{B ** step:12.5f}  {length(edge) / length0:16.2f}")
    # --8<-- [end:area]


if __name__ == "__main__":
    main()
