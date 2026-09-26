"""Lab 10.1 -- kneading dough on a line.

The strip of dough runs from 0 to 1 and a raisin sits at x. One knead
stretches the strip to twice its length and folds whatever sticks out past
1 back on top: double x, and if the result is past 1, take it from 2.
Write the knead, then ask how many kneads it takes before two raisins that
start very close together are far apart.
"""


def knead(x: float) -> float:
    """Where a raisin at x ends up after one knead (stretch, then fold)."""
    raise NotImplementedError("your turn: replace this line")


def kneads_until_apart(x: float, gap: float, tolerance: float) -> int:
    """How many kneads until raisins at x and x + gap are more than
    `tolerance` apart. Count the kneads; the start itself is knead 0."""
    raise NotImplementedError("your turn: replace this line")
