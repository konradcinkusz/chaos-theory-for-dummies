"""Chapter 8 -- where does each doubling happen? Watch, and bisect.

Between two values of r whose periods are known from the last table, find
the r at which period p gives way to period 2p: try the middle, see what
the orbit settles into, and keep the half where the change still lies.
"""
# transcript: ch08-doublings

from chaoslab import logistic, orbit, period


# --8<-- [start:settle]
def settled_period(r: float, burn: int = 20_000) -> int | None:
    """The period the orbit at r has settled into, after `burn` steps."""
    xs = orbit(logistic(r), 0.5, burn + 256)
    return period(xs[burn:], tol=1e-6)
# --8<-- [end:settle]


# --8<-- [start:fork]
def fork(p: int, lo: float, hi: float, rounds: int = 20) -> float:
    """The r between lo and hi at which period p gives way to 2p."""
    for _ in range(rounds):
        mid = (lo + hi) / 2
        q = settled_period(mid)
        if q is not None and q <= p:
            lo = mid        # still period p here: the fork is further on
        else:
            hi = mid        # already doubled: the fork is behind us
    return (lo + hi) / 2
# --8<-- [end:fork]


# From the last table: period 1 at 2.8, 2 at 3.2, 4 at 3.5, 8 at 3.56,
# 16 at 3.567. Each fork lies between two neighbouring rows.
BRACKETS = [(1, 2.8, 3.2), (2, 3.2, 3.5), (4, 3.5, 3.56), (8, 3.56, 3.567)]


def forks() -> list[float]:
    """The four forks, to the four decimals the table prints."""
    return [round(fork(p, lo, hi), 4) for p, lo, hi in BRACKETS]


def main() -> None:
    # --8<-- [start:table]
    rs = forks()
    print("   fork       r     gap   ratio")
    for i, (p, _, _) in enumerate(BRACKETS):
        line = f"{p:>2} -> {2 * p:<2}  {rs[i]:.4f}"
        if i >= 1:
            line += f"  {rs[i] - rs[i - 1]:.4f}"
        if i >= 2:
            ratio = (rs[i - 1] - rs[i - 2]) / (rs[i] - rs[i - 1])
            line += f"  {ratio:6.2f}"
        print(line)
    # --8<-- [end:table]


if __name__ == "__main__":
    main()
