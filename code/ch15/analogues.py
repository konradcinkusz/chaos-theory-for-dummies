"""Chapter 15 -- forecasting by analogues: find the past value most like
now, and say that what happened next then will happen next now.

It needs no rule, only a record. For a series made by a rule it works a
few steps ahead; for shuffled numbers it is no better than a blind guess.
"""
# transcript: ch15-analogues

from twins import rule_series, shuffled

SPLIT = 1000   # learn from the first 1000 values, test on the rest


# --8<-- [start:forecast]
def forecast(library: list[float], x: float, h: int) -> float:
    """Predict h steps after x: find the value in the library most like
    x, and return what came h steps after it."""
    best = min(range(len(library) - h),
               key=lambda j: abs(library[j] - x))
    return library[best + h]


def mean_error(xs: list[float], h: int, split: int = SPLIT) -> float:
    """The average size of the forecast's miss, h steps ahead: learn from
    xs[:split], test on every value after it."""
    library, test = xs[:split], xs[split:]
    misses = [abs(forecast(library, test[t], h) - test[t + h])
              for t in range(len(test) - h)]
    return sum(misses) / len(misses)
# --8<-- [end:forecast]


def main() -> None:
    rule = rule_series()
    shuf = shuffled(rule)
    print("steps ahead   rule    shuffled")
    for h in range(1, 13):
        print(f"{h:11d}  {mean_error(rule, h):7.2g}  "
              f"{mean_error(shuf, h):8.2g}")


if __name__ == "__main__":
    main()
