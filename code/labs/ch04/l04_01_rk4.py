"""Lab 4.1 -- one Runge-Kutta step, from the recipe.

A rule of change is a function `field` that takes the state -- a tuple of
numbers -- and returns how fast each number is changing right now. One RK4
step of length dt asks the rule four times:

  k1: the rates at the start;
  k2: the rates half a step ahead, if you had moved at k1;
  k3: the rates half a step ahead, if you had moved at k2;
  k4: the rates a whole step ahead, if you had moved at k3;

and then moves the whole step at the average (k1 + 2*k2 + 2*k3 + k4) / 6.
Every one of these is done number by number: `state` may hold two
numbers (a pendulum), three (the weather model of Chapter 9) or more.
"""

from collections.abc import Callable

State = tuple[float, ...]


def rk4_step(field: Callable[[State], State], state: State,
             dt: float) -> State:
    """The state one step of length dt later, by the RK4 recipe."""
    raise NotImplementedError("your turn: replace this line")
