"""Reference solution for Lab 5.1."""


def fixed_point(r: float) -> float:
    """The value, other than zero, that r*x*(1 - x) leaves unchanged."""
    return 1.0 - 1.0 / r


def slope_at(r: float, x: float, h: float = 1e-6) -> float:
    """How much one step of the map multiplies a tiny nudge at x."""
    up = r * (x + h) * (1.0 - (x + h))
    down = r * (x - h) * (1.0 - (x - h))
    return (up - down) / (2.0 * h)


def holds(r: float) -> bool:
    """True when a nudge at the fixed point shrinks, step after step."""
    return abs(slope_at(r, fixed_point(r))) < 1.0


def lets_go(lo: float, hi: float, tol: float = 1e-9) -> float:
    """The r between lo and hi at which the fixed point stops holding."""
    while hi - lo > tol:
        mid = (lo + hi) / 2
        if holds(mid):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2
