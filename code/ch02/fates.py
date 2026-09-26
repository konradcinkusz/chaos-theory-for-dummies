"""Chapter 2 -- four straight-line rules, run side by side.

Each rule multiplies by a fixed number and then adds a fixed number. Started
from the same place, they meet different fates: one grows without bound,
one shrinks to nothing, and two settle on the same number -- one of them
from alternate sides.
"""
# transcript: ch02-fates

from chaoslab import linear, orbit

# --8<-- [start:rules]
RULES = {
    "2x": linear(2.0, 0.0),           # multiply by 2
    "0.5x": linear(0.5, 0.0),         # multiply by 0.5
    "0.5x+5": linear(0.5, 5.0),       # multiply by 0.5, add 5
    "-0.5x+15": linear(-0.5, 15.0),   # multiply by -0.5, add 15
}


def main() -> None:
    runs = [orbit(rule, 1.0, 8) for rule in RULES.values()]
    print(" n" + "".join(f"{name:>11}" for name in RULES))
    for n in range(9):
        print(f"{n:2d}" + "".join(f"{run[n]:11.4f}" for run in runs))
# --8<-- [end:rules]


if __name__ == "__main__":
    main()
