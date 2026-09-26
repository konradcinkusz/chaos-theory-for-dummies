"""Chapter 3 -- one bacterium, doubling every twenty minutes, weighed.

Growth in proportion to what is already there: every cell becomes two, so
the colony is multiplied by the same factor at every step. Counted with
whole numbers, so the count is exact however large it gets.
"""
# transcript: ch03-doubling

# --8<-- [start:grow]
CELL = 1e-12       # grams: one E. coli bacterium weighs about a picogram
EARTH = 5.97e27    # grams: the mass of the Earth
MINUTES = 20       # one doubling, in a warm dish with food to spare


def doublings_to_outweigh(target: float) -> int:
    """How many doublings until a colony grown from a single cell weighs
    more than `target` grams."""
    cells, n = 1, 0
    while cells * CELL <= target:
        cells = 2 * cells
        n = n + 1
    return n
# --8<-- [end:grow]


def main() -> None:
# --8<-- [start:table]
    print("hours      cells      grams")
    for hours in range(0, 48, 8):
        cells = 2 ** (hours * 60 // MINUTES)
        print(f"{hours:5d}  {cells:9.1e}  {cells * CELL:9.1e}")
    n = doublings_to_outweigh(EARTH)
    print(f"heavier than the Earth after {n} doublings,"
          f" {n * MINUTES / 60:.1f} hours")
# --8<-- [end:table]


if __name__ == "__main__":
    main()
