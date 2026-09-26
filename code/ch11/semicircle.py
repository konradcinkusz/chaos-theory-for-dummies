"""Chapter 11 -- a smooth curve measured with shorter and shorter rulers.

Half a circle of radius one, from (1, 0) over the top to (-1, 0). Each round
puts a new point on the circle halfway between every pair of neighbours, so
the ruler -- the straight step between neighbours -- gets shorter. Only +,
-, *, / and square roots, so every digit is the same on every machine.
"""
# transcript: ch11-semicircle

from __future__ import annotations

import math
from itertools import pairwise

from _ruler import Point, length


def halve(points: list[Point]) -> list[Point]:
    """Put a new point on the circle halfway between each pair."""
    out = [points[0]]
    for (x0, y0), (x1, y1) in pairwise(points):
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        r = math.sqrt(mx * mx + my * my)   # push the midpoint out
        out += [(mx / r, my / r), (x1, y1)]  # onto the circle
    return out


def rounds(n: int) -> list[list[Point]]:
    """The points after 0, 1, ..., n rounds of halving."""
    pts = [(1.0, 0.0), (0.0, 1.0), (-1.0, 0.0)]
    out = [pts]
    for _ in range(n):
        pts = halve(pts)
        out.append(pts)
    return out


def main() -> None:
    # --8<-- [start:table]
    print(" steps    ruler    measured length")
    for pts in rounds(8):
        steps = len(pts) - 1
        ruler = length(pts[:2])       # one step, from the first point
        print(f"{steps:6d}   {ruler:.4f}   {length(pts):.5f}")
# --8<-- [end:table]


if __name__ == "__main__":
    main()
