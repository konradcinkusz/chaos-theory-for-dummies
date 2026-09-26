"""Chapter 2 -- the slope of a rule, measured by nudging.

The slope at a point is how far the output moves for each unit the input
moves. chaoslab.slope measures it: nudge x a millionth either way, see how
far the output moved, and divide by how far the input moved.
"""
# transcript: ch02-slope

from chaoslab import linear, slope

# --8<-- [start:measure]
tablets = linear(0.5, 100.0)    # a straight line


def square(x: float) -> float:
    """A curved rule: x times itself."""
    return x * x


def main() -> None:
    for x in (0.0, 150.0, 400.0):
        print(f"line   at x = {x:5.1f}: slope {slope(tablets, x):.4f}")
    for x in (0.5, 1.5, 3.0):
        print(f"square at x = {x:5.1f}: slope {slope(square, x):.4f}")
# --8<-- [end:measure]


if __name__ == "__main__":
    main()
