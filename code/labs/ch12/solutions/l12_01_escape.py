"""Reference solution for Lab 12.1."""

Pair = tuple[float, float]


def step(z: Pair, c: Pair) -> Pair:
    """One step of z -> z*z + c, for z = x + y i and c = a + b i."""
    x, y = z
    a, b = c
    return x * x - y * y + a, 2 * x * y + b


def escape_time(c: Pair, limit: int = 100, z: Pair = (0.0, 0.0)) -> int:
    """The step at which the length of z first exceeds 2, or `limit`."""
    for n in range(limit):
        x, y = z
        if x * x + y * y > 4.0:
            return n
        z = step(z, c)
    return limit


def in_mandelbrot(c: Pair, limit: int = 200) -> bool:
    """Does the orbit of 0 stay within 2 for `limit` steps?"""
    return escape_time(c, limit) == limit


def in_julia(start: Pair, c: Pair, limit: int = 200) -> bool:
    """For this c, does the orbit of `start` stay within 2?"""
    return escape_time(c, limit, start) == limit
