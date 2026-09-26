"""Chapter 7 -- how much one step stretches a tiny gap.

Two runs of the logistic map at r = 4 start a hair apart. At every step
the gap between them is multiplied by some factor. This listing prints
that factor beside the slope of the rule at the point the first run is on,
and the two columns agree: the stretch of one step IS the slope there.
"""
# transcript: ch07-stretch

# --8<-- [start:rule]
def step(r: float, x: float) -> float:
    """One step of the logistic map."""
    return r * x * (1.0 - x)


def stretch(r: float, x: float) -> float:
    """How much one step multiplies a tiny nudge at x: the slope there."""
    return r * (1.0 - 2.0 * x)
# --8<-- [end:rule]


def factors(r: float, x0: float, delta: float, n: int) -> list[float]:
    """By how much the gap between two runs delta apart grows, step by
    step, for n steps."""
    a, b = x0, x0 + delta
    out = []
    for _ in range(n):
        na, nb = step(r, a), step(r, b)
        out.append(abs(nb - na) / abs(b - a))
        a, b = na, nb
    return out


def main() -> None:
    # --8<-- [start:table]
    r, a, b = 4.0, 0.3, 0.3 + 1e-10
    print("step     x     gap grew by   slope there")
    for n in range(1, 9):
        grew = abs(step(r, b) - step(r, a)) / abs(b - a)
        print(f"{n:4d}   {a:.3f}   {grew:10.3f}   {abs(stretch(r, a)):10.3f}")
        a, b = step(r, a), step(r, b)
    # --8<-- [end:table]


if __name__ == "__main__":
    main()
