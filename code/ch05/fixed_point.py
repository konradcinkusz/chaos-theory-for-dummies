"""Chapter 5 -- the logistic map's steady state, and whether it holds.

Where the fixed point is comes from a line of algebra. Whether it holds is a
measurement, Chapter 3's: nudge x a tiny amount each way and see how much
one step multiplies the nudge. That number is the slope of the rule there.
"""
# transcript: ch05-fixed-point

# --8<-- [start:fixed]
from chaoslab import logistic, slope


def fixed_point(r: float) -> float:
    """The value, other than zero, that the rule leaves unchanged."""
    return 1.0 - 1.0 / r


def main() -> None:
    print("  r   fixed point   slope there   a nudge")
    for r in (2.8, 3.2, 3.5, 3.9):
        x = fixed_point(r)
        s = slope(logistic(r), x)      # nudge x both ways, measure the move
        fate = "shrinks" if abs(s) < 1 else "grows"
        print(f"{r:.1f}   {x:11.3f}   {s:11.2f}   {fate}")
# --8<-- [end:fixed]


if __name__ == "__main__":
    main()
