"""Lab 13.2 -- when do two releases part?

Write the function the chapter's listing only printed: step two double
pendulums side by side with RK4 and report the first moment their angles
differ by more than `tol` radians (the larger of the two angle gaps, as in
the chapter's gap()). If they are still together after `limit` seconds,
return None rather than a time.

Use chaoslab's rule and stepper:

    from chaoslab import double_pendulum, rk4_step
    rule = double_pendulum()
    state = rk4_step(rule, state, dt)

Then use it to answer the question the chapter leaves you: releases a
billionth of a radian apart take how much longer to part than releases a
millionth apart?
"""

from __future__ import annotations


def seconds_until_apart(first: tuple[float, ...],
                        second: tuple[float, ...],
                        tol: float = 0.1, dt: float = 0.001,
                        limit: float = 30.0) -> float | None:
    """Seconds until the two pendulums differ by more than tol, or None."""
    raise NotImplementedError("your turn: replace this line")
