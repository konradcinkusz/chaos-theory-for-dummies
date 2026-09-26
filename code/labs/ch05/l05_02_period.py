"""Lab 5.2 -- a cycle detector of your own.

`settle` runs the logistic map from a start for a while without looking,
then keeps the values that follow. `period` reads a list of numbers and
says how often it repeats: the smallest p for which EVERY value in the
list equals the one p places further on, to within a tolerance. When no p
up to `longest` fits, it returns None -- which means "not found", never
"proved chaotic".
"""


def settle(r: float, x0: float, skip: int, keep: int) -> list[float]:
    """Take `skip` steps of r*x*(1 - x) from x0, then return the next
    `keep` values (the first of them is the value after `skip` steps)."""
    raise NotImplementedError("your turn: replace this line")


def period(xs: list[float], tol: float = 1e-9,
           longest: int = 64) -> int | None:
    """The smallest p from 1 to `longest` such that every xs[i] is within
    tol of xs[i + p]; None if no such p exists."""
    raise NotImplementedError("your turn: replace this line")
