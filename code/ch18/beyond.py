"""Chapter 18 -- what is still predictable after the horizon.

A forecast made as an ensemble: a thousand runs of the logistic map at
r = 4, started across the range of what the measurement allows. The
forecast is the fraction of runs that land below 0.25 -- the odds. Then one
long run, from two different starts, asks the same question of the long
term. Only + - * / touch the runs, so every fraction is the same everywhere.
"""
# transcript: ch18-beyond

from chaoslab import logistic

RULE = logistic(4.0)
MEMBERS = 1000


# --8<-- [start:ensemble]
def odds(centre: float, width: float, steps: int) -> list[float]:
    """After each step, the fraction of MEMBERS runs below 0.25. The runs
    start spread evenly across `width` around `centre`."""
    runs = [centre + width * (k / (MEMBERS - 1) - 0.5)
            for k in range(MEMBERS)]
    fractions = []
    for _ in range(steps + 1):
        fractions.append(sum(1 for x in runs if x < 0.25) / MEMBERS)
        runs = [RULE(x) for x in runs]
    return fractions


def long_run(start: float, steps: int = 100_000) -> float:
    """The fraction of one long run's steps spent below 0.25."""
    x, below = start, 0
    for _ in range(steps):
        below += x < 0.25
        x = RULE(x)
    return below / steps
# --8<-- [end:ensemble]


def main() -> None:
    wide, narrow = odds(0.3, 1e-6, 40), odds(0.3, 1e-9, 40)
    print("       chance that x < 0.25, start right to")
    print("step      6 digits       9 digits")
    for step in range(0, 41, 4):
        print(f"{step:4d}{wide[step]:14.2f}{narrow[step]:15.2f}")
    for start in (0.3, 0.8):
        print(f"one long run from {start}: {long_run(start):.2f} of its "
              f"steps below 0.25")


if __name__ == "__main__":
    main()
