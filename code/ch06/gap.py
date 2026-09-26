"""Chapter 6 -- the gap between the twin runs, step by step.

Beside the measured gap is what it would be if it doubled exactly every
step. Multiplying by a power of two is exact on a computer, so that column
is the doubling rule itself, not an approximation to it.
"""
# transcript: ch06-gap

from twins import NUDGE, START, rule

from chaoslab import separation

# --8<-- [start:gap]
gaps = separation(rule, START, NUDGE, 45)

print("step         gap    if it doubled")
for n in range(0, 46, 5):
    print(f"{n:4d}   {gaps[n]:9.2e}   {NUDGE * 2**n:14.2e}")
# --8<-- [end:gap]
