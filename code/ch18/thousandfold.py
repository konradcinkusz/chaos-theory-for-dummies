"""Chapter 18 -- a thousand times better data, measured on the logistic map.

The formula says how far a forecast lasts. This does it the long way: for
two hundred and one different starts, run two copies of the logistic map at
r = 4 that begin a millionth apart, and count the steps until they differ
by more than 0.1. Then do it again a billionth apart -- a measurement a
thousand times as precise.
"""
# transcript: ch18-thousandfold

from statistics import median

from chaoslab import logistic, steps_until_apart

RULE = logistic(4.0)
STARTS = [0.1 + 0.8 * k / 201 + 0.00123 for k in range(201)]


# --8<-- [start:measure]
def typical_horizon(error: float, tolerance: float = 0.1) -> float:
    """The median, over many starts, of the steps two runs `error` apart
    stay within `tolerance` of each other."""
    return median(steps_until_apart(RULE, x0, error, tolerance)
                  for x0 in STARTS)


def main() -> None:
    six = typical_horizon(1 / 10**6)      # start known to six digits
    nine = typical_horizon(1 / 10**9)     # a thousand times better
    print(f"start right to 6 digits: {six:.0f} steps")
    print(f"start right to 9 digits: {nine:.0f} steps")
    print(f"a thousandfold better measurement bought {nine - six:.0f} steps")
    # --8<-- [end:measure]


if __name__ == "__main__":
    main()
