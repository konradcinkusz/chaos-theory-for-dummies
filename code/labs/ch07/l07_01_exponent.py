"""Lab 7.1 -- the Lyapunov exponent of the logistic map, from its orbit.

`stretch` is how much one step of the map x -> r*x*(1 - x) multiplies a
tiny nudge at x: the slope of the rule there, r*(1 - 2x). `exponent` follows
an orbit, lets it settle for `burn` steps, and then averages the natural
logarithm of the SIZE of the stretch at each of the next `steps` points.
Python's math.log is the natural logarithm, and abs() gives the size.
"""


def stretch(r: float, x: float) -> float:
    """The slope of the logistic map at x: r*(1 - 2x)."""
    raise NotImplementedError("your turn: replace this line")


def exponent(r: float, x0: float = 0.3, steps: int = 100_000,
             burn: int = 1000) -> float:
    """The average of ln|stretch(r, x)| over `steps` points of the orbit
    from x0, after throwing away the first `burn` steps."""
    raise NotImplementedError("your turn: replace this line")
