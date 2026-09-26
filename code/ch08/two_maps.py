"""Chapter 8 -- the same search on a different rule.

The sine map x -> s*sin(pi*x) has one hump with its top at x = 0.5, like
the logistic map, and nothing else in common with it. Find its landmarks
exactly as before and divide each gap by the next.

math.sin can differ in its last digit from one machine to another, so the
ratios are printed to two decimals, which no last digit can move.
"""
# transcript: ch08-two-maps

from superstable import LOGISTIC, landmarks, ratios

from chaoslab import sine_map

# --8<-- [start:sine]
SINE = (sine_map, (0.4, 0.6), (0.72, 0.84))
# --8<-- [end:sine]


def main() -> None:
    # --8<-- [start:table]
    a = landmarks(*LOGISTIC, count=11)
    b = landmarks(*SINE, count=11)
    print(" n   logistic   sine map")
    for n, (x, y) in enumerate(zip(ratios(a), ratios(b), strict=True), 2):
        print(f"{n:2d}  {x:9.2f}  {y:9.2f}")
    print(f"last{a[-1]:9.4f}  {b[-1]:9.4f}")
    # --8<-- [end:table]


if __name__ == "__main__":
    main()
