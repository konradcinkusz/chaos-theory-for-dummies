"""Reference solution for Lab 10.2."""


def step(x: float, y: float, a: float = 1.4,
         b: float = 0.3) -> tuple[float, float]:
    """One step of Henon's map."""
    return 1.0 - a * x * x + y, b * x


def area_factor(x: float, y: float, a: float = 1.4, b: float = 0.3,
                h: float = 1e-7) -> float:
    """How much one step multiplies a tiny area near (x, y)."""
    x0, y0 = step(x, y, a, b)
    x1, y1 = step(x + h, y, a, b)
    x2, y2 = step(x, y + h, a, b)
    p, q = x1 - x0, y1 - y0          # where the side along x went
    r, s = x2 - x0, y2 - y0          # where the side along y went
    return abs(p * s - q * r) / (h * h)
