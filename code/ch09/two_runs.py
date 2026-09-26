"""Chapter 9 -- two runs of Lorenz's rules, a hair apart.

The first fifty time units carry the run away from its start and onto the
butterfly; there it is copied, and the copy nudged by one part in a hundred
million in x. Both are then followed with the same rule.
"""
# transcript: ch09-two-runs

import math

from chaoslab import integrate, lorenz, rk4_step

# --8<-- [start:split]
DT = 0.01
field = lorenz()
a = integrate(field, (1.0, 1.0, 1.0), DT, 5000)[-1]   # fifty time units
b = (a[0] + 1e-8, a[1], a[2])      # the copy, 0.00000001 further in x
# --8<-- [end:split]


def distance(p: tuple[float, ...], q: tuple[float, ...]) -> float:
    """How far apart two states are, straight across the three numbers."""
    return math.sqrt(sum((u - v) * (u - v)
                         for u, v in zip(p, q, strict=True)))


def first_apart(p: tuple[float, ...], q: tuple[float, ...],
                tolerance: float = 1.0, limit: int = 10_000) -> float:
    """The time at which two runs from p and q first differ by more than
    `tolerance`."""
    for k in range(limit):
        if distance(p, q) > tolerance:
            return k * DT
        p, q = rk4_step(field, p, DT), rk4_step(field, q, DT)
    raise RuntimeError("still together")


def main() -> None:
    print("  time   x of A    x of B     apart")
    p, q = a, b
    for k in range(2401):
        if k % 200 == 0:
            print(f"{k * DT:6.0f} {p[0]:8.2f} {q[0]:9.2f} "
                  f"{distance(p, q):9.1e}")
        p, q = rk4_step(field, p, DT), rk4_step(field, q, DT)
    print(f"first more than 1 apart at time {first_apart(a, b):.1f}")


if __name__ == "__main__":
    main()
