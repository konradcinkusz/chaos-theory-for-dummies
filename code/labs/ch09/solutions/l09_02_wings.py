"""Reference solution for Lab 9.2."""

State = tuple[float, float, float]


def fraction_right(path: list[State]) -> float:
    """The share of the states with x above zero."""
    return sum(1 for x, _, _ in path if x > 0) / len(path)


def mean_height(path: list[State]) -> float:
    """The average of z over every state of the run."""
    return sum(z for _, _, z in path) / len(path)
