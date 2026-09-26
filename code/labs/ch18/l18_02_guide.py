"""Lab 18.2 -- the field guide, run on a model.

The chapter's first three questions, turned into code you can point at any
rule that takes a number and returns the next one:

  1. does a small change in the start grow?
  2. how fast -- what is its growth rate per step?
  3. what is predictable anyway -- how often does a long run visit a range?

The test checks your functions on Chapter 1's cooling tea and on the
logistic map. Then write a rule of your own at the bottom of this file (a
tent map, a sine map, a population with a harvest) and ask it all three.
"""

import math  # noqa: F401 -- you will need it
from collections.abc import Callable

Rule = Callable[[float], float]


def error_grows(rule: Rule, x0: float, delta: float = 1e-9,
                steps: int = 30) -> bool:
    """Run two copies from x0 and x0 + delta. True if after `steps` steps
    they are further apart than delta was."""
    raise NotImplementedError("your turn: replace this line")


def growth_rate(rule: Rule, x0: float, delta: float = 1e-12,
                steps: int = 20) -> float:
    """The average growth of the gap per step: ln(gap after `steps` steps
    divided by delta), divided by `steps`. Positive if the gap grows."""
    raise NotImplementedError("your turn: replace this line")


def long_run_fraction(rule: Rule, x0: float, low: float, high: float,
                      steps: int = 100_000) -> float:
    """The fraction of `steps` steps, starting from x0, at which the state
    lies in the range low <= x < high."""
    raise NotImplementedError("your turn: replace this line")
