"""Chapter 4 -- a planet round a sun, stepped with RK4, timed ten times.

Newton's gravity as a rule of change. The sun is heavy enough not to move
and sits at (0, 0); the planet's state is four numbers, where it is (x, y)
and how fast it is going (vx, vy). Units are chosen to keep the numbers
small: the sun's pull at distance 1 is 1. Only +, -, *, / and sqrt, so
every digit printed is the same on every machine.
"""
# transcript: ch04-two-bodies

import math

from chaoslab import rk4_step


# --8<-- [start:gravity]
def gravity(s: tuple[float, ...]) -> tuple[float, ...]:
    """Position changes at the velocity; velocity changes towards the sun,
    by one over the distance squared."""
    x, y, vx, vy = s
    r = math.sqrt(x * x + y * y)
    pull = 1.0 / (r * r * r)          # 1/r^2, and x/r, y/r point home
    return (vx, vy, -pull * x, -pull * y)
# --8<-- [end:gravity]


def orbit(speed: float, laps: int = 10,
          dt: float = 0.002) -> tuple[float, float, float]:
    """Launch sideways at `speed` from (1, 0) and follow `laps` orbits.

    Returns the time of the first return to the starting line, the time
    of the last return divided by the number of laps, and the orbit's size
    (half its longest width: the average of nearest and farthest distance).
    """
    s = (1.0, 0.0, 0.0, speed)
    steps, returns = 0, []
    near = far = 1.0
    while len(returns) < laps:
        new = rk4_step(gravity, s, dt)
        r = math.sqrt(new[0] * new[0] + new[1] * new[1])
        near, far = min(near, r), max(far, r)
        if s[1] < 0.0 <= new[1]:          # crossed the starting line
            share = -s[1] / (new[1] - s[1])
            returns.append((steps + share) * dt)
        s, steps = new, steps + 1
    return returns[0], returns[-1] / laps, (near + far) / 2


SPEEDS = (1.0, 1.2, 1.3)


def main() -> None:
    print("launch   first lap   average of 10     size   lap^2/size^3")
    for speed in SPEEDS:
        first, average, size = orbit(speed)
        print(f"{speed:6.1f} {first:11.6f} {average:15.6f} {size:8.4f}"
              f" {average * average / (size * size * size):14.4f}")


if __name__ == "__main__":
    main()
