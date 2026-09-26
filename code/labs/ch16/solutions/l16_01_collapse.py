"""Reference solution for Lab 16.1."""


def doubling(x: float) -> float:
    """One step of the doubling map: double, and drop the whole part."""
    y = 2.0 * x
    return y - 1.0 if y >= 1.0 else y


def steps_to_zero(x: float) -> int:
    """Run the map from x and count the steps until it is exactly 0.0."""
    n = 0
    while x != 0.0:
        x = doubling(x)
        n += 1
    return n


def predicted_steps(x: float) -> int:
    """The same count, without running the map: the power of two below."""
    _, bottom = x.as_integer_ratio()
    return bottom.bit_length() - 1
