"""Chapter 5 -- the logistic map at four settings of its one knob.

The rule is one line: multiply, subtract, multiply. Those operations are
rounded in exactly the same way on every computer, so every digit printed
here is the same wherever the listing runs.
"""
# transcript: ch05-four-rates


# --8<-- [start:rule]
def step(r: float, x: float) -> float:
    """One step of the logistic map: the next value from this one."""
    return r * x * (1.0 - x)
# --8<-- [end:rule]


# --8<-- [start:run]
def after(r: float, x0: float, skip: int, keep: int) -> list[float]:
    """Take `skip` steps from x0 without looking, then keep `keep` values."""
    x = x0
    for _ in range(skip):
        x = step(r, x)
    values = []
    for _ in range(keep):
        values.append(x)
        x = step(r, x)
    return values


def main() -> None:
    print("after 200 steps from 0.2, the next eight values:")
    for r in (2.8, 3.2, 3.5, 3.9):
        values = after(r, 0.2, 200, 8)
        print(f"r = {r}: " + " ".join(f"{v:.3f}" for v in values))
# --8<-- [end:run]


if __name__ == "__main__":
    main()
