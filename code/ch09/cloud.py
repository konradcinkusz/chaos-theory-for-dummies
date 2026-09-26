"""Chapter 9 -- eight starts far outside the butterfly, all pulled onto it.

Each start is a corner of a box eighty wide. Each run is followed for fifty
time units, the first five are ignored, and the program prints the largest
size x reached and the lowest and highest z: the room the run lived in.
"""
# transcript: ch09-cloud

from chaoslab import integrate, lorenz

# --8<-- [start:cloud]
field = lorenz()
corners = [(x, y, z) for x in (-40.0, 40.0) for y in (-40.0, 40.0)
           for z in (-40.0, 80.0)]
# --8<-- [end:cloud]


def room(start: tuple[float, float, float]) -> tuple[float, float, float]:
    """Largest |x|, lowest z and highest z, from time 5 to time 50."""
    path = integrate(field, start, 0.01, 5000)[500:]
    return (max(abs(p[0]) for p in path), min(p[2] for p in path),
            max(p[2] for p in path))


def main() -> None:
    print("start                  largest |x|   lowest z   highest z")
    for start in corners:
        big, low, high = room(start)
        label = "(" + ", ".join(f"{v:.0f}" for v in start) + ")"
        print(f"{label:22} {big:10.1f} {low:10.1f} {high:11.1f}")


if __name__ == "__main__":
    main()
