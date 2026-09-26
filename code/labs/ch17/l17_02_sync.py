"""Lab 17.2 -- how long does the driven copy take to fall into step?

The original is the Lorenz system (sigma = 10, rho = 28, beta = 8/3). The
copy has its own y2 and z2, obeying the same rules as y and z, but it is
handed the original's x instead of having one of its own. The state is the
five numbers (x, y, z, y2, z2). `start` is written for you: the original
settled on its attractor, the copy's y2 and z2 at zero.
"""

from chaoslab import lorenz, rk4_step

SIGMA, RHO, BETA = 10.0, 28.0, 8.0 / 3.0


def start(dt: float = 0.01) -> tuple[float, ...]:
    """The original after 2000 steps from (1, 1, 1); the copy at zero."""
    s = (1.0, 1.0, 1.0)
    field = lorenz(SIGMA, RHO, BETA)
    for _ in range(2000):
        s = rk4_step(field, s, dt)
    return s + (0.0, 0.0)


def copy_field(s: tuple[float, ...]) -> tuple[float, ...]:
    """How fast each of (x, y, z, y2, z2) is changing, as five numbers."""
    raise NotImplementedError("your turn: replace this line")


def error(s: tuple[float, ...]) -> float:
    """The distance between the copy (y2, z2) and the original's (y, z)."""
    raise NotImplementedError("your turn: replace this line")


def sync_time(tol: float, dt: float = 0.01, limit: float = 100.0) -> float:
    """The first time, in steps of dt from `start`, at which error < tol.

    Step the five numbers together with rk4_step and copy_field.
    """
    raise NotImplementedError("your turn: replace this line")
