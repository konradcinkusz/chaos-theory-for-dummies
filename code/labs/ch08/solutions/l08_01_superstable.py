"""Reference solution for Lab 8.1."""


def from_top(r: float, steps: int) -> float:
    """How far from 0.5 the logistic map is after `steps` steps from 0.5."""
    x = 0.5
    for _ in range(steps):
        x = r * x * (1.0 - x)
    return x - 0.5


def bisect(g, lo: float, hi: float, rounds: int = 60) -> float:
    """A point between lo and hi where g changes sign."""
    below = g(lo) < 0
    for _ in range(rounds):
        mid = (lo + hi) / 2
        if (g(mid) < 0) == below:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def superstable(steps: int, lo: float, hi: float) -> float:
    """The r between lo and hi at which 0.5 returns to 0.5 after `steps`."""
    return bisect(lambda r: from_top(r, steps), lo, hi)
