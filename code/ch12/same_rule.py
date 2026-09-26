"""Chapter 12 -- the logistic map and z -> z*z + c are one rule.

Put z = r * (1/2 - x). Then x -> r*x*(1 - x) becomes z -> z*z + c with
c = r/2 - r*r/4. Run both at the same r and they settle into cycles of the
same length: the conversion is checked here, not trusted.
"""
# transcript: ch12-same-rule

from collections.abc import Callable

from chaoslab import logistic, orbit, period, r_to_c


# --8<-- [start:same]
def square_plus(c: float) -> Callable[[float], float]:
    """The rule z -> z*z + c, on the real line."""
    return lambda z: z * z + c


def both_periods(r: float, x0: float = 0.3) -> tuple[int | None, ...]:
    """The cycle length of each rule, after 3000 steps from matching starts.
    None means no cycle up to 64 steps long was found."""
    xs = orbit(logistic(r), x0, 3000)
    zs = orbit(square_plus(r_to_c(r)), r * (0.5 - x0), 3000)
    return period(xs), period(zs)
# --8<-- [end:same]


def main() -> None:
    # --8<-- [start:table]
    print("   r         c    cycle of x    cycle of z")
    for r in (2.8, 3.2, 3.5, 3.56, 3.83, 3.9):
        px, pz = (str(p or "none") for p in both_periods(r))
        print(f"{r:4.2f}  {r_to_c(r):8.4f}  {px:>12}  {pz:>12}")
    # --8<-- [end:table]


if __name__ == "__main__":
    main()
