"""Chapter 10 -- stretched one way, squeezed the other.

Two starts a ten-billionth apart separate until they are as far apart as
the attractor is wide, and then stop growing apart: bounded, and still
sensitive. Then a tiny arrow is carried along one long run to find the
average stretch per step, which is the Lyapunov exponent of Chapter 7
measured on a map of the plane.
"""
# transcript: ch10-stretch

import math

from henon import A, B, henon


def settle(steps: int = 1000) -> tuple[float, float]:
    """A point on the attractor: start at (0, 0) and let it settle."""
    x, y = 0.0, 0.0
    for _ in range(steps):
        x, y = henon(x, y)
    return x, y


def gaps() -> None:
    """Two starts 1e-10 apart, and the distance between them."""
    x1, y1 = settle()
    x2, y2 = x1 + 1e-10, y1
    for step in range(81):
        if step % 10 == 0:
            dx, dy = x2 - x1, y2 - y1
            gap = math.sqrt(dx * dx + dy * dy)
            print(f"step {step:2d}: gap {gap:.1e}")
        x1, y1 = henon(x1, y1)
        x2, y2 = henon(x2, y2)


# --8<-- [start:arrow]
def exponent(steps: int = 200_000) -> float:
    """The average of log(stretch) of a tiny arrow along one long run."""
    x, y = settle()
    dx, dy = 1.0, 0.0                    # an arrow of length one
    total = 0.0
    for _ in range(steps):
        dx, dy = -2.0 * A * x * dx + dy, B * dx   # one step moves it
        x, y = henon(x, y)
        grow = math.sqrt(dx * dx + dy * dy)       # how much it stretched
        total += math.log(grow)
        dx, dy = dx / grow, dy / grow             # back to length one
    return total / steps
# --8<-- [end:arrow]


def main() -> None:
    gaps()
    lam = exponent()
    print(f"Lyapunov exponent: {lam:.2f} per step")
    print(f"stretch per step:  {math.exp(lam):.2f}")
    print(f"squeeze per step:  {B / math.exp(lam):.2f}")


if __name__ == "__main__":
    main()
