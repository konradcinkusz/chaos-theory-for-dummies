"""Chapter 12 -- the rule z -> z*z + c, run from z = 0, for five values of c.

Four of them are ordinary numbers on a line. The last, c = i, is a point off
the line, and Python carries it with no extra work.
"""
# transcript: ch12-orbits


# --8<-- [start:orbit]
def orbit_of_zero(c: complex, steps: int) -> list[complex]:
    """0, then z*z + c applied again and again: steps + 1 values."""
    zs = [0j]
    for _ in range(steps):
        z = zs[-1]
        zs.append(z * z + c)
    return zs
# --8<-- [end:orbit]


def show(z: complex) -> str:
    """A value short enough for a column: 2, 0.3477, -1+1i, -1i."""
    x, y = z.real, z.imag
    if y == 0:
        return f"{x:.4g}"
    if x == 0:
        return f"{y:.4g}i"
    return f"{x:.4g}{y:+.4g}i"


def main() -> None:
# --8<-- [start:table]
    for label, c in [("1", 1), ("-1", -1), ("0.25", 0.25),
                     ("-2", -2), ("i", 1j)]:
        zs = orbit_of_zero(c, 5)
        print(f"c = {label:>4}: " + "".join(f"{show(z):>9}" for z in zs))
# --8<-- [end:table]


if __name__ == "__main__":
    main()
