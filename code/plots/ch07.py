"""Chapter 7's plots: an average that settles, a horizon that is a straight
line, and the exponent across the logistic map's knob r."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch07"))

from _style import AMBER, BLUE, GREY, RED, T, main, new, num, plot
from exponent import exponent
from horizon import counts, horizon
from stretch import step, stretch

LN2 = math.log(2)


def _running(r: float, x0: float, n: int) -> list[float]:
    """The running average of ln|stretch| along the orbit from x0."""
    x, total, out = x0, 0.0, []
    for k in range(1, n + 1):
        total += math.log(abs(stretch(r, x)))
        out.append(total / k)
        x = step(r, x)
    return out


@plot("ch07-running-average")
def running_average(lang: str):
    fig, ax = new(height=2.5)
    n = 20_000
    ks = np.arange(1, n + 1)
    for x0, ls in ((0.1, "-"), (0.3, "--"), (0.77, ":")):
        ax.semilogx(ks, _running(4.0, x0, n), ls, color=BLUE, lw=0.9)
        ax.semilogx(ks, _running(3.7, x0, n), ls, color=AMBER, lw=0.9)
    ax.axhline(LN2, color=GREY, lw=0.6)
    ax.text(150, LN2 + 0.12, T(lang, r"$r = 4$: settles on $\ln 2$",
                                r"$r = 4$: ustala się na $\ln 2$"),
            color=BLUE)
    ax.text(150, 0.12, T(lang, r"$r = 3.7$: a smaller rate",
                         r"$r = 3{,}7$: mniejsze tempo"), color=AMBER)
    ax.set_ylim(-0.6, 1.3)
    ax.set_xlabel(T(lang, "steps averaged (three starts each)",
                    "liczba uśrednionych kroków (po trzy starty)"))
    ax.set_ylabel(T(lang, r"average of $\ln|$stretch$|$",
                    r"średnia z $\ln|$rozciągnięcia$|$"))
    fig.tight_layout()
    return fig


@plot("ch07-horizon-line")
def horizon_line(lang: str):
    fig, ax = new(height=2.6)
    tol = 0.1
    ks = list(range(2, 14))
    deltas = [10.0 ** -k for k in ks]
    means, lo, hi = [], [], []
    for d in deltas:
        c = sorted(counts(4.0, d, tol))
        means.append(sum(c) / len(c))
        lo.append(c[len(c) // 10])
        hi.append(c[len(c) * 9 // 10])
    ax.fill_between(deltas, lo, hi, color=BLUE, alpha=0.12, lw=0,
                    label=T(lang, "middle 80% of a thousand starts",
                            "środkowe 80% z tysiąca startów"))
    ax.semilogx(deltas, means, "o", ms=3, color=BLUE,
                label=T(lang, "counted: the mean", "policzone: średnia"))
    fine = np.logspace(-1.7, -13.3, 50)
    ax.semilogx(fine, [horizon(LN2, d, tol) for d in fine], color=RED,
                lw=0.9, label=T(lang, r"formula $\ln(T/\delta)/\ln 2$",
                                r"wzór $\ln(T/\delta)/\ln 2$"))
    ax.invert_xaxis()
    ax.set_xlabel(T(lang, r"error in the start, $\delta$ "
                          r"(better measurements to the right)",
                    r"błąd startu $\delta$ (lepsze pomiary po prawej)"))
    ax.set_ylabel(T(lang, "steps until the gap\nexceeds "
                    + num(lang, tol, ".1f"),
                    "kroki, aż różnica\nprzekroczy "
                    + num(lang, tol, ".1f")))
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    return fig


@plot("ch07-exponent-r")
def exponent_r(lang: str):
    fig, ax = new(height=2.7)
    rs = np.linspace(2.5, 4.0, 1501)
    x = np.full_like(rs, 0.3)
    for _ in range(1000):
        x = rs * x * (1.0 - x)
    total = np.zeros_like(rs)
    n = 4000
    for _ in range(n):
        total += np.log(np.maximum(np.abs(rs * (1.0 - 2.0 * x)), 1e-12))
        x = rs * x * (1.0 - x)
    lam = total / n
    ax.plot(rs, lam, color=BLUE, lw=0.6)
    ax.axhline(0.0, color=GREY, lw=0.6)
    marks = (2.8, 3.2, 3.5, 4.0)
    ax.plot(marks, [exponent(r) for r in marks], "o", ms=3.5, color=RED)
    ax.set_ylim(-1.6, 1.0)
    ax.set_xlim(2.5, 4.02)
    ax.text(2.55, 0.25, T(lang, "above zero: errors grow",
                          "powyżej zera: błędy rosną"), color=GREY)
    ax.text(2.55, -1.4, T(lang, "below zero: errors shrink",
                          "poniżej zera: błędy maleją"), color=GREY)
    ax.set_xlabel(T(lang, r"the knob $r$", r"pokrętło $r$"))
    ax.set_ylabel(T(lang, r"Lyapunov exponent $\lambda$",
                    r"wykładnik Lapunowa $\lambda$"))
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    main()
