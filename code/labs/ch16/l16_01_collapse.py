"""Lab 16.1 -- predict when the doubling map dies on a computer.

The doubling map x -> 2x mod 1 shifts every binary digit one place left and
throws away the one that crosses the point. A double is a whole number
divided by a power of two, so its binary digits run out, and then the orbit
is exactly 0 for ever. Write one function that COUNTS the steps by running
the map, and one that PREDICTS the count without running it.
"""


def doubling(x: float) -> float:
    """One step of the doubling map: double, and drop the whole part."""
    raise NotImplementedError("your turn: replace this line")


def steps_to_zero(x: float) -> int:
    """Run the map from x and count the steps until it is exactly 0.0.

    Start with 0 if x is already 0.0.
    """
    raise NotImplementedError("your turn: replace this line")


def predicted_steps(x: float) -> int:
    """The same count, without running the map.

    Hint: x.as_integer_ratio() gives (top, bottom) with bottom a power of
    two, 2**k. How many steps does it take to push k binary digits out?
    """
    raise NotImplementedError("your turn: replace this line")
