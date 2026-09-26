"""Chapter 7 -- the Lyapunov exponent, by averaging.

Follow one orbit of the logistic map, take the natural logarithm of the
size of the stretch at every point it visits, and average. That average is
the Lyapunov exponent: positive when nearby starts separate, negative when
they close up. At r = 4 the exact value is known, ln 2, so the program can
be checked against it.
"""
# transcript: ch07-exponent

import math

from stretch import step, stretch


# --8<-- [start:exponent]
def exponent(r: float, x0: float = 0.3, steps: int = 100_000,
             burn: int = 1000) -> float:
    """The average of ln|stretch| along the orbit of the logistic map."""
    x = x0
    for _ in range(burn):          # let the orbit settle first
        x = step(r, x)
    total = 0.0
    for _ in range(steps):
        total += math.log(abs(stretch(r, x)))
        x = step(r, x)
    return total / steps
# --8<-- [end:exponent]


def main() -> None:
# --8<-- [start:run]
    for r in (2.8, 3.2, 3.5, 4.0):
        lam = exponent(r)
        verdict = "errors grow" if lam > 0 else "errors shrink"
        print(f"r = {r}:  exponent {lam:+.2f}   {verdict}")
    print(f"exact value at r = 4:  ln 2 = {math.log(2):.4f}")
# --8<-- [end:run]


if __name__ == "__main__":
    main()
