"""Chapter 12 -- a point of the plane as a number, and how to multiply two.

The rule by hand uses nothing but i * i = -1. Python's built-in complex type
does the same arithmetic, and writes i as 1j, the engineers' spelling.
"""
# transcript: ch12-complex

import cmath
import math


# --8<-- [start:times]
def times(a: float, b: float, c: float, d: float) -> tuple[float, float]:
    """(a + b i) times (c + d i): multiply out, then use i * i = -1."""
    return a * c - b * d, a * d + b * c
# --8<-- [end:times]


def degrees(z: complex) -> float:
    """The angle of z, turned anticlockwise from the positive real axis."""
    return math.degrees(cmath.phase(z))


def main() -> None:
# --8<-- [start:check]
    print("i times i, by hand:  ", times(0, 1, 0, 1))
    print("i times i, by Python:", 1j * 1j)
    z = 3 + 4j
    print("(3+4i)^2, by hand:   ", times(3, 4, 3, 4))
    print("(3+4i)^2, by Python: ", z * z)
    print(f"lengths: {abs(z)} and {abs(z * z)}")
    print(f"angles:  {degrees(z):.2f} and {degrees(z * z):.2f} degrees")
# --8<-- [end:check]


if __name__ == "__main__":
    main()
