"""Lab 9.1 -- Lorenz's three rules, in your own hand.

`rates` takes the state (x, y, z) and returns how fast each of the three is
changing, by the chapter's three rules:

    x changes at  sigma * (y - x)
    y changes at  x * (rho - z) - y
    z changes at  x * y - beta * z

`still_points` returns every state at which all three rates are zero: the
pan at rest and, when the heating rho is above 1, the two steady rolls.
"""

State = tuple[float, float, float]

SIGMA, RHO, BETA = 10.0, 28.0, 8.0 / 3.0


def rates(state: State, sigma: float = SIGMA, rho: float = RHO,
          beta: float = BETA) -> State:
    """(how fast x, y and z are changing) at `state`."""
    raise NotImplementedError("your turn: replace this line")


def still_points(rho: float = RHO, beta: float = BETA) -> list[State]:
    """Every state at which nothing changes, rest state first.

    One state when rho is 1 or less. Above 1, also the two steady rolls,
    x = y = plus or minus the square root of beta * (rho - 1), z = rho - 1:
    the one turning with x positive, then the one with x negative.
    """
    raise NotImplementedError("your turn: replace this line")
