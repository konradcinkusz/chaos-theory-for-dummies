"""Chapter 9's plots: the butterfly from two sides, two runs parting
company, and two histograms that do not care where the run began."""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch09"))

import numpy as np
from _style import AMBER, BLUE, GREY, TEAL, T, main, new, num, plot
from averages import STARTS
from two_runs import DT, a, b, distance

from chaoslab import integrate, lorenz, rk4_step

FIELD = lorenz()
STILL = math.sqrt(8.0 / 3.0 * 27.0)


@plot("ch09-butterfly")
def butterfly(lang: str):
    fig, (left, right) = new(height=2.7, ncols=2,
                             gridspec_kw={"width_ratios": [1, 1.25]})
    run = np.array(integrate(FIELD, (1.0, 1.0, 1.0), DT, 6000))
    left.plot(run[500:, 0], run[500:, 2], color=BLUE, lw=0.35)
    left.plot([STILL, -STILL], [27, 27], "x", color=AMBER, ms=5, mew=1.2)
    left.set_xlabel(T(lang, "x (the roll)", "x (wir)"))
    left.set_ylabel(T(lang, "z (the layer)", "z (warstwa)"))
    left.set_title(T(lang, "Seen from the side: x against z",
                     "Z boku: x względem z"))
    t = np.arange(4001) * DT
    right.plot(t, run[:4001, 0], color=BLUE, lw=0.6)
    right.axhline(0, color=GREY, lw=0.5)
    for s in (STILL, -STILL):
        right.axhline(s, color=AMBER, lw=0.6, ls="--")
    right.set_xlabel(T(lang, "time", "czas"))
    right.set_ylabel("x")
    right.set_title(T(lang, "Over time: which wing, when",
                      "W czasie: które skrzydło i kiedy"))
    fig.tight_layout()
    return fig


def _pair(steps: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    p, q = a, b
    xa, xb, gap = [p[0]], [q[0]], [distance(p, q)]
    for _ in range(steps):
        p, q = rk4_step(FIELD, p, DT), rk4_step(FIELD, q, DT)
        xa.append(p[0])
        xb.append(q[0])
        gap.append(distance(p, q))
    return np.array(xa), np.array(xb), np.array(gap)


@plot("ch09-apart")
def apart(lang: str):
    fig, (left, right) = new(height=2.6, ncols=2)
    xa, xb, gap = _pair(3000)
    t = np.arange(len(gap)) * DT
    left.plot(t, xa, color=BLUE, lw=0.8, label=T(lang, "run A", "przebieg A"))
    left.plot(t, xb, color=AMBER, lw=0.8, ls="--",
              label=T(lang, "run B", "przebieg B"))
    left.set_xlabel(T(lang, "time since the split", "czas od rozdzielenia"))
    left.set_ylabel("x")
    left.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2,
                frameon=False)
    right.semilogy(t, gap, color=BLUE, lw=0.8)
    guide = 1e-8 * np.exp(0.9 * t[t < 24])
    right.semilogy(t[t < 24], guide, color=GREY, lw=0.8, ls="--",
                   label=T(lang, "exponent " + num(lang, 0.9, ".1f")
                           + " per time unit",
                           "wykładnik " + num(lang, 0.9, ".1f")
                           + " na jednostkę czasu"))
    right.axhline(1.0, color=TEAL, lw=0.6)
    right.set_xlabel(T(lang, "time since the split", "czas od rozdzielenia"))
    right.set_ylabel(T(lang, "distance between the runs",
                       "odległość między przebiegami"))
    right.legend(loc="lower right", frameon=False)
    fig.tight_layout()
    return fig


@plot("ch09-histograms")
def histograms(lang: str):
    fig, (left, right) = new(height=2.5, ncols=2)
    colours = [BLUE, AMBER, TEAL]
    for start, colour in zip(STARTS[:3], colours, strict=True):
        run = np.array(integrate(FIELD, start, DT, 51_000)[1000:])
        label = "(" + ", ".join(f"{v:.0f}" for v in start) + ")"
        left.hist(run[:, 0], bins=60, range=(-20, 20), density=True,
                  histtype="step", color=colour, lw=0.9)
        right.hist(run[:, 2], bins=60, range=(0, 50), density=True,
                   histtype="step", color=colour, lw=0.9, label=label)
    left.set_xlabel(T(lang, "x: which wing, how far out",
                      "x: które skrzydło, jak daleko"))
    left.set_ylabel(T(lang, "share of the time", "udział czasu"))
    right.legend(loc="upper right", frameon=False, fontsize=7,
                 title=T(lang, "start", "start"), title_fontsize=7)
    right.set_xlabel(T(lang, "z: how high", "z: jak wysoko"))
    for ax in (left, right):
        ax.set_yticks([])
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    main()
