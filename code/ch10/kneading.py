"""Chapter 10 -- kneading dough on a line: stretch, then fold.

A strip of dough one unit long; a raisin at position x. One knead rolls the
strip out to twice its length and folds the part that sticks out past the
end back on top of the rest. That is the tent map, and it uses only doubling
and subtraction, so every digit printed here is the same on every machine.
"""
# transcript: ch10-kneading


# --8<-- [start:knead]
def knead(x: float) -> float:
    """One knead: stretch the strip to twice its length, then fold."""
    stretched = 2.0 * x
    if stretched <= 1.0:
        return stretched          # still on the strip: nothing to fold
    return 2.0 - stretched        # past the end: fold it back


def main() -> None:
    a, b = 0.2345, 0.2355        # two raisins a thousandth apart
    print("knead  raisin A  raisin B     gap")
    for n in range(14):
        print(f"{n:5d}  {a:8.4f}  {b:8.4f}  {abs(b - a):6.4f}")
        a, b = knead(a), knead(b)
# --8<-- [end:knead]


if __name__ == "__main__":
    main()
