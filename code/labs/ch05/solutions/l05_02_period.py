"""Reference solution for Lab 5.2."""


def settle(r: float, x0: float, skip: int, keep: int) -> list[float]:
    """Take `skip` steps from x0, then return the next `keep` values."""
    x = x0
    for _ in range(skip):
        x = r * x * (1.0 - x)
    values = []
    for _ in range(keep):
        values.append(x)
        x = r * x * (1.0 - x)
    return values


def period(xs: list[float], tol: float = 1e-9,
           longest: int = 64) -> int | None:
    """The smallest p such that every xs[i] is within tol of xs[i + p]."""
    for p in range(1, min(longest, len(xs) - 1) + 1):
        if all(abs(xs[i] - xs[i + p]) < tol for i in range(len(xs) - p)):
            return p
    return None
