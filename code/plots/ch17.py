"""Chapter 17's plots: control switched on mid-run, and a driven copy of
the Lorenz system falling into step with the original."""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch17"))

from _style import AMBER, BLUE, GREY, RED, T, main, new, plot
from control import LEVER, R0, STRETCH, TARGET, nudge, step
from sync import DT, ORIGINAL, drive_and_copy, gap, start

from chaoslab import rk4_step

ON = 100


@plot("ch17-control")
def control(lang: str):
    fig, (top, bottom) = new(height=3.6, nrows=2, sharex=True,
                             gridspec_kw={"height_ratios": [2.2, 1]})
    largest = 0.01 * R0
    reach = largest * LEVER / abs(STRETCH)
    x, xs, pct = 0.2, [], []
    for n in range(301):
        change = nudge(x, largest) if n >= ON else 0.0
        xs.append(x)
        pct.append(100 * change / R0)
        x = step(x, change)
    steps = range(len(xs))
    top.axhspan(TARGET - reach, TARGET + reach, color=AMBER, alpha=0.25,
                lw=0)
    top.axhline(TARGET, color=AMBER, lw=0.7, ls="--")
    top.plot(steps, xs, "-", color=GREY, lw=0.4)
    top.plot(steps, xs, "o", ms=1.6, color=BLUE)
    for ax in (top, bottom):
        ax.axvline(ON, color=RED, lw=0.7)
    top.text(ON + 4, 0.08, T(lang, "controller on", "sterowanie włączone"),
             color=RED, fontsize=8)
    top.set_ylabel("x")
    top.set_ylim(0, 1)
    bottom.plot(steps, pct, "-", color=RED, lw=0.8)
    bottom.set_ylim(-1.1, 1.1)
    bottom.set_xlabel(T(lang, "step", "krok"))
    bottom.set_ylabel(T(lang, "change to r (%)", "zmiana r (%)"))
    fig.tight_layout()
    return fig


@plot("ch17-sync")
def sync(lang: str):
    fig, ax = new(height=2.6)
    s = start()
    alone = (s[0], s[3], s[4])
    e0 = gap(s[1:3], s[3:5])
    ts, driven, free = [], [], []
    for n in range(3001):
        e = gap(s[1:3], s[3:5])
        ts.append(n * DT)
        driven.append(e if e > 0.0 else math.nan)
        free.append(gap(s[0:3], alone))
        s = rk4_step(drive_and_copy, s, DT)
        alone = rk4_step(ORIGINAL, alone, DT)
    ax.semilogy(ts, free, color=GREY, lw=0.8,
                label=T(lang, "copy left alone", "kopia zostawiona sama"))
    ax.semilogy(ts, driven, color=BLUE, lw=1.1,
                label=T(lang, "copy driven by $x$", "kopia napędzana przez $x$"))
    ax.semilogy(ts, [e0 * math.exp(-t) for t in ts], color=AMBER, lw=0.8,
                ls="--", label=T(lang, "guaranteed: $e$ times smaller per unit",
                                 "gwarancja: $e$ razy mniej na jednostkę"))
    last = max(t for t, e in zip(ts, driven, strict=True) if e == e)
    ax.axvline(last, color=BLUE, lw=0.5, ls=":")
    ax.text(last + 0.5, 1e-6, T(lang, "identical in every\ndigit from here",
                                "identyczne w każdej\ncyfrze od tego miejsca"),
            color=BLUE, fontsize=7.5)
    ax.set_ylim(1e-17, 1e3)
    ax.set_xlabel(T(lang, "time", "czas"))
    ax.set_ylabel(T(lang, "gap from the original", "odległość od oryginału"))
    ax.legend(loc="lower left", frameon=False)
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    main()
