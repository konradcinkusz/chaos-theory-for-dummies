"""Chapter 2 -- how many steps until a balance doubles?

Two ways to answer. Count the steps by iterating until the balance has
doubled, or ask the logarithm, which answers in fractions of a step. The
count is the logarithm's answer rounded up; the rule of 70 is the version
you can do in your head.
"""
# transcript: ch02-doubling

import math


# --8<-- [start:count]
def steps_to_double(rate: float) -> int:
    """Whole steps of x -> (1 + rate) * x until x has at least doubled."""
    x, steps = 1.0, 0
    while x < 2.0:
        x = (1.0 + rate) * x
        steps += 1
    return steps


def doubling_time(rate: float) -> float:
    """The same question asked of the logarithm: ln 2 / ln(1 + rate)."""
    return math.log(2.0) / math.log(1.0 + rate)
# --8<-- [end:count]


def main() -> None:
    # --8<-- [start:table]
    print("rate   counted   logarithm   rule of 70")
    for percent in (1, 2, 3, 5, 7, 10):
        rate = percent / 100
        print(f"{percent:3d}%   {steps_to_double(rate):7d}"
              f"   {doubling_time(rate):9.2f}   {70 / percent:10.1f}")
    # --8<-- [end:table]


if __name__ == "__main__":
    main()
