"""Chapter 17 -- holding the logistic map at a fixed point it cannot keep.

The idea of Ott, Grebogi and Yorke (1990), in its simplest setting. Leave
the map alone until its chaotic orbit passes close to the unstable fixed
point; then, at every step, change r by the small amount that cancels the
coming miss. If the change needed is bigger than you allow, do nothing and
wait.
"""
# transcript: ch17-control

from chaoslab import logistic_slope

# --8<-- [start:rule]
R0 = 3.9
TARGET = 1.0 - 1.0 / R0                # the fixed point, unstable at R0
STRETCH = logistic_slope(R0)(TARGET)   # one step multiplies a miss by this
LEVER = TARGET * (1.0 - TARGET)        # next x moves this much per unit of r


def nudge(x: float, largest: float) -> float:
    """The change to r, for this step only, that cancels the coming miss.

    Zero if the change needed is bigger than `largest`: then wait.
    """
    change = -STRETCH * (x - TARGET) / LEVER
    return change if abs(change) <= largest else 0.0
# --8<-- [end:rule]


def step(x: float, change: float) -> float:
    """One step of the logistic map with r set to R0 + change."""
    return (R0 + change) * x * (1.0 - x)


def main() -> None:
# --8<-- [start:run]
    largest = 0.01 * R0          # never more than one per cent of r
    x, biggest = 0.2, 0.0
    print("step  x             change to r")
    for n in range(301):
        change = nudge(x, largest) if n >= 100 else 0.0
        if n % 50 == 0 or abs(change) > 1e-9:
            print(f"{n:4d}  {x:.10f}  {change:+.2e}")
        biggest = max(biggest, abs(change))
        x = step(x, change)
    print(f"largest change: {100 * biggest / R0:.2f} per cent of r")
# --8<-- [end:run]


if __name__ == "__main__":
    main()
