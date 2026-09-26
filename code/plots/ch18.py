"""Chapter 18's plots: the log law made visible, and a forecast that turns
into odds and then into the climate."""

from __future__ import annotations

import math
import sys
from pathlib import Path
from statistics import median

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch18"))

from _exponents import henon_exponent, logistic_exponent
from _style import AMBER, BLUE, GREY, T, main, new, plot
from beyond import long_run, odds
from horizon import forecast_length
from thousandfold import typical_horizon

DIGITS = list(range(2, 13))


def _henon(p: tuple[float, float]) -> tuple[float, float]:
    x, y = p
    return (1.0 - 1.4 * x * x + y, 0.3 * x)


def _henon_starts(n: int = 201) -> list[tuple[float, float]]:
    """Points on the Henon attractor, a few steps apart."""
    p = (0.1, 0.1)
    for _ in range(1000):
        p = _henon(p)
    starts = []
    for k in range(7 * n):
        p = _henon(p)
        if k % 7 == 0:
            starts.append(p)
    return starts


def _henon_apart(p: tuple[float, float], error: float,
                 tolerance: float = 0.1) -> int:
    q = (p[0] + error, p[1])
    for n in range(1, 10_000):
        p, q = _henon(p), _henon(q)
        if math.hypot(p[0] - q[0], p[1] - q[1]) > tolerance:
            return n
    raise RuntimeError("never separated")


@plot("ch18-digits")
def digits(lang: str):
    fig, ax = new(height=2.9)
    lam_l, lam_h = logistic_exponent(), henon_exponent()
    starts = _henon_starts()
    measured_l = [typical_horizon(1 / 10**d) for d in DIGITS]
    measured_h = [median(_henon_apart(s, 1 / 10**d) for s in starts)
                  for d in DIGITS]
    ax.plot(DIGITS, [forecast_length(lam_h, d) for d in DIGITS],
            color=AMBER,
            label=T(lang, "Hénon map: formula", "odwzorowanie Hénona: wzór"))
    ax.plot(DIGITS, measured_h, "s", ms=3.5, color=AMBER,
            label=T(lang, "Hénon map: measured",
                    "odwzorowanie Hénona: pomiar"))
    ax.plot(DIGITS, [forecast_length(lam_l, d) for d in DIGITS],
            color=BLUE,
            label=T(lang, "logistic map: formula",
                    "odwzorowanie logistyczne: wzór"))
    ax.plot(DIGITS, measured_l, "o", ms=3.5, color=BLUE,
            label=T(lang, "logistic map: measured",
                    "odwzorowanie logistyczne: pomiar"))
    ax.set_xticks(DIGITS)
    ax.set_xlabel(T(lang, "correct decimal places in the start",
                    "poprawne miejsca po przecinku w stanie początkowym"))
    ax.set_ylabel(T(lang, "steps before the error\nexceeds 0.1",
                    "kroki, zanim błąd\nprzekroczy 0,1"))
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    return fig


@plot("ch18-odds")
def odds_plot(lang: str):
    fig, ax = new(height=2.6)
    steps = list(range(46))
    ax.axhline(long_run(0.3), color=GREY, lw=0.8, ls="--")
    ax.text(45, long_run(0.3) - 0.06,
            T(lang, "one long run: a third",
              "długi przebieg: jedna trzecia"),
            ha="right", va="top", color=GREY, fontsize=8)
    ax.plot(steps, odds(0.3, 1e-6, 45), "-o", ms=2.5, color=BLUE,
            label=T(lang, "start right to 6 digits",
                    "stan początkowy z dokładnością do 6 cyfr"))
    ax.plot(steps, odds(0.3, 1e-9, 45), "-s", ms=2.5, color=AMBER,
            label=T(lang, "start right to 9 digits",
                    "stan początkowy z dokładnością do 9 cyfr"))
    ax.set_xlabel(T(lang, "step", "krok"))
    ax.set_ylabel(T(lang, "chance that x < 0.25",
                    "szansa, że x < 0,25"))
    ax.set_ylim(-0.05, 1.32)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
    ax.legend(frameon=False, loc="upper right", ncols=2)
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    main()
