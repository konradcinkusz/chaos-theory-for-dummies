"""Chapter 7 -- the prediction horizon, predicted and counted.

At r = 4 an error delta grows at ln 2 per step, so the formula says it
reaches a tolerance T after about ln(T / delta) / ln 2 steps. Here the
formula is set beside a count: two runs delta apart, followed until they
differ by more than T, from a thousand different starts.
"""
# transcript: ch07-horizon

import math

from chaoslab import logistic, steps_until_apart


# --8<-- [start:formula]
def horizon(lam: float, delta: float, tol: float) -> float:
    """Steps until an error delta grows to tol, growing at lam per step."""
    return math.log(tol / delta) / lam
# --8<-- [end:formula]


def counts(r: float, delta: float, tol: float) -> list[int]:
    """The step at which two runs delta apart first differ by more than
    tol, from each of a thousand starts spread evenly between 0 and 1."""
    starts = [(k + 0.5) / 1000 for k in range(1000)]
    return [steps_until_apart(logistic(r), x0, delta, tol) for x0 in starts]


def main() -> None:
    # --8<-- [start:table]
    lam, tol = math.log(2), 0.1
    print("  error    formula   counted:  mean   fastest  slowest")
    for delta in (1e-3, 1e-6, 1e-9, 1e-12):
        c = counts(4.0, delta, tol)
        mean = sum(c) / len(c)
        print(f"{delta:7.0e}   {horizon(lam, delta, tol):6.1f}"
              f"            {mean:5.1f}    {min(c):4d}     {max(c):4d}")
    # --8<-- [end:table]


if __name__ == "__main__":
    main()
