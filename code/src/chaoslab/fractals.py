"""Fractals: shapes built by repeating one rule at smaller and smaller sizes,
and the escape-time pictures of Chapter 12.

Complex numbers here are Python's built-in `complex`: 2 + 3j is the point two
across and three up, and multiplication is done by the rule Chapter 12
derives. Only +, -, * on floats, so every pixel is the same on every machine.
"""

from __future__ import annotations

import math

Point = tuple[float, float]


# --8<-- [start:cantor]
def cantor(level: int) -> list[tuple[float, float]]:
    """The intervals left after removing middle thirds `level` times."""
    pieces = [(0.0, 1.0)]
    for _ in range(level):
        nxt = []
        for a, b in pieces:
            third = (b - a) / 3
            nxt += [(a, a + third), (b - third, b)]
        pieces = nxt
    return pieces
# --8<-- [end:cantor]


# --8<-- [start:koch]
def koch(level: int) -> list[Point]:
    """The corners of the Koch curve from (0, 0) to (1, 0) after `level`
    rounds of replacing every segment's middle third with a tent."""
    h = math.sqrt(3.0) / 2.0   # height of a unit equilateral triangle
    pts = [(0.0, 0.0), (1.0, 0.0)]
    for _ in range(level):
        nxt = [pts[0]]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:], strict=False):
            dx, dy = (x1 - x0) / 3, (y1 - y0) / 3
            a = (x0 + dx, y0 + dy)
            b = (x0 + 2 * dx, y0 + 2 * dy)
            # the tip: the middle third turned 60 degrees to the left
            tip = (a[0] + dx / 2 - h * dy, a[1] + dy / 2 + h * dx)
            nxt += [a, tip, b, (x1, y1)]
        pts = nxt
    return pts
# --8<-- [end:koch]


# --8<-- [start:escape]
def escape_time(c: complex, limit: int = 100, z: complex = 0j) -> int:
    """Iterate z -> z*z + c from z; return the step at which |z| exceeds 2,
    or `limit` if it never does. Once |z| > 2 it is gone for good."""
    for n in range(limit):
        if z.real * z.real + z.imag * z.imag > 4.0:
            return n
        z = z * z + c
    return limit
# --8<-- [end:escape]


# --8<-- [start:rtoc]
def r_to_c(r: float) -> float:
    """The logistic map at r is z -> z*z + c at this real c."""
    return r / 2 - r * r / 4
# --8<-- [end:rtoc]
