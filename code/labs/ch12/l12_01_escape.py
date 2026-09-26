"""Lab 12.1 -- escape time, by hand.

The chapter's escape time uses Python's complex numbers. Here you write it
without them: a point of the plane is a pair (x, y), meaning x + y i, and
one step of the rule z -> z*z + c is the chapter's multiplication rule
followed by an addition. Then ask the escape question both ways round: with
the start fixed at 0 and c free (the Mandelbrot question), and with c fixed
and the start free (the Julia question).
"""

Pair = tuple[float, float]


def step(z: Pair, c: Pair) -> Pair:
    """One step of z -> z*z + c, for z = x + y i and c = a + b i.

    Squaring by the multiplication rule gives (x*x - y*y) + (2*x*y) i;
    then add c, the real parts together and the imaginary parts together.
    """
    raise NotImplementedError("your turn: replace this line")


def escape_time(c: Pair, limit: int = 100, z: Pair = (0.0, 0.0)) -> int:
    """The step at which the length of z first exceeds 2, or `limit` if it
    never does in that many steps.

    Check the length BEFORE each step, as chaoslab's escape_time does, and
    compare x*x + y*y with 4 rather than taking a square root.
    """
    raise NotImplementedError("your turn: replace this line")


def in_mandelbrot(c: Pair, limit: int = 200) -> bool:
    """Does the orbit of 0 stay within 2 for `limit` steps?"""
    raise NotImplementedError("your turn: replace this line")


def in_julia(start: Pair, c: Pair, limit: int = 200) -> bool:
    """For this c, does the orbit of `start` stay within 2 for `limit`
    steps? Same rule, the other question."""
    raise NotImplementedError("your turn: replace this line")
