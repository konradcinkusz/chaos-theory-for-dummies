"""Reference solution for Lab 15.1."""


def return_pairs(xs: list[float]) -> list[tuple[float, float]]:
    """Each value paired with the one after it: (x0, x1), (x1, x2), ..."""
    return list(zip(xs[:-1], xs[1:], strict=True))


def squares_touched(xs: list[float], k: int = 10) -> int:
    """How many of the k by k little squares the return map lands in."""

    def box(v: float) -> int:
        return min(k - 1, max(0, int(v * k)))

    return len({(box(a), box(b)) for a, b in return_pairs(xs)})


def verdict(xs: list[float], k: int = 10) -> str:
    """"curve" if fewer than half the squares are touched, else "cloud"."""
    return "curve" if squares_touched(xs, k) < k * k / 2 else "cloud"
