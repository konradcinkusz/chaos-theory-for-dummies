"""Chapter 15 -- two series made of exactly the same numbers.

One is the logistic map at r = 4, the rule of Chapter 5. The other is the
same numbers shuffled into a random order: a shuffle keeps every value, so
it keeps the histogram exactly, and destroys only the order. A series made
this way to test another is called a surrogate.
"""
# transcript: ch15-twins

import random

from chaoslab import logistic, orbit

N = 2000     # how many values each series has
X0 = 0.2     # where the rule starts
SEED = 15    # the shuffle's seed: the same shuffle on every machine


# --8<-- [start:make]
def rule_series(n: int = N, x0: float = X0) -> list[float]:
    """n values of the logistic map x -> 4x(1 - x), starting at x0."""
    return orbit(logistic(4.0), x0, n - 1)


def shuffled(xs: list[float], seed: int = SEED) -> list[float]:
    """The same numbers in a random order: a surrogate."""
    copy = list(xs)
    random.Random(seed).shuffle(copy)
    return copy
# --8<-- [end:make]


def histogram(xs: list[float], bins: int = 5) -> list[int]:
    """How many values fall in each of `bins` equal slices of 0 to 1."""
    counts = [0] * bins
    for x in xs:
        counts[min(bins - 1, int(x * bins))] += 1
    return counts


def main() -> None:
    rule = rule_series()
    shuf = shuffled(rule)
    print("   rule  shuffled")
    for a, b in zip(rule[:5], shuf[:5], strict=True):
        print(f"{a:7.4f}  {b:7.4f}")
    print("counts in five slices of width 0.2:")
    print("rule    ", histogram(rule))
    print("shuffled", histogram(shuf))


if __name__ == "__main__":
    main()
