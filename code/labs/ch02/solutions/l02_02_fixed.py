"""Reference solution for Lab 2.2."""


def fixed_point(a: float, b: float) -> float:
    """The x with a * x + b == x."""
    if a == 1.0:
        raise ValueError("x -> x + b has no single fixed point")
    return b / (1.0 - a)


def is_stable(a: float, b: float) -> bool:
    """True when a nudge away from the fixed point shrinks."""
    star = fixed_point(a, b)
    nudge = 1.0
    after = a * (star + nudge) + b - star
    return abs(after) < abs(nudge)


def steps_to_settle(a: float, b: float, x0: float, tol: float) -> int:
    """Steps from x0 until x is within `tol` of the fixed point."""
    if not is_stable(a, b):
        raise ValueError("an unstable fixed point is never approached")
    star, x, steps = fixed_point(a, b), x0, 0
    while abs(x - star) >= tol:
        x = a * x + b
        steps += 1
    return steps
