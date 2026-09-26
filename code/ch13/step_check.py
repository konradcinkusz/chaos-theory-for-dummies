"""Chapter 13 -- is the parting physics, or is it the stepper?

Run the same two releases with four step sizes. If the parting were made by
the stepper's own errors, a smaller step would move it; the energy column
shows how much smaller those errors get each time the step is halved.
"""
# transcript: ch13-step-check

from release import RULE, release
from two_releases import APART, NUDGE, gap

from chaoslab import double_pendulum_energy, rk4_step


# --8<-- [start:parting]
def parting(dt: float) -> tuple[float, float]:
    """Seconds until the pair is APART, and how far the energy moved."""
    a = release(120, 120)
    b = (a[0] + NUDGE, a[1], a[2], a[3])
    start = double_pendulum_energy(a)
    worst, step = 0.0, 0
    while gap(a, b) <= APART:
        a, b = rk4_step(RULE, a, dt), rk4_step(RULE, b, dt)
        step += 1
        worst = max(worst, abs(double_pendulum_energy(a) - start))
    return step * dt, worst
# --8<-- [end:parting]


STEPS = (0.004, 0.002, 0.001, 0.0005)


def main() -> None:
    # --8<-- [start:run]
    for dt in STEPS:
        seconds, worst = parting(dt)
        print(f"step {dt:6.4f} s   apart after {seconds:5.2f} s"
              f"   energy moved {worst:.1e} J")
    # --8<-- [end:run]


if __name__ == "__main__":
    main()
