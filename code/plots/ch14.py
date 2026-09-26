"""Chapter 14's plots: an ensemble plume, spread and skill against lead
time, and the climate of the toy atmosphere under two forcings."""

from __future__ import annotations

import random
import sys
from functools import cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch14"))

import numpy as np
from _skill import average_scores
from _style import AMBER, BLUE, GREY, RED, TEAL, T, main, new, plot
from chance_of_rain import RAIN
from climate import HOT
from ensemble import DT, FORCING, ensemble, run, spin_up


@plot("ch14-plume")
def plume(lang: str):
    fig, ax = new(height=2.7)
    rng = random.Random(14)             # the forecast of the two listings
    truth = spin_up()
    _, members = ensemble(truth, rng)
    steps = 120
    paths = [[m[0]] for m in members]
    truth_path = [truth[0]]
    for _ in range(steps):
        members = [run(m, 1) for m in members]
        truth = run(truth, 1)
        for path, m in zip(paths, members, strict=True):
            path.append(m[0])
        truth_path.append(truth[0])
    leads = [k * DT for k in range(steps + 1)]
    for k, path in enumerate(paths):
        ax.plot(leads, path, color=BLUE, lw=0.5, alpha=0.55,
                label=T(lang, "the twenty members", "dwadzieścia członków")
                if k == 0 else None)
    ax.plot(leads, truth_path, color=AMBER, lw=1.8,
            label=T(lang, "the truth", "prawda"))
    ax.axhline(RAIN, color=GREY, lw=0.7, ls="--")
    ax.text(2.05, RAIN + 0.4, T(lang, "rain above this line",
                               "powyżej tej linii pada"),
            color=GREY, fontsize=8)
    ax.set_xlabel(T(lang, "lead time (model time units)",
                    "wyprzedzenie (jednostki czasu modelu)"))
    ax.set_ylabel(T(lang, "the number at site 0", "liczba w punkcie 0"))
    ax.legend(loc="lower left", frameon=False)
    fig.tight_layout()
    return fig


@plot("ch14-skill")
def skill(lang: str):
    fig, ax = new(height=2.8)
    leads, sp, e_mean, e_one = _scores()
    swing = float(np.std(_samples(FORCING, 0.01)))
    ax.plot(leads, e_one, color=RED,
            label=T(lang, "error of one run", "błąd jednego przebiegu"))
    ax.plot(leads, e_mean, color=BLUE,
            label=T(lang, "error of the ensemble mean",
                    "błąd średniej zespołu"))
    ax.plot(leads, sp, color=TEAL, ls="--",
            label=T(lang, "spread of the ensemble", "rozrzut zespołu"))
    ax.axhline(swing, color=GREY, lw=0.8, ls=":",
               label=T(lang, "error of always saying the average",
                       "błąd mówienia zawsze średniej"))
    ax.set_xlabel(T(lang, "lead time (model time units)",
                    "wyprzedzenie (jednostki czasu modelu)"))
    ax.set_ylabel(T(lang, "typical size", "typowa wielkość"))
    ax.set_ylim(0, 6)
    ax.legend(loc="upper left", frameon=False)
    fig.tight_layout()
    return fig


@cache
def _scores():
    return average_scores()


@cache
def _samples(forcing: float, nudge: float, steps: int = 10000) -> np.ndarray:
    state = spin_up(forcing, nudge)
    out = []
    for _ in range(steps):
        state = run(state, 1, forcing)
        out.extend(state)
    return np.array(out)


@plot("ch14-climate")
def climates(lang: str):
    fig, ax = new(height=2.7)
    bins = np.linspace(-12, 18, 61)
    for data, color, ls, label in (
        (_samples(FORCING, 0.01), BLUE, "-",
         T(lang, "forcing 8, one start", "wymuszenie 8, jeden start")),
        (_samples(FORCING, 1.0), TEAL, "--",
         T(lang, "forcing 8, another start", "wymuszenie 8, inny start")),
        (_samples(HOT, 0.01), RED, "-",
         T(lang, "forcing 10", "wymuszenie 10")),
    ):
        ax.hist(data, bins=bins, density=True, histtype="step", color=color,
                ls=ls, lw=1.1, label=label)
    ax.axvline(RAIN, color=GREY, lw=0.7, ls=":")
    ax.set_xlabel(T(lang, "the number at a site", "liczba w punkcie"))
    ax.set_ylabel(T(lang, "how often", "jak często"))
    ax.legend(loc="upper left", frameon=False)
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    main()
