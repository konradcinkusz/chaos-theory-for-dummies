"""Chapter 4 -- how much energy a simulated spring gains or loses.

A spring without friction keeps its energy for ever. A simulation of one
need not, and the change is the cleanest measure there is of how far a
simulation has wandered from the system it claims to be.
"""
# transcript: ch04-energy-drift

from chaoslab import euler_step, rk4_step, spring

# --8<-- [start:drift]
FIELD = spring(1.0)        # the rule of change from the chapter
START = (1.0, 0.0)         # pulled out 1 metre, at rest


def energy(state: tuple[float, ...]) -> float:
    x, v = state
    return 0.5 * v * v + 0.5 * x * x


def drift(stepper, dt: float, seconds: float) -> float:
    """Fractional change in energy after following the rule for seconds."""
    state = START
    for _ in range(round(seconds / dt)):
        state = stepper(FIELD, state, dt)
    return energy(state) / energy(START) - 1.0
# --8<-- [end:drift]


RUNS = [(euler_step, "Euler", 1, 0.1, 10), (euler_step, "Euler", 1, 0.01, 10),
        (euler_step, "Euler", 1, 0.01, 100),
        (euler_step, "Euler", 1, 0.025, 10),
        (rk4_step, "RK4", 4, 0.1, 10), (rk4_step, "RK4", 4, 0.1, 1000)]


def main() -> None:
    print("method   step   seconds   rule calls   energy change")
    for stepper, name, calls, dt, seconds in RUNS:
        work = calls * round(seconds / dt)
        change = 100 * drift(stepper, dt, seconds)
        print(f"{name:6s} {dt:6.3f} {seconds:8d} {work:11d}"
              f"   {change:+.3g} %")


if __name__ == "__main__":
    main()
