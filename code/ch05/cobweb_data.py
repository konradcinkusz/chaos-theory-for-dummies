"""Chapter 5 -- the corners of a cobweb on the logistic map's hump.

Up to the curve, across to the diagonal, and again. Chaoslab's `cobweb`
returns the corners; this listing labels each one with the move that
reached it.
"""
# transcript: ch05-cobweb

# --8<-- [start:corners]
from chaoslab import cobweb, logistic


def main() -> None:
    corners = cobweb(logistic(2.8), 0.2, 3)       # three steps from 0.2
    moves = ["start"] + ["up", "across"] * 3
    for move, (x, y) in zip(moves, corners, strict=True):
        print(f"{move:<7}  x = {x:.3f}   height = {y:.3f}")
# --8<-- [end:corners]


if __name__ == "__main__":
    main()
