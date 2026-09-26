"""Chapter 6 -- what a forecast is worth, for each digit of the start.

For a start known to 2, 4, ... 12 decimal places, count the steps before
the true run and the forecast differ by more than 0.1, a tenth of the whole
range. One start can be lucky or unlucky, so the count is averaged over a
thousand starts spread evenly between 0 and 1.
"""
# transcript: ch06-worth

from twins import rule

from chaoslab import steps_until_apart

# --8<-- [start:worth]
TOL = 0.1                                           # "no longer useful"
STARTS = [(i + 0.5) / 1000 for i in range(1000)]
ERRORS = {2: 1e-2, 4: 1e-4, 6: 1e-6, 8: 1e-8, 10: 1e-10, 12: 1e-12}


def average_steps(error: float) -> float:
    """Steps a forecast stays within TOL, averaged over every start."""
    total = 0
    for x0 in STARTS:
        total += steps_until_apart(rule, x0, error, TOL)
    return total / len(STARTS)
# --8<-- [end:worth]


def main() -> None:
    for digits, error in ERRORS.items():
        print(f"start known to {digits:2d} decimal places: "
              f"{average_steps(error):4.1f} steps")


if __name__ == "__main__":
    main()
