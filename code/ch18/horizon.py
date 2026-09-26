"""Chapter 18 -- the horizon calculator.

How far ahead does a forecast stay useful? If errors grow by the factor
e**exponent every step, the answer depends on the logarithm of how well you
know the start -- so each extra correct digit buys the same few steps.
The exponents are measured here, on three of the book's systems.
"""
# transcript: ch18-horizon

from _exponents import henon_exponent, logistic_exponent, lorenz_exponent

from chaoslab import horizon


# --8<-- [start:calculator]
def forecast_length(exponent: float, digits: int,
                    tolerance: float = 0.1) -> float:
    """How far ahead a forecast stays within `tolerance`, when the start is
    right to `digits` decimal places and an error is multiplied by
    e**exponent every step (or every unit of time)."""
    error = 1 / 10**digits          # six digits: an error of 0.000001
    return horizon(exponent, error, tolerance)
# --8<-- [end:calculator]


def main() -> None:
# --8<-- [start:table]
    systems = [("logistic map", logistic_exponent(), "steps"),
               ("Henon map", henon_exponent(), "steps"),
               ("Lorenz system", lorenz_exponent(), "time units")]
    print("                exponent   horizon with the start right to")
    print("                           3 digits  6 digits  9 digits")
    for name, lam, unit in systems:
        row = "".join(f"{forecast_length(lam, d):10.1f}" for d in (3, 6, 9))
        print(f"{name:14s}{lam:10.3f}{row}  {unit}")
# --8<-- [end:table]


if __name__ == "__main__":
    main()
