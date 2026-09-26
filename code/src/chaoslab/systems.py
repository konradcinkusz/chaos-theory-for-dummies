"""The systems the book studies, each a rule or a field you can hand to
iterate.orbit or flows.integrate.

Maps (one step at a time) take and return a number or a pair; fields (a flow
in continuous time) take the state tuple and return its rate of change.

Most of these use only +, -, * and /. The pendulums and the sine map call
math.sin and math.cos, whose last digit is NOT guaranteed identical on every
machine -- which is harmless for a pendulum that is not chaotic and matters
for one that is. Chapter 16 is about exactly that, and code/measure/ prints
nothing from a chaotic trajectory that a one-digit difference could move.
"""

from __future__ import annotations

import math
from collections.abc import Callable

from .flows import Field, State

Map2 = Callable[[tuple[float, float]], tuple[float, float]]


# --8<-- [start:lorenz]
def lorenz(sigma: float = 10.0, rho: float = 28.0,
           beta: float = 8.0 / 3.0) -> Field:
    """Lorenz's 1963 convection model: three numbers, three rules."""

    def field(s: State) -> State:
        x, y, z = s
        return (sigma * (y - x),
                x * (rho - z) - y,
                x * y - beta * z)

    return field
# --8<-- [end:lorenz]


# --8<-- [start:spring]
def spring(k: float = 1.0) -> Field:
    """A mass on a spring: position changes at the velocity, velocity
    changes against the stretch."""

    def field(s: State) -> State:
        x, v = s
        return (v, -k * x)

    return field
# --8<-- [end:spring]


# --8<-- [start:pendulum]
def pendulum(g_over_l: float = 1.0, damping: float = 0.0) -> Field:
    """A pendulum: state (angle, angular velocity), angle in radians."""

    def field(s: State) -> State:
        theta, omega = s
        return (omega, -g_over_l * math.sin(theta) - damping * omega)

    return field
# --8<-- [end:pendulum]


def pendulum_energy(s: State, g_over_l: float = 1.0) -> float:
    """Energy of the frictionless pendulum per unit mass and length squared."""
    theta, omega = s
    return 0.5 * omega * omega + g_over_l * (1.0 - math.cos(theta))


# --8<-- [start:double]
def double_pendulum(g: float = 9.81, l1: float = 1.0, l2: float = 1.0,
                    m1: float = 1.0, m2: float = 1.0) -> Field:
    """Two pendulums, the second hung from the first.

    State (theta1, theta2, omega1, omega2), angles from the vertical.
    """

    def field(s: State) -> State:
        t1, t2, w1, w2 = s
        d = t2 - t1
        sd, cd = math.sin(d), math.cos(d)
        den1 = (m1 + m2) * l1 - m2 * l1 * cd * cd
        den2 = (l2 / l1) * den1
        a1 = (m2 * l1 * w1 * w1 * sd * cd
              + m2 * g * math.sin(t2) * cd
              + m2 * l2 * w2 * w2 * sd
              - (m1 + m2) * g * math.sin(t1)) / den1
        a2 = (-m2 * l2 * w2 * w2 * sd * cd
              + (m1 + m2) * (g * math.sin(t1) * cd
                             - l1 * w1 * w1 * sd
                             - g * math.sin(t2))) / den2
        return (w1, w2, a1, a2)

    return field
# --8<-- [end:double]


def double_pendulum_energy(s: State, g: float = 9.81, l1: float = 1.0,
                           l2: float = 1.0, m1: float = 1.0,
                           m2: float = 1.0) -> float:
    """Kinetic plus potential energy of the double pendulum."""
    t1, t2, w1, w2 = s
    kinetic = (0.5 * m1 * l1 * l1 * w1 * w1
               + 0.5 * m2 * (l1 * l1 * w1 * w1 + l2 * l2 * w2 * w2
                             + 2 * l1 * l2 * w1 * w2 * math.cos(t1 - t2)))
    potential = (-(m1 + m2) * g * l1 * math.cos(t1)
                 - m2 * g * l2 * math.cos(t2))
    return kinetic + potential


# --8<-- [start:henon]
def henon(a: float = 1.4, b: float = 0.3) -> Map2:
    """Henon's 1976 map of the plane: (x, y) -> (1 - a*x*x + y, b*x)."""

    def rule(p: tuple[float, float]) -> tuple[float, float]:
        x, y = p
        return (1.0 - a * x * x + y, b * x)

    return rule
# --8<-- [end:henon]


# --8<-- [start:lorenz96]
def lorenz96(forcing: float = 8.0) -> Field:
    """Lorenz's 1996 toy atmosphere: n numbers round a circle of latitude.

    Each one is pushed by its neighbours, damped, and driven by `forcing`.
    The number of variables is the length of the state you pass in.
    """

    def field(s: State) -> State:
        n = len(s)
        return tuple((s[(i + 1) % n] - s[i - 2]) * s[i - 1] - s[i] + forcing
                     for i in range(n))

    return field
# --8<-- [end:lorenz96]


def sine_map(s: float) -> Callable[[float], float]:
    """x -> s*sin(pi*x): a different hump from the logistic map's."""

    def rule(x: float) -> float:
        return s * math.sin(math.pi * x)

    return rule


def tent(mu: float = 2.0) -> Callable[[float], float]:
    """The tent map: up a straight slope, down the other side."""

    def rule(x: float) -> float:
        return mu * min(x, 1.0 - x)

    return rule


# --8<-- [start:doubling]
def doubling(x: float) -> float:
    """The doubling map x -> 2x mod 1: shift every binary digit left."""
    y = 2.0 * x
    return y - 1.0 if y >= 1.0 else y
# --8<-- [end:doubling]
