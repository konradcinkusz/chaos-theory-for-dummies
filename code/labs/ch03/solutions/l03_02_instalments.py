"""Reference solution for Lab 3.2."""


def next_gen(x: float, r: float) -> float:
    """The crowding rule: r * x times the share of room still free."""
    return r * x * (1 - x)


def in_instalments(x: float, r: float, k: int) -> float:
    """One generation of the crowding rule, paid in k instalments."""
    for _ in range(k):
        x = x + (next_gen(x, r) - x) / k
    return x


def run(r: float, k: int, x0: float, generations: int) -> list[float]:
    """The population at the end of each generation, starting with x0."""
    xs = [x0]
    for _ in range(generations):
        xs.append(in_instalments(xs[-1], r, k))
    return xs


def overshoots(r: float, k: int, x0: float = 0.01,
               generations: int = 100) -> bool:
    """True if the population ever passes its settled level by more than
    a millionth."""
    level = 1 - 1 / r
    return any(x > level + 1e-6 for x in run(r, k, x0, generations))
