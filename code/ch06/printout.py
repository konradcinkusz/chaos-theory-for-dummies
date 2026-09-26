"""Chapter 6 -- Lorenz's printout, reproduced on the logistic map.

The machine held 0.506127 and the printout showed 0.506. Run once from the
full number, again from the full number, and once from the printout, and
compare the second and third runs with the first.
"""
# transcript: ch06-printout

from twins import rule

from chaoslab import orbit

# --8<-- [start:printout]
FULL = 0.506127    # what the machine held
PRINTED = 0.506    # what the printout showed: three decimal places

first = orbit(rule, FULL, 20)
again = orbit(rule, FULL, 20)       # the same start, typed in full
rounded = orbit(rule, PRINTED, 20)  # the start copied off the printout
# --8<-- [end:printout]


def main() -> None:
    print("step     first     again   rounded")
    for n in range(0, 21, 2):
        print(f"{n:4d}  {first[n]:8.6f}  {again[n]:8.6f}  {rounded[n]:8.6f}")
    print("again == first, every digit of every step:", again == first)


if __name__ == "__main__":
    main()
