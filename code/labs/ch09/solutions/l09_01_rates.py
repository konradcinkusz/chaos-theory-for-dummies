"""Reference solution for Lab 9.1."""

import math

State = tuple[float, float, float]

SIGMA, RHO, BETA = 10.0, 28.0, 8.0 / 3.0


def rates(state: State, sigma: float = SIGMA, rho: float = RHO,
          beta: float = BETA) -> State:
    """(how fast x, y and z are changing) at `state`."""
    x, y, z = state
    return (sigma * (y - x), x * (rho - z) - y, x * y - beta * z)


def fixed_points(rho: float = RHO, beta: float = BETA) -> list[State]:
    """Every state at which nothing changes, rest state first."""
    points = [(0.0, 0.0, 0.0)]
    if rho > 1:
        s = math.sqrt(beta * (rho - 1))
        points += [(s, s, rho - 1), (-s, -s, rho - 1)]
    return points
