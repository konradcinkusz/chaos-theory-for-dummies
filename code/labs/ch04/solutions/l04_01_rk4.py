"""Reference solution for Lab 4.1."""

from collections.abc import Callable

State = tuple[float, ...]


def _ahead(state: State, rates: State, h: float) -> State:
    """Where you would be after moving for h at these rates."""
    return tuple(s + h * r for s, r in zip(state, rates, strict=True))


def rk4_step(field: Callable[[State], State], state: State,
             dt: float) -> State:
    """The state one step of length dt later, by the RK4 recipe."""
    k1 = field(state)
    k2 = field(_ahead(state, k1, dt / 2))
    k3 = field(_ahead(state, k2, dt / 2))
    k4 = field(_ahead(state, k3, dt))
    return tuple(s + dt * (a + 2 * b + 2 * c + d) / 6
                 for s, a, b, c, d in zip(state, k1, k2, k3, k4, strict=True))
