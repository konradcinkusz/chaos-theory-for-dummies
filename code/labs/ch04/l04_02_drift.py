"""Lab 4.2 -- measure how far a simulation drifts from the system.

A spring without friction keeps its energy for ever, so a simulation's
energy is a check on the simulation: any change is the simulation's own
doing. Write the energy and the drift, then use them to answer a question
the chapter leaves open: halve the step, and how many times smaller does
each method's drift become?

The spring's state is (x, v): how far it is pulled out and how fast it is
moving. Its energy is half v squared plus half x squared (the stiffness is
1, as in the chapter). It starts at (1, 0), pulled out one metre, at rest.
A stepper is a function like chaoslab's `euler_step` or `rk4_step`: give it
the rule, the state and dt, and it returns the state dt later.
"""

from chaoslab import spring

FIELD = spring(1.0)
START = (1.0, 0.0)


def spring_energy(state: tuple[float, float]) -> float:
    """Energy of motion plus energy stored in the spring."""
    raise NotImplementedError("your turn: replace this line")


def drift(stepper, dt: float, seconds: float) -> float:
    """Follow the spring from START for `seconds`, in steps of dt, with
    `stepper`; return energy at the end divided by energy at the start,
    minus one (so 0.1 means ten per cent gained)."""
    raise NotImplementedError("your turn: replace this line")


def halving(stepper, dt: float, seconds: float) -> float:
    """How many times smaller the drift over `seconds` becomes when the step
    dt is halved: drift with dt divided by drift with dt / 2."""
    raise NotImplementedError("your turn: replace this line")
