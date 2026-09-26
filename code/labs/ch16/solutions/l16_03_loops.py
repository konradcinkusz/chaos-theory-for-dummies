"""Reference solution for Lab 16.3."""

from collections.abc import Callable


def lcg(a: int, c: int, m: int) -> Callable[[int], int]:
    """The rule x -> (a*x + c) mod m, as a function of x."""

    def rule(x: int) -> int:
        return (a * x + c) % m

    return rule


def find_loop(rule: Callable, x0) -> tuple[int, int]:
    """(steps before the loop, length of the loop) for the orbit of x0."""
    seen = {}
    x, n = x0, 0
    while x not in seen:
        seen[x] = n
        x, n = rule(x), n + 1
    return seen[x], n - seen[x]
