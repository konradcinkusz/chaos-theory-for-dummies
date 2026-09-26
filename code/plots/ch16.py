"""Chapter 16's plots: a map that dies, two precisions parting, and the
statistics that survive when the path does not."""

from __future__ import annotations

import math
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch16"))

import numpy as np
from _machine import rule_single, to_single
from _style import AMBER, BLUE, GREY, RED, TEAL, T, main, new, plot
from doubling import exact_doubling
from shadow import computed
from two_formulas import rule_a, rule_b, truth

from chaoslab import doubling


@plot("ch16-collapse")
def collapse(lang: str):
    fig, ax = new(height=2.4)
    steps = 70
    x, t = 0.1, Fraction(1, 10)
    xs, ts = [x], [float(t)]
    for _ in range(steps):
        x, t = doubling(x), exact_doubling(t)
        xs.append(x)
        ts.append(float(t))
    n = range(steps + 1)
    ax.plot(n, ts, "o", ms=3.2, mfc="white", mec=GREY,
            label=T(lang, "the truth: one tenth", "prawda: jedna dziesiąta"))
    ax.plot(n, xs, "o", ms=1.8, color=BLUE,
            label=T(lang, "the computer: 0.1", "komputer: 0,1"))
    ax.set_xlabel(T(lang, "step", "krok"))
    ax.set_ylabel("x")
    ax.set_ylim(-0.05, 1.3)
    ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.legend(loc="upper center", frameon=False, ncol=2)
    fig.tight_layout()
    return fig


def _errors(xs: list[float], true: list[Decimal]) -> list[float]:
    return [float(abs(Decimal(x) - t)) for x, t in zip(xs, true, strict=True)]


@plot("ch16-parting")
def parting(lang: str):
    fig, ax = new(height=2.8)
    steps = 80
    true = truth(steps)
    a = computed(rule_a, steps)
    b = computed(rule_b, steps)
    s = [to_single(0.1)]
    for _ in range(steps):
        s.append(rule_single(s[-1]))
    n = list(range(steps + 1))
    ax.semilogy(n, _errors(s, true), "o", ms=2.2, color=AMBER,
                label=T(lang, "single precision", "pojedyncza precyzja"))
    ax.semilogy(n, _errors(a, true), "o", ms=2.2, color=BLUE,
                label=T(lang, "double, 4x(1−x)", "podwójna, 4x(1−x)"))
    ax.semilogy(n, _errors(b, true), "s", ms=1.8, color=TEAL,
                label=T(lang, "double, 4x−4xx", "podwójna, 4x−4xx"))
    guide = [1e-17 * 2.0**k for k in n]
    ax.semilogy(n, guide, ":", color=GREY, lw=0.8,
                label=T(lang, "doubling every step", "podwojenie co krok"))
    ax.axhline(0.1, color=RED, lw=0.6, ls="--")
    ax.set_ylim(1e-18, 3)
    ax.set_xlabel(T(lang, "step", "krok"))
    ax.set_ylabel(T(lang, "distance from the true orbit",
                    "odległość od prawdziwej orbity"))
    ax.legend(loc="lower right", frameon=False, fontsize=7.5)
    fig.tight_layout()
    return fig


def _running_below(xs: list[float], marks: list[int]) -> list[float]:
    """The fraction of xs[:m] below 0.1, at each m in marks."""
    out, below, k = [], 0, 0
    for m in marks:
        while k < m:
            below += xs[k] < 0.1
            k += 1
        out.append(below / m)
    return out


@plot("ch16-statistics")
def statistics(lang: str):
    fig, (left, right) = new(height=2.5, ncols=2)
    steps = 1_000_000
    a = computed(rule_a, steps)[1:]
    b = computed(rule_b, steps)[1:]
    x, s = to_single(0.1), []
    for _ in range(steps):
        x = rule_single(x)
        s.append(x)
    edges = np.linspace(0.0, 1.0, 41)
    mid = np.linspace(0.004, 0.996, 400)
    left.plot(mid, 1.0 / (math.pi * np.sqrt(mid * (1.0 - mid))),
              color=GREY, lw=1.0, label=T(lang, "exact", "dokładnie"))
    left.hist(a, bins=edges, density=True, histtype="step", color=BLUE,
              label="4x(1−x)")
    left.hist(b, bins=edges, density=True, histtype="step", color=TEAL,
              ls="--", label="4x−4xx")
    left.set_ylim(0, 4.5)
    left.set_xlabel("x")
    left.set_ylabel(T(lang, "share of time (density)",
                      "udział czasu (gęstość)"))
    left.legend(loc="upper center", frameon=False, fontsize=7)
    marks = sorted({int(10 ** (k / 8)) for k in range(8, 49)})
    exact = 2 / math.pi * math.asin(math.sqrt(0.1))
    right.axhline(exact, color=GREY, lw=1.0,
                  label=T(lang, "exact", "dokładnie"))
    right.semilogx(marks, _running_below(a, marks), color=BLUE,
                   label="4x(1−x)")
    right.semilogx(marks, _running_below(b, marks), color=TEAL, ls="--",
                   label="4x−4xx")
    right.semilogx(marks, _running_below(s, marks), color=AMBER,
                   label=T(lang, "single", "pojedyncza"))
    right.set_ylim(0.12, 0.27)
    right.set_xlabel(T(lang, "steps run", "wykonane kroki"))
    right.set_ylabel(T(lang, "fraction of steps below 0.1",
                       "odsetek kroków poniżej 0,1"))
    right.legend(loc="lower right", frameon=False, fontsize=7, ncol=2)
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    main()
