"""Chapter 17 -- two Lorenz systems that agree, because one drives the other.

The original is Lorenz's chaotic system. The copy has the same rules for y
and z, but it is not allowed its own x: it is handed the original's x at
every moment. Pecora and Carroll (1990) showed that its y and z then fall
into step with the original's. A second copy, left to run on its own from
the same wrong start, never does.
"""
# transcript: ch17-sync

import math

from chaoslab import lorenz, rk4_step

SIGMA, RHO, BETA = 10.0, 28.0, 8.0 / 3.0
DT = 0.01


# --8<-- [start:field]
def drive_and_copy(s: tuple[float, ...]) -> tuple[float, ...]:
    """The original (x, y, z) and a copy (y2, z2) handed the original's x."""
    x, y, z, y2, z2 = s
    return (SIGMA * (y - x),
            x * (RHO - z) - y,
            x * y - BETA * z,
            x * (RHO - z2) - y2,     # the copy's rules, fed the SAME x
            x * y2 - BETA * z2)
# --8<-- [end:field]


ORIGINAL = lorenz(SIGMA, RHO, BETA)


def start() -> tuple[float, ...]:
    """The original, settled on its attractor; the copy's y and z at zero."""
    s = (1.0, 1.0, 1.0)
    for _ in range(2000):
        s = rk4_step(ORIGINAL, s, DT)
    return s + (0.0, 0.0)


def gap(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    """How far apart two states are: the square root of summed squares."""
    pairs = zip(a, b, strict=True)
    return math.sqrt(sum((p - q) * (p - q) for p, q in pairs))


def main() -> None:
    s = start()
    alone = (s[0], s[3], s[4])       # a copy that runs on its own
    print("  time    driven copy    copy left alone")
    for n in range(3001):
        if n % 500 == 0:
            driven = gap(s[1:3], s[3:5])
            free = gap(s[0:3], alone)
            print(f"{n * DT:6.1f}    {driven:10.2e}    {free:10.2e}")
        s = rk4_step(drive_and_copy, s, DT)
        alone = rk4_step(ORIGINAL, alone, DT)


if __name__ == "__main__":
    main()
