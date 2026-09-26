"""Flows: rules of change in continuous time, and how to step them.

A flow is a function that takes the state -- a tuple of numbers -- and
returns how fast each number is changing right now. Chapter 4 reads it as a
velocity. To follow it on a computer you take small steps of length dt; this
file has the crudest way to do that (Euler) and a good one (RK4).

Only +, -, * and / on floats, so every step is correctly rounded and the
same on every machine.
"""

from __future__ import annotations

from collections.abc import Callable

State = tuple[float, ...]
Field = Callable[[State], State]
Stepper = Callable[[Field, State, float], State]


def _add(a: State, b: State, k: float) -> State:
    """a + k*b, component by component."""
    return tuple(x + k * y for x, y in zip(a, b, strict=True))


# --8<-- [start:euler]
def euler_step(field: Field, state: State, dt: float) -> State:
    """One Euler step: move for dt at the velocity you have now."""
    return _add(state, field(state), dt)
# --8<-- [end:euler]


# --8<-- [start:rk4]
def rk4_step(field: Field, state: State, dt: float) -> State:
    """One Runge-Kutta step: sample the velocity four times, average them.

    k1 is the velocity at the start; k2 and k3 are velocities half a step
    ahead; k4 is a full step ahead. The weights 1, 2, 2, 1 are what make the
    error shrink sixteen-fold when dt is halved, where Euler's only halves.
    """
    k1 = field(state)
    k2 = field(_add(state, k1, dt / 2))
    k3 = field(_add(state, k2, dt / 2))
    k4 = field(_add(state, k3, dt))
    return tuple(
        s + dt * (a + 2 * b + 2 * c + d) / 6
        for s, a, b, c, d in zip(state, k1, k2, k3, k4, strict=True)
    )
# --8<-- [end:rk4]


# --8<-- [start:integrate]
def integrate(field: Field, state: State, dt: float, steps: int,
              stepper: Stepper = rk4_step) -> list[State]:
    """Follow the flow for `steps` steps of length dt; keep every state."""
    path = [state]
    for _ in range(steps):
        state = stepper(field, state, dt)
        path.append(state)
    return path
# --8<-- [end:integrate]
