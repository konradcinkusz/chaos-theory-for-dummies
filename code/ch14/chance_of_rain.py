"""Chapter 14 -- a chance of rain, counted off the ensemble.

Call site 0 your town, and say it rains there whenever its number is
above 5. The chance of rain is then a count: how many members rain, out
of how many members there are. The forecast is the same one that
ensemble.py scores, from the same truth and the same random nudges.
"""
# transcript: ch14-rain

import random

from ensemble import DT, State, ensemble, run, spin_up

# --8<-- [start:chance]
RAIN = 5.0   # it rains at a site whenever its number is above this


def chance(members: list[State], site: int = 0) -> float:
    """The fraction of the members in which it rains at `site`."""
    wet = sum(1 for state in members if state[site] > RAIN)
    return wet / len(members)
# --8<-- [end:chance]


def main() -> None:
# --8<-- [start:table]
    rng = random.Random(14)
    truth = spin_up()
    _, members = ensemble(truth, rng)
    print(" lead   members raining   chance   did it rain?")
    for half in range(1, 13):
        truth = run(truth, 10)
        members = [run(m, 10) for m in members]
        wet = sum(1 for m in members if m[0] > RAIN)
        rained = "yes" if truth[0] > RAIN else "no"
        print(f"{half * 10 * DT:5.1f}   {wet:7d} of {len(members)}"
              f"   {chance(members):6.0%}   {rained}")
# --8<-- [end:table]


if __name__ == "__main__":
    main()
