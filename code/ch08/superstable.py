"""Chapter 8 -- the superstable landmarks, found exactly by bisection.

The logistic map's slope r*(1 - 2x) is zero at the top of the hump, x = 0.5.
A cycle that passes through 0.5 kills every nudge in one trip, so for each
period there is one r -- the superstable landmark -- at which 0.5 itself
comes back to 0.5. That is one equation in r, and halving an interval until
it is tiny solves it with nothing but + - * and /.
"""
# transcript: ch08-superstable

from collections.abc import Callable

from chaoslab import logistic

Rule = Callable[[float], float]
Family = Callable[[float], Rule]


# --8<-- [start:search]
def from_top(f: Rule, steps: int) -> float:
    """Start at the top of the hump; how far from it are you after steps?"""
    x = 0.5
    for _ in range(steps):
        x = f(x)
    return x - 0.5


def bisect(g: Callable[[float], float], lo: float, hi: float,
           rounds: int = 60) -> float:
    """A root of g between lo and hi, where g changes sign: halve and keep
    the half in which the sign still changes."""
    below = g(lo) < 0
    if (g(hi) < 0) == below:
        raise ValueError("g must change sign between lo and hi")
    for _ in range(rounds):
        mid = (lo + hi) / 2
        if (g(mid) < 0) == below:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2
# --8<-- [end:search]


# --8<-- [start:landmarks]
def returns(family: Family, steps: int) -> Callable[[float], float]:
    """The function of r whose root is the landmark with this period."""
    return lambda r: from_top(family(r), steps)


def landmarks(family: Family, first: tuple[float, float],
              second: tuple[float, float], count: int,
              base: int = 1) -> list[float]:
    """The landmarks for periods base, 2*base, 4*base, ... `first` and
    `second` bracket the first two; each later one is sought between a
    tenth and a half of the last gap beyond the last landmark found."""
    found = [bisect(returns(family, base), *first),
             bisect(returns(family, 2 * base), *second)]
    for n in range(2, count):
        gap = found[-1] - found[-2]
        found.append(bisect(returns(family, base * 2 ** n),
                            found[-1] + gap / 10, found[-1] + gap / 2))
    return found


LOGISTIC = (logistic, (1.5, 2.5), (3.0, 3.4))
# --8<-- [end:landmarks]


def ratios(found: list[float]) -> list[float]:
    """Each gap divided by the next one."""
    return [(b - a) / (c - b) for a, b, c in zip(found, found[1:],
                                                   found[2:], strict=False)]


def main() -> None:
    found = landmarks(*LOGISTIC, count=11)
    print(" n  period    landmark R_n           gap   ratio")
    for n, r in enumerate(found):
        line = f"{n:2d}  {2 ** n:6d}  {r:.10f}"
        if n >= 1:
            line += f"  {r - found[n - 1]:.10f}"
        if n >= 2:
            line += f"  {ratios(found)[n - 2]:.4f}"
        print(line)


if __name__ == "__main__":
    main()
