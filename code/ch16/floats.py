"""Chapter 16 -- what a computer actually stores for 0.1.

Python's float is a "double": a number kept to 53 significant binary digits.
Most decimal fractions have no exact binary form, so they are rounded on the
way in, and every sum and product is rounded again on the way out.
"""
# transcript: ch16-floats

from decimal import Decimal


def main() -> None:
    print(0.1 + 0.2)
    print(0.1 + 0.2 == 0.3)
    print(Decimal(0.1))              # the exact value stored for 0.1
    print((0.1).as_integer_ratio())  # the same number as a fraction
    print(2**55)                     # the bottom of that fraction
    print((0.1 + 0.2) + 0.3, 0.1 + (0.2 + 0.3))
    big = float(2**53)
    print(big + 1.0 == big)          # 2**53 + 1 has no room to be stored


if __name__ == "__main__":
    main()
