"""Chapter 9 -- what stays the same from every start: two statistics.

Five starts, each followed for 510 time units; the first ten are dropped so
that the start itself is forgotten. For each run: which wing it is on at
time 50 (unpredictable), the fraction of the time it spends on the right
wing, and its average height z (neither of which cares about the start).
"""
# transcript: ch09-averages

from chaoslab import integrate, lorenz

STARTS = [(1.0, 1.0, 1.0), (-5.0, 3.0, 20.0), (10.0, -10.0, 30.0),
          (0.0, -1.0, 50.0), (30.0, -30.0, 5.0)]


# --8<-- [start:stats]
def fraction_right(path: list[tuple[float, ...]]) -> float:
    """The share of the states with x positive: time on the right wing."""
    return sum(1 for x, _, _ in path if x > 0) / len(path)


def mean_height(path: list[tuple[float, ...]]) -> float:
    """The average of z over the run: how high the state lives."""
    return sum(z for _, _, z in path) / len(path)
# --8<-- [end:stats]


def main() -> None:
    field = lorenz()
    print("start                 wing at 50   time on right   mean height")
    for start in STARTS:
        path = integrate(field, start, 0.01, 51_000)[1000:]
        wing = "R" if path[4000][0] > 0 else "L"
        label = "(" + ", ".join(f"{v:.0f}" for v in start) + ")"
        print(f"{label:22} {wing:>10} {fraction_right(path):15.2f} "
              f"{mean_height(path):13.2f}")


if __name__ == "__main__":
    main()
