"""Chapter 11 -- the Koch curve, built round by round, and measured.

Every round replaces each straight piece by four pieces a third as long.
The ruler that fits the curve after a round is the length of one piece, so
measuring the round-n curve IS measuring the Koch curve with a ruler of
length 1/3**n. The height and the area show how much room it all takes.
"""
# transcript: ch11-koch-length

from __future__ import annotations

from itertools import pairwise

from _ruler import Point, length

from chaoslab import koch


def area(points: list[Point]) -> float:
    """The area between the curve and the straight line under it.

    The shoelace formula: walk round the outline, adding x*y' - x'*y for
    each step, and halve. The walk goes clockwise, so the sum comes out
    negative; its size is the area.
    """
    loop = points + [points[0]]
    total = 0.0
    for (x0, y0), (x1, y1) in pairwise(loop):
        total += x0 * y1 - x1 * y0
    return abs(total) / 2


def main() -> None:
    # --8<-- [start:table]
    print("round  pieces    ruler   length   height     area")
    for n in range(7):
        pts = koch(n)
        pieces = len(pts) - 1
        ruler = 1 / 3**n
        height = max(y for x, y in pts)
        print(f"{n:5d}  {pieces:6d}  {ruler:7.5f}  {length(pts):7.3f}"
              f"  {height:7.4f}  {area(pts):7.4f}")
# --8<-- [end:table]


if __name__ == "__main__":
    main()
