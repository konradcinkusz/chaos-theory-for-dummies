"""Chapter 10 -- Henon's map: two numbers, one line of arithmetic each.

Michel Henon published it in 1976 as a stripped-down picture of what
Lorenz's equations do. The state is a point (x, y) of the plane; one step
bends, squeezes and swaps it. Only +, - and *, so every digit is the same
on every machine however long the run.
"""
# transcript: ch10-henon

# --8<-- [start:rule]
A = 1.4   # how hard each step bends
B = 0.3   # how hard each step squeezes


def henon(x: float, y: float) -> tuple[float, float]:
    """One step of Henon's map."""
    return 1.0 - A * x * x + y, B * x
# --8<-- [end:rule]


def main() -> None:
    x, y = 0.0, 0.0
    print("step        x        y")
    for n in range(9):
        print(f"{n:4d}  {x:7.4f}  {y:7.4f}")
        x, y = henon(x, y)


if __name__ == "__main__":
    main()
