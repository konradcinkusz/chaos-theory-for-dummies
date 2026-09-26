"""Chapter 4 helper -- a rule whose motion settles onto a loop.

Balthasar van der Pol's oscillator: a pull back to the middle, plus a push
that feeds energy in while the swing is small and takes it out while the
swing is large. Imported by the chapter's measurement and plot scripts;
the page states the rule in words.
"""

from chaoslab.flows import Field, State

MU = 1.0   # how hard the push and the brake act


def van_der_pol(mu: float = MU) -> Field:
    """State (x, v): x moves at v; v is pulled back by x and pushed by
    (1 - x*x) * v, which speeds up small swings and slows large ones."""

    def field(s: State) -> State:
        x, v = s
        return (v, -x + mu * (1.0 - x * x) * v)

    return field


def swing(path: list[State], last: int) -> float:
    """How far out the motion reaches over the last `last` states."""
    return max(abs(s[0]) for s in path[-last:])
