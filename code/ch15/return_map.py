"""Chapter 15 -- the return map: plot each value against the next.

A rule makes the next value from this one, so the pairs (this, next) lie on
the graph of the rule, whatever the rule is. Shuffled numbers have no rule
between neighbours, so their pairs spread over the whole square. Counting
how many little squares the pairs land in turns the picture into a number.
"""
# transcript: ch15-return-map

from twins import rule_series, shuffled


# --8<-- [start:pairs]
def return_pairs(xs: list[float]) -> list[tuple[float, float]]:
    """Each value paired with the one after it."""
    return list(zip(xs[:-1], xs[1:], strict=True))


def squares_touched(xs: list[float], k: int = 10) -> int:
    """Cut the unit square into k by k little squares; count how many
    of them the return map lands in."""

    def box(v: float) -> int:
        return min(k - 1, max(0, int(v * k)))

    return len({(box(a), box(b)) for a, b in return_pairs(xs)})
# --8<-- [end:pairs]


def main() -> None:
    rule = rule_series()
    # --8<-- [start:count]
    print("values  rule  shuffled   (of 100 squares)")
    for n in (100, 500, 2000):
        part = rule[:n]
        print(f"{n:6d}  {squares_touched(part):4d}  "
              f"{squares_touched(shuffled(part)):8d}")
    # --8<-- [end:count]


if __name__ == "__main__":
    main()
