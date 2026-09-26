"""Lab 17.1 -- a small-nudge controller for the logistic map.

The chapter's rule, for any r0 at which the fixed point 1 - 1/r0 has
become unstable. Near the fixed point one step multiplies a miss by the
slope r0*(1 - 2x) there, and changing r by a small amount dr moves the next
value by dr * x*(1 - x). Choose dr so the two cancel -- but only if the dr
needed is no bigger than `largest`; otherwise leave r alone and wait.
"""


def nudge(x: float, r0: float, largest: float) -> float:
    """The change to r, for this step only, that cancels the coming miss.

    Return 0.0 when the change needed is bigger than `largest`.
    """
    raise NotImplementedError("your turn: replace this line")


def hold(x0: float, r0: float, steps: int,
         largest: float) -> tuple[list[float], list[float]]:
    """Run `steps` steps from x0 with the controller on from the start.

    Return (xs, changes): xs has steps + 1 entries, the start and every
    step after it; changes has `steps` entries, the nudge used at each step.
    """
    raise NotImplementedError("your turn: replace this line")
