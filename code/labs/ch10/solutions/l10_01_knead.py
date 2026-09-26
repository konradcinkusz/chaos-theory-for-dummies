"""Reference solution for Lab 10.1."""


def knead(x: float) -> float:
    """Where a raisin at x ends up after one knead (stretch, then fold)."""
    stretched = 2.0 * x
    if stretched <= 1.0:
        return stretched
    return 2.0 - stretched


def kneads_until_apart(x: float, gap: float, tolerance: float) -> int:
    """How many kneads until raisins at x and x + gap are more than
    `tolerance` apart."""
    a, b = x, x + gap
    n = 0
    while abs(b - a) <= tolerance:
        a, b = knead(a), knead(b)
        n += 1
    return n
