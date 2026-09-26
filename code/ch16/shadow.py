"""Chapter 16 -- the true orbit that a computed orbit is following.

Forwards, the logistic map at r = 4 doubles errors, so a computed orbit soon
leaves the orbit of its own start. Backwards it halves them. Running the rule
backwards from the computed orbit's last value finds a start whose EXACT
orbit stays close to every computed value: a shadow. Then the statistics:
how often each computed orbit is below 0.1, against the exact answer.
"""
# transcript: ch16-shadow

import math
from decimal import Decimal, localcontext

from two_formulas import rule_a, rule_b

HALF = Decimal("0.5")


# --8<-- [start:back]
def shadow(xs: list[float], digits: int = 400) -> list[Decimal]:
    """A true orbit that stays near the computed orbit xs, found backwards.

    Two numbers lead to y in one step: 1/2 - s/2 and 1/2 + s/2, where s is
    the square root of 1 - y. Take the one on the same side of 1/2 as the
    computed value, and step back again.
    """
    with localcontext() as ctx:
        ctx.prec = digits
        y = Decimal(xs[-1])
        ys = [y]
        for x in reversed(xs[:-1]):
            s = (1 - y).sqrt()
            y = HALF - s / 2 if x < 0.5 else HALF + s / 2
            ys.append(y)
    return ys[::-1]
# --8<-- [end:back]


def exact_orbit(start: Decimal, steps: int,
                digits: int = 400) -> list[Decimal]:
    """Forwards from `start`, carrying enough digits to be exact here."""
    with localcontext() as ctx:
        ctx.prec = digits
        x = start
        xs = [x]
        for _ in range(steps):
            x = 4 * x * (1 - x)
            xs.append(x)
    return xs


def computed(rule, steps: int) -> list[float]:
    xs = [0.1]
    for _ in range(steps):
        xs.append(rule(xs[-1]))
    return xs


def fraction_below(xs: list[float], level: float) -> float:
    return sum(1 for x in xs if x < level) / len(xs)


def main() -> None:
    xs = computed(rule_a, 1000)
    start = shadow(xs)[0]
    true = exact_orbit(start, 1000)
    gap = max(abs(t - Decimal(x)) for t, x in zip(true, xs, strict=True))
    tenth = Decimal(1) / 10
    print(f"steps computed with 4x(1-x):     {len(xs) - 1}")
    print(f"shadow's start minus 1/10:       {float(start - tenth):.1e}")
    print(f"farthest its exact orbit strays: {float(gap):.1e}")
    a = computed(rule_a, 1_000_000)[1:]
    b = computed(rule_b, 1_000_000)[1:]
    exact = 2 / math.pi * math.asin(math.sqrt(0.1))
    print("fraction of a million steps below 0.1:")
    print(f"  4x(1-x) {fraction_below(a, 0.1):.3f}   "
          f"4x-4xx {fraction_below(b, 0.1):.3f}   exact {exact:.3f}")


if __name__ == "__main__":
    main()
