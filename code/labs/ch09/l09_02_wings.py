"""Lab 9.2 -- two numbers the start does not decide.

A run of Lorenz's rules is a list of states (x, y, z), one per step. Where
the run is at any one moment depends on its start. These two summaries of
the whole run do not -- which is what your test checks, on two runs from
two very different starts.
"""

State = tuple[float, float, float]


def fraction_right(path: list[State]) -> float:
    """The share of the states with x above zero: the fraction of the time
    spent on the right-hand wing of the butterfly."""
    raise NotImplementedError("your turn: replace this line")


def mean_height(path: list[State]) -> float:
    """The average of z over every state of the run."""
    raise NotImplementedError("your turn: replace this line")
