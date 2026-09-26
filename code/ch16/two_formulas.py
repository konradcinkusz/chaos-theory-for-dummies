"""Chapter 16 -- one rule written two ways, with the truth beside them.

4x(1 - x) and 4x - 4xx are the same rule: multiply out the bracket. On a
computer they round differently, and the logistic map at r = 4 does the
rest. The truth is the orbit of exactly one tenth, carried to a hundred
significant digits, which is far more than seventy steps can use up.
"""
# transcript: ch16-two-formulas

from decimal import Decimal, localcontext


# --8<-- [start:rules]
def rule_a(x: float) -> float:
    return 4.0 * x * (1.0 - x)


def rule_b(x: float) -> float:
    return 4.0 * x - 4.0 * x * x      # the same, multiplied out
# --8<-- [end:rules]


def truth(steps: int, digits: int = 100) -> list[Decimal]:
    """The orbit of exactly 1/10, kept to `digits` significant digits."""
    with localcontext() as ctx:
        ctx.prec = digits
        x = Decimal(1) / 10
        xs = [x]
        for _ in range(steps):
            x = 4 * x * (1 - x)
            xs.append(x)
    return xs


def main() -> None:
    # --8<-- [start:race]
    a = b = 0.1
    true = truth(70)
    print("step    4x(1-x)    4x-4xx      truth")
    for n in range(71):
        if n % 10 == 0 or n in (45, 55):
            print(f"{n:4d} {a:10.6f} {b:10.6f} {float(true[n]):10.6f}")
        a, b = rule_a(a), rule_b(b)
    # --8<-- [end:race]


if __name__ == "__main__":
    main()
