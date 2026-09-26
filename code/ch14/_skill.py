"""Chapter 14 helper -- scores averaged over many forecasts.

Imported by code/measure/ch14.py and code/plots/ch14.py, so the numbers
on the page and the curves in the figure come from one computation. The
truths are one long run of the model, sampled every GAP steps; the
nudges come from a seeded generator, so every forecast is the same on
every machine.
"""

import random

from ensemble import DT, State, error, forecast, perturb, run, spin_up

CASES = 40    # forecasts averaged over
GAP = 100     # steps between one forecast's start and the next


def truths(cases: int = CASES) -> list[State]:
    """The starting truths: one long run, sampled every GAP steps."""
    state, out = spin_up(), []
    for _ in range(cases):
        state = run(state, GAP)
        out.append(state)
    return out


def average_scores(steps: int = 160, seed: int = 1400) -> tuple[
        list[float], list[float], list[float], list[float]]:
    """Leads, and the spread, error of the mean and error of one run,
    each averaged over CASES forecasts, at every step up to `steps`."""
    rng = random.Random(seed)
    sums = [[0.0, 0.0, 0.0] for _ in range(steps + 1)]
    for truth in truths():
        rows = forecast(truth, rng, range(steps + 1))
        for k, (_, sp, e_mean, e_one) in enumerate(rows):
            sums[k][0] += sp
            sums[k][1] += e_mean
            sums[k][2] += e_one
    leads = [k * DT for k in range(steps + 1)]
    return (leads, [s[0] / CASES for s in sums],
            [s[1] / CASES for s in sums], [s[2] / CASES for s in sums])


def single_errors(size: float, steps: int = 240,
                  seed: int = 1402) -> list[float]:
    """The error of one run from an analysis wrong by up to `size`,
    averaged over the same CASES truths, at every step."""
    rng = random.Random(seed)
    sums = [0.0] * (steps + 1)
    for truth in truths():
        one = perturb(truth, size, rng)
        for k in range(steps + 1):
            sums[k] += error(one, truth)
            one, truth = run(one, 1), run(truth, 1)
    return [s / CASES for s in sums]
