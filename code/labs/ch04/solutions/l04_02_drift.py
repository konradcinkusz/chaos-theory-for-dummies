"""Reference solution for Lab 4.2."""

from chaoslab import spring

FIELD = spring(1.0)
START = (1.0, 0.0)


def spring_energy(state: tuple[float, float]) -> float:
    """Energy of motion plus energy stored in the spring."""
    x, v = state
    return 0.5 * v * v + 0.5 * x * x


def drift(stepper, dt: float, seconds: float) -> float:
    """Fractional change in energy after `seconds` of steps of dt."""
    state = START
    for _ in range(round(seconds / dt)):
        state = stepper(FIELD, state, dt)
    return spring_energy(state) / spring_energy(START) - 1.0
