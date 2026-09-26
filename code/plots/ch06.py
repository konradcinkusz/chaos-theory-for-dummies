"""Chapter 6's plots: two runs peeling apart, and their gap on a log scale."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch06"))

from _style import AMBER, BLUE, GREY, T, main, new, plot
from twins import NUDGE, START, rule, twin_runs
from worth import TOL

from chaoslab import separation, steps_until_apart

APART = steps_until_apart(rule, START, NUDGE, TOL)


@plot("ch06-peel")
def peel(lang: str):
    fig, ax = new(height=2.6)
    a, b = twin_runs(50)
    steps = range(51)
    ax.plot(steps, a, "-o", ms=2.5, lw=0.8, color=BLUE,
            label=T(lang, "start 0.2", "start 0,2"))
    ax.plot(steps, b, "--s", ms=2.2, lw=0.8, color=AMBER,
            label=T(lang, "start 0.2000000001", "start 0,2000000001"))
    ax.axvline(APART, color=GREY, lw=0.6, ls=":")
    ax.set_xlabel(T(lang, "step", "krok"))
    ax.set_ylabel("x")
    ax.set_ylim(-0.02, 1.25)
    ax.set_xlim(0, 50)
    ax.legend(loc="upper left", ncols=2, frameon=False)
    fig.tight_layout()
    return fig


@plot("ch06-gap-log")
def gap_log(lang: str):
    fig, ax = new(height=2.6)
    gaps = separation(rule, START, NUDGE, 60)
    ax.semilogy(range(61), gaps, "o", ms=2.5, color=BLUE,
                label=T(lang, "measured gap", "zmierzona różnica"))
    top = 36
    ax.semilogy(range(top), [NUDGE * 2**n for n in range(top)], "--",
                color=AMBER, lw=0.9,
                label=T(lang, "doubling every step",
                        "podwajanie w każdym kroku"))
    ax.axhline(1.0, color=GREY, lw=0.6, ls=":")
    ax.text(60, 1.6, T(lang, "the whole range", "cały przedział"),
            ha="right", va="bottom", fontsize=8, color=GREY)
    ax.set_xlabel(T(lang, "step", "krok"))
    ax.set_ylabel(T(lang, "gap between the runs", "różnica między biegami"))
    ax.set_ylim(1e-11, 20)
    ax.set_xlim(0, 60)
    ax.legend(loc="lower right", frameon=False)
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    main()
