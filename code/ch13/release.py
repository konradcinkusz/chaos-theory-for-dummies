"""Chapter 13 -- a double pendulum let go from high up, with its check.

Two arms one metre long and two bobs of one kilogram, released from rest
with both arms 120 degrees from hanging straight down. The rule of change
comes from Newton's laws and lives in chaoslab.double_pendulum; Chapter 4's
RK4 steps it. The last column is the check: with no friction the energy
must not change, so any change there is the stepper's error, not physics.
"""
# transcript: ch13-release

import math

from chaoslab import double_pendulum, double_pendulum_energy, rk4_step

# --8<-- [start:setup]
DT = 0.001                  # seconds per step
RULE = double_pendulum()    # g = 9.81, arms of 1 m, bobs of 1 kg


def release(upper: float, lower: float) -> tuple[float, ...]:
    """A pendulum let go from rest, with its arms at these angles (degrees).

    The state is four numbers: the two angles (in radians, measured from
    straight down) and how fast each angle is changing (radians a second).
    """
    return (math.radians(upper), math.radians(lower), 0.0, 0.0)
# --8<-- [end:setup]


def main() -> None:
# --8<-- [start:run]
    state = release(120, 120)
    print(" t (s)   upper arm   lower arm    energy (J)")
    for step in range(10_001):
        if step % 2000 == 0:
            upper = math.degrees(state[0])
            lower = math.degrees(state[1])
            energy = double_pendulum_energy(state)
            print(f"{step * DT:5.1f} {upper:9.1f} deg {lower:7.1f} deg"
                  f" {energy:13.8f}")
        state = rk4_step(RULE, state, DT)
# --8<-- [end:run]


if __name__ == "__main__":
    main()
