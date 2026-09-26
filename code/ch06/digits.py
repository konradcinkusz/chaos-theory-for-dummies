"""Chapter 6 -- the doubling map reads out the binary digits of its start.

Write a number between 0 and 1 in binary: 0.101 means one half, no
quarters, one eighth. The doubling map pushes every digit one place to the
left and drops the one that crosses the point, so whether the number is in
the upper half at step n is the digit n + 1 places after the point.
"""
# transcript: ch06-digits

from twins import NUDGE, START

from chaoslab import doubling


# --8<-- [start:digits]
def binary_digits(x: float, n: int) -> str:
    """The first n binary digits of x after the point.

    x * 2**n moves the point n places right, int() drops what is left
    over, and format(..., "b") writes the whole number in binary.
    """
    return format(int(x * 2**n), f"0{n}b")


def sides(x: float, n: int) -> str:
    """Run the doubling map n steps: 1 in the upper half, 0 in the lower."""
    out = ""
    for _ in range(n):
        out += "1" if x >= 0.5 else "0"
        x = doubling(x)
    return out
# --8<-- [end:digits]


def main() -> None:
    for x in (START, START + NUDGE):
        print(f"digits of {x:.10f}: {binary_digits(x, 40)}")
        print(f"doubling map sides: {sides(x, 40)}")


if __name__ == "__main__":
    main()
