"""Chapter 1 -- two cups that start one degree apart.

The question every later chapter asks, asked of the gentlest model in the
book: if you get the start slightly wrong, what happens to the error?
"""
# transcript: ch01-two-cups

from cooling_cup import next_minute


def main() -> None:
# --8<-- [start:gap]
    a, b = 90.0, 91.0
    for minute in range(31):
        if minute % 10 == 0:
            print(f"minute {minute:2d}: gap {b - a:.4f} C")
        a, b = next_minute(a), next_minute(b)
# --8<-- [end:gap]


if __name__ == "__main__":
    main()
