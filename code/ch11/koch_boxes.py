"""Chapter 11 -- the box-counting dimension of the Koch curve.

Cover the curve with a grid of squares of side s, count the squares it
touches, halve s and count again. The boxes are powers of two on purpose:
the Koch curve is built in thirds, and a measurement that knew that would
be less of a test.
"""
# transcript: ch11-koch-boxes

from __future__ import annotations

import math

from chaoslab import box_count, fit_slope, koch

POINTS = koch(8)                       # 65,537 corners
SIZES = [1 / 2**k for k in range(1, 11)]


def counts(points: list[tuple[float, float]],
           sizes: list[float]) -> list[int]:
    """How many boxes of each size the points touch."""
    return [box_count(points, s) for s in sizes]


def dimension(sizes: list[float], ns: list[int]) -> float:
    """The slope of ln N against ln(1/s): the box-counting dimension."""
    xs = [math.log(1 / s) for s in sizes]
    ys = [math.log(n) for n in ns]
    return fit_slope(xs, ys)


def main() -> None:
# --8<-- [start:count]
    ns = counts(POINTS, SIZES)
    print("  box side     boxes   times as many as the row above")
    for k, (s, n) in enumerate(zip(SIZES, ns, strict=True)):
        line = f"  1/{round(1 / s):<6d} {n:8d}"
        if k:
            line += f"   {n / ns[k - 1]:.2f}"
        print(line)
    print(f"slope of ln N against ln(1/s): {dimension(SIZES, ns):.3f}")
    print(f"ln 4 / ln 3:                   {math.log(4) / math.log(3):.3f}")
# --8<-- [end:count]


if __name__ == "__main__":
    main()
