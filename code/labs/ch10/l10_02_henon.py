"""Lab 10.2 -- one step of Henon's map, and what it does to an area.

The rule, from the chapter: (x, y) goes to (1 - a*x*x + y, b*x).
For the area, put a tiny square of side h with one corner at (x, y), move
its three corners (x, y), (x + h, y) and (x, y + h) one step, and read off
the two sides of the new, slanted shape as arrows (p, q) and (r, s). The
area of that parallelogram is |p*s - q*r|; divide by h*h to get the factor
by which one step multiplies areas near (x, y).
"""


def step(x: float, y: float, a: float = 1.4,
         b: float = 0.3) -> tuple[float, float]:
    """One step of Henon's map."""
    raise NotImplementedError("your turn: replace this line")


def area_factor(x: float, y: float, a: float = 1.4, b: float = 0.3,
                h: float = 1e-7) -> float:
    """How much one step multiplies a tiny area near (x, y)."""
    raise NotImplementedError("your turn: replace this line")
