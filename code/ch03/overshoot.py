"""Chapter 3 -- the same law of growth, applied once a generation and in
ten small instalments.

Both populations change by the same law: over a whole generation, by
next_gen(x, r) - x. The only difference is how often the population looks
at how crowded it is while it changes.
"""
# transcript: ch03-overshoot

from crowding import next_gen


# --8<-- [start:instalments]
def in_instalments(x: float, r: float, k: int = 10) -> float:
    """One generation of the crowding rule, paid in k instalments, each
    worked out from the population as it stands after the one before."""
    for _ in range(k):
        x = x + (next_gen(x, r) - x) / k
    return x
# --8<-- [end:instalments]


def compare(r: float, generations: range) -> None:
    """Both populations from the same small start; print the generations
    asked for."""
    # --8<-- [start:compare]
    once = paid = 0.01
    print(f"r = {r}, settled level {1 - 1 / r:.4f}")
    print("gen    once  in ten")
    for gen in range(generations.stop):
        if gen in generations:
            print(f"{gen:3d}  {once:.4f}  {paid:.4f}")
        once = next_gen(once, r)
        paid = in_instalments(paid, r)
    # --8<-- [end:compare]


def main() -> None:
    compare(2.8, range(15))


if __name__ == "__main__":
    main()
