"""Chapter 2 -- one tablet every morning.

The state is the amount of the drug in the blood, in milligrams, just after
the morning's tablet. By the next morning the body has cleared half of it,
and then the next tablet adds 100 mg: the rule is x -> 0.5 * x + 100.
"""
# transcript: ch02-drug

from chaoslab import linear, orbit

# --8<-- [start:tablets]
KEPT = 0.5      # the fraction of yesterday's drug still in the blood
DOSE = 100.0    # milligrams in one tablet
tablets = linear(KEPT, DOSE)
steady = DOSE / (1.0 - KEPT)    # the fixed point: solve x = 0.5x + 100


def main() -> None:
    print("day   in blood   short of the fixed point")
    for day, x in enumerate(orbit(tablets, DOSE, 8)):
        print(f"{day:3d}   {x:8.2f}   {steady - x:8.2f}")
# --8<-- [end:tablets]


if __name__ == "__main__":
    main()
