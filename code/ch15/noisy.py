"""Chapter 15 -- real data is a mix: chaos seen through measurement noise.

Each value of the rule's series is moved by a small random amount, as a
real instrument would move it, and both tests are run again: on the whole
record, and then on many short records, counting how often each test still
tells the rule from its own shuffle.
"""
# transcript: ch15-noisy

import random

from analogues import mean_error
from return_map import squares_touched
from twins import rule_series, shuffled

NOISE_SEED = 2     # the seed of the measurement noise
TRIALS = 100       # short records tried at each length


# --8<-- [start:noise]
def with_noise(xs: list[float], size: float,
               seed: int = NOISE_SEED) -> list[float]:
    """Move each value by a random amount between -size and +size."""
    rng = random.Random(seed)
    return [x + rng.uniform(-size, size) for x in xs]
# --8<-- [end:noise]


def right_answers(n: int, size: float) -> tuple[int, int]:
    """In TRIALS short records of length n, how often does each test
    (forecast, squares) say the rule's record is the less random one?"""
    record = with_noise(rule_series(n * TRIALS), size)
    rng = random.Random(n)
    by_forecast = by_squares = 0
    for k in range(TRIALS):
        part = record[k * n:(k + 1) * n]
        shuf = shuffled(part, seed=rng.randrange(10**9))
        if mean_error(part, 1, n // 2) < mean_error(shuf, 1, n // 2):
            by_forecast += 1
        if squares_touched(part) < squares_touched(shuf):
            by_squares += 1
    return by_forecast, by_squares


def main() -> None:
    rule = rule_series()
    # --8<-- [start:whole]
    print("noise  squares  1-step error")
    for size in (0.0, 0.01, 0.05, 0.2):
        noisy = with_noise(rule, size)
        print(f"{size:5.2f}  {squares_touched(noisy):7d}  "
              f"{mean_error(noisy, 1):12.2g}")
    # --8<-- [end:whole]
    # --8<-- [start:short]
    print("right answers out of 100 short records:")
    print("length  forecast test    squares test")
    print("        clean  noisy    clean  noisy")
    for n in (10, 20, 40, 100):
        f0, s0 = right_answers(n, 0.0)
        f1, s1 = right_answers(n, 0.2)
        print(f"{n:6d}  {f0:5d}  {f1:5d}    {s0:5d}  {s1:5d}")
    # --8<-- [end:short]


if __name__ == "__main__":
    main()
