"""Chapter 16 -- the doubling map on a computer, beside the truth.

x -> 2x mod 1 moves every binary digit one place to the left and throws
away the one that crosses the point. The computer's orbit of 0.1 is set
beside the true orbit of one tenth, worked in exact fractions.
"""
# transcript: ch16-doubling

from fractions import Fraction

from chaoslab import doubling


def exact_doubling(x: Fraction) -> Fraction:
    """The same rule on an exact fraction: double, drop the whole part."""
    y = 2 * x
    return y - 1 if y >= 1 else y


def main() -> None:
# --8<-- [start:race]
    x = 0.1                   # what the computer stores for one tenth
    t = Fraction(1, 10)       # one tenth itself
    for n in range(61):
        if n <= 5 or n in (40, 45, 50, 53, 54, 55, 60):
            print(f"step {n:2d}:  computer {x:.6f}   truth {float(t):.6f}")
        x, t = doubling(x), exact_doubling(t)
# --8<-- [end:race]


if __name__ == "__main__":
    main()
