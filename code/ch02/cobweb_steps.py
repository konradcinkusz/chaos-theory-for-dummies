"""Chapter 2 -- the corners of a cobweb diagram, as numbers.

To the rule's line, across to the diagonal, to the line again: each pair of
corners after the first is one step of the rule, drawn on its own graph.
"""
# transcript: ch02-cobweb

from chaoslab import cobweb, linear


def main() -> None:
    # --8<-- [start:corners]
    tablets = linear(0.5, 100.0)
    corners = cobweb(tablets, 0.0, 3)
    print(f"start            ({corners[0][0]:5.1f}, {corners[0][1]:5.1f})")
    for k, (x, y) in enumerate(corners[1:]):
        move = "to the line" if k % 2 == 0 else "to the diagonal"
        print(f"{move:15}  ({x:5.1f}, {y:5.1f})")
    # --8<-- [end:corners]


if __name__ == "__main__":
    main()
