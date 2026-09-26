"""Reference solution for Lab 17.1."""


def nudge(x: float, r0: float, largest: float) -> float:
    """The change to r, for this step only, that cancels the coming miss.

    Return 0.0 when the change needed is bigger than `largest`.
    """
    target = 1.0 - 1.0 / r0
    stretch = r0 * (1.0 - 2.0 * target)
    lever = target * (1.0 - target)
    change = -stretch * (x - target) / lever
    return change if abs(change) <= largest else 0.0


def hold(x0: float, r0: float, steps: int,
         largest: float) -> tuple[list[float], list[float]]:
    """Run `steps` steps from x0 with the controller on from the start."""
    xs, changes = [x0], []
    x = x0
    for _ in range(steps):
        change = nudge(x, r0, largest)
        x = (r0 + change) * x * (1.0 - x)
        xs.append(x)
        changes.append(change)
    return xs, changes
