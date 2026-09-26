"""Reference solution for Lab 3.1."""


def slope(f, x: float, h: float = 1e-6) -> float:
    """How much one step of f multiplies a tiny nudge at x."""
    return (f(x + h) - f(x - h)) / (2 * h)


def fixed_points(r: float) -> list[float]:
    """The two fixed points of x -> r*x*(1 - x), smaller first."""
    return sorted([0.0, 1 - 1 / r])


def is_stable(f, x: float) -> bool:
    """True when a tiny nudge away from the fixed point x of f shrinks."""
    return abs(slope(f, x)) < 1
