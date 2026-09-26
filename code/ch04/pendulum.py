"""Chapter 4 -- how long a pendulum takes to swing out and back.

The state is two numbers, the angle and how fast the angle is changing,
and the rule of change is chaoslab's pendulum field, followed with RK4.
The timing is found by stepping until the swing turns round at the far
side, then sharing out the last step in proportion (interpolation).
"""
# transcript: ch04-pendulum

import math

from chaoslab import pendulum, rk4_step

# --8<-- [start:period]
G_OVER_L = 9.81              # gravity over length: a one-metre pendulum
FIELD = pendulum(G_OVER_L)   # (angle, angular velocity) -> their rates


def period(swing_degrees: float, dt: float = 0.001) -> float:
    """Seconds for one full swing, out and back, released at rest."""
    state = (math.radians(swing_degrees), 0.0)
    steps = 0
    while True:
        new = rk4_step(FIELD, state, dt)
        if new[1] > 0.0:     # it has stopped at the far side, turned round
            share = -state[1] / (new[1] - state[1])
            return 2 * (steps + share) * dt   # out and back is twice this
        state, steps = new, steps + 1
# --8<-- [end:period]


SWINGS = (5, 10, 45, 90, 170)


def main() -> None:
    print("released at   one swing out and back")
    for degrees in SWINGS:
        print(f"{degrees:6d} deg    {period(degrees):8.3f} s")


if __name__ == "__main__":
    main()
