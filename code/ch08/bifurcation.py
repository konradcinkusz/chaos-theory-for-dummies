"""Chapter 8 -- where the logistic map lives in the long run, r by r.

The recipe behind the bifurcation diagram: for each r, run the map, throw
away the first thousand steps (the transient), and keep what comes after.
One value kept over and over is a fixed point; two is a two-cycle; a smear
of values that never repeats is chaos.
"""
# transcript: ch08-bifurcation

from chaoslab import logistic, orbit, period

# --8<-- [start:longrun]
BURN = 1000   # steps thrown away while the orbit settles
KEEP = 300    # steps kept: where the orbit lives


def long_run(r: float, burn: int = BURN, keep: int = KEEP) -> list[float]:
    """The values the logistic map visits at r once it has settled."""
    xs = orbit(logistic(r), 0.5, burn + keep)
    return xs[burn + 1:]
# --8<-- [end:longrun]


def main() -> None:
    print("    r  period  where the orbit lives")
    for r in (2.8, 3.2, 3.5, 3.56, 3.567, 3.9):
        xs = long_run(r)
        p = period(xs)
        if p is None:
            where = f"anywhere from {min(xs):.2f} to {max(xs):.2f}"
        elif p <= 4:
            where = " ".join(f"{x:.4f}" for x in sorted(xs[:p]))
        else:
            where = f"{p} values from {min(xs):.2f} to {max(xs):.2f}"
        print(f"{r:5}  {p if p else '-':>6}  {where}")


if __name__ == "__main__":
    main()
