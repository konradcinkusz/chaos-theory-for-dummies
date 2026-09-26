"""Chapter 11 -- the box-counting dimension of the Henon attractor.

Chapter 10's two-line map, run for a million steps after it has settled
onto its attractor, and the points counted into boxes exactly as for the
Koch curve. The map uses only +, - and *, and the boxes are powers of two,
so every count is the same on every machine.
"""
# transcript: ch11-henon-boxes

from __future__ import annotations

from koch_boxes import counts, dimension

from chaoslab import henon


# --8<-- [start:points]
def attractor(n: int, burn: int = 1000) -> list[tuple[float, float]]:
    """n points of the Henon attractor, after `burn` steps to settle."""
    step = henon()                     # a = 1.4, b = 0.3
    p = (0.0, 0.0)
    for _ in range(burn):
        p = step(p)
    points = []
    for _ in range(n):
        p = step(p)
        points.append(p)
    return points
# --8<-- [end:points]


SIZES = [1 / 2**k for k in range(2, 11)]


def main() -> None:
    # --8<-- [start:count]
    print("boxes of side 1/4, 1/8, ... 1/1024 touched by the attractor")
    for n in (100_000, 1_000_000):
        ns = counts(attractor(n), SIZES)
        fives = [dimension(SIZES[i:i + 5], ns[i:i + 5]) for i in range(5)]
        print(f"{n:9d} points:" + "".join(f"{c:6d}" for c in ns))
        print(f"   slope through all nine sizes:   "
              f"{dimension(SIZES, ns):.3f}")
        print(f"   through any five in a row:      "
              f"{min(fives):.3f} to {max(fives):.3f}")
    # --8<-- [end:count]


if __name__ == "__main__":
    main()
