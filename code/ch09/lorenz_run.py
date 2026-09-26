"""Chapter 9 -- Lorenz's three rules, followed with Chapter 4's RK4.

The state is three numbers and the rule says how fast each one is changing.
The run is printed every two time units, then as one letter per loop: the
wing of the butterfly each loop went round. The last line is the same start
with the heating turned down.
"""
# transcript: ch09-butterfly

from chaoslab import integrate, lorenz

# --8<-- [start:run]
DT = 0.01                        # one step is a hundredth of a time unit
field = lorenz(sigma=10.0, rho=28.0, beta=8.0 / 3.0)
path = integrate(field, (1.0, 1.0, 1.0), DT, 4000)   # forty time units
# --8<-- [end:run]


# --8<-- [start:loops]
def side(x: float) -> str:
    """Which wing the state is on: R when x is positive, L otherwise."""
    return "R" if x > 0 else "L"


def loops(path: list[tuple[float, ...]]) -> str:
    """One letter per loop: the wing at the top of each loop (z highest)."""
    out = ""
    for before, now, after in zip(path, path[1:], path[2:], strict=False):
        if before[2] < now[2] >= after[2]:
            out += side(now[0])
    return out
# --8<-- [end:loops]


def main() -> None:
    print("  time       x       y       z   wing")
    for k in range(0, 2001, 200):
        x, y, z = path[k]
        print(f"{k * DT:6.0f} {x:7.2f} {y:7.2f} {z:7.2f}   {side(x)}")
    print("loops:", loops(path[100:]))
    rest = integrate(lorenz(rho=20.0), (1.0, 1.0, 1.0), DT, 10_000)[-1]
    print("rho = 20, after 100 time units:",
          ", ".join(f"{v:.2f}" for v in rest))


if __name__ == "__main__":
    main()
