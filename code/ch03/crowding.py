"""Chapter 3 -- doubling, and doubling with the room running out.

x is the population as a fraction of the most the place could ever hold:
0 is empty, 1 is every scrap of food and space taken. With room to spare
each individual leaves r offspring; the factor (1 - x), the room still
free, scales that down as the place fills.
"""
# transcript: ch03-crowding

# --8<-- [start:rule]
def next_gen(x: float, r: float) -> float:
    """The next generation, as a fraction of the room: r * x is what the
    population would breed with room to spare, and (1 - x) is the share
    of the room still free."""
    return r * x * (1 - x)
# --8<-- [end:rule]


def main() -> None:
    # --8<-- [start:run]
    r = 2.0
    free = crowded = 0.001
    print("gen  doubling  crowded")
    for gen in range(15):
        print(f"{gen:3d}  {free:8.4f}  {crowded:7.4f}")
        free = r * free
        crowded = next_gen(crowded, r)
    # --8<-- [end:run]


if __name__ == "__main__":
    main()
