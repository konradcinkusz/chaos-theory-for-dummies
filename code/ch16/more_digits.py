"""Chapter 16 -- exact arithmetic, and arithmetic with more digits.

A Fraction never rounds, but the logistic map squares the bottom of the
fraction at every step, so the number of digits doubles. A Decimal keeps a
fixed number of digits instead, and every digit buys a fixed number of
correct steps.
"""
# transcript: ch16-more-digits

from decimal import Decimal, localcontext
from fractions import Fraction


def orbit(digits: int, steps: int) -> list[Decimal]:
    """The orbit of 1/10 at r = 4, kept to `digits` significant digits."""
    with localcontext() as ctx:
        ctx.prec = digits
        x = Decimal(1) / 10
        xs = [x]
        for _ in range(steps):
            x = 4 * x * (1 - x)
            xs.append(x)
    return xs


def right_for(digits: int, truth: list[Decimal]) -> int:
    """Steps before a run with `digits` digits is 0.1 away from the truth."""
    path = orbit(digits, len(truth) - 1)
    return next(n for n, (p, t) in enumerate(zip(path, truth, strict=True))
                if abs(p - t) > Decimal("0.1"))


def main() -> None:
    # --8<-- [start:exact]
    x = Fraction(1, 10)
    for n in range(13):
        if n % 2 == 0:
            print(f"step {n:2d}: {len(str(x.denominator)):5d} digits")
        x = 4 * x * (1 - x)
    # --8<-- [end:exact]
    truth = orbit(1000, 600)
    for digits in (16, 32, 64, 128):
        print(f"{digits:4d} digits kept: right for "
              f"{right_for(digits, truth)} steps")


if __name__ == "__main__":
    main()
