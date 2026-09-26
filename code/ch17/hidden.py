"""Chapter 17 -- an unstable fixed point, and a chaotic orbit that keeps
coming back to it.

At r = 3.9 the logistic map has a fixed point, 1 - 1/r, where the rule
leaves x where it is. It repels: one step multiplies a miss by the slope
there. The orbit never settles on it -- and yet it keeps passing close.
"""
# transcript: ch17-hidden

from chaoslab import logistic, logistic_slope

# --8<-- [start:point]
R = 3.9
rule = logistic(R)
POINT = 1.0 - 1.0 / R                  # where the rule leaves x unchanged
STRETCH = logistic_slope(R)(POINT)     # one step multiplies a miss by this
# --8<-- [end:point]


def visits(x0: float, steps: int, near: float) -> list[int]:
    """The steps at which the orbit from x0 is within `near` of POINT."""
    found = []
    x = x0
    for n in range(1, steps + 1):
        x = rule(x)
        if abs(x - POINT) < near:
            found.append(n)
    return found


def main() -> None:
    print(f"fixed point      {POINT:.4f}")
    print(f"one step later   {rule(POINT):.4f}")
    print(f"slope there      {STRETCH:+.2f}")
    close = visits(0.2, 10_000, 0.01)
    print(f"steps within 0.01 of it, out of 10000: {len(close)}")
    print(f"the first ten: {close[:10]}")


if __name__ == "__main__":
    main()
