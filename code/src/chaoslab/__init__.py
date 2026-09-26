"""chaoslab -- the small library the listings of Chaos from Zero share.

Pure Python, no dependencies, and short enough to read in an afternoon. The
book prints most of it, a region at a time, in the chapter that first needs
each piece:

    iterate   orbit, linear, logistic, slope, cobweb, period     Chapters 2-5
    flows     euler_step, rk4_step, integrate                    Chapter 4
    systems   lorenz, pendulum, double_pendulum, henon, ...      Chapters 4-14
    measure   separation, lyapunov, horizon, box_count, ...      Chapters 6-11
    fractals  cantor, koch, escape_time, r_to_c                  Chapters 11-12
"""

from .flows import euler_step, integrate, rk4_step
from .fractals import cantor, escape_time, koch, r_to_c
from .iterate import (
    cobweb,
    linear,
    logistic,
    logistic_slope,
    orbit,
    period,
    slope,
)
from .measure import (
    box_count,
    fit_slope,
    horizon,
    lyapunov,
    lyapunov_flow,
    separation,
    steps_until_apart,
)
from .systems import (
    double_pendulum,
    double_pendulum_energy,
    doubling,
    henon,
    lorenz,
    lorenz96,
    pendulum,
    pendulum_energy,
    sine_map,
    spring,
    tent,
)

__all__ = [
    "box_count", "cantor", "cobweb", "double_pendulum",
    "double_pendulum_energy", "doubling", "escape_time", "euler_step",
    "fit_slope", "henon", "horizon", "integrate", "koch", "linear",
    "logistic", "logistic_slope", "lorenz", "lorenz96", "lyapunov",
    "lyapunov_flow", "orbit", "pendulum", "pendulum_energy", "period",
    "r_to_c", "rk4_step", "separation", "sine_map", "slope", "spring",
    "steps_until_apart", "tent",
]
