"""Chapter 4 -- a mass on a spring, stepped forward with Euler's method.

The rule does not say where the mass will be next; it says how fast each
number of the state is changing right now. Euler's method turns that back
into the iteration of Chapter 2: pretend the rates stay the same for a
short time dt, move, and ask the rule again.
"""
# transcript: ch04-spring-euler

# --8<-- [start:euler]
K = 1.0   # how stiff the spring is, for each kilogram of mass


def rates(x: float, v: float) -> tuple[float, float]:
    """How fast position and velocity are changing right now."""
    return v, -K * x   # moves at v; the spring pulls back towards 0


def euler_step(x: float, v: float, dt: float) -> tuple[float, float]:
    """Pretend the rates stay the same for dt, and move."""
    dx, dv = rates(x, v)
    return x + dt * dx, v + dt * dv


def energy(x: float, v: float) -> float:
    """Energy of motion plus energy stored in the stretched spring."""
    return 0.5 * v * v + 0.5 * K * x * x


def main() -> None:
    x, v, dt = 1.0, 0.0, 0.1       # pulled out 1 metre, let go
    for step in range(101):        # 100 steps of 0.1 s: ten seconds
        if step % 20 == 0:
            print(f"t = {step * dt:4.1f} s   x = {x:6.3f}   "
                  f"v = {v:6.3f}   energy = {energy(x, v):.4f}")
        x, v = euler_step(x, v, dt)
# --8<-- [end:euler]


if __name__ == "__main__":
    main()
