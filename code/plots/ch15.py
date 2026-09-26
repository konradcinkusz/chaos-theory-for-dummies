"""Chapter 15's plots: two series with one histogram, two return maps, a
forecast that fails in steps, and a curve thickening in noise."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch15"))

from _style import AMBER, BLUE, GREY, T, main, new, num, plot
from analogues import mean_error
from noisy import with_noise
from return_map import return_pairs
from twins import rule_series, shuffled

RULE = rule_series()
SHUF = shuffled(RULE)


def _grid(ax) -> None:
    """Faint lines every 0.1: the hundred little squares of the test."""
    for k in range(1, 10):
        ax.axhline(k / 10, color=GREY, lw=0.25, alpha=0.5)
        ax.axvline(k / 10, color=GREY, lw=0.25, alpha=0.5)
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.set_aspect("equal")


@plot("ch15-twins")
def twins(lang: str):
    fig, axes = new(height=3.9, ncols=2, nrows=2)
    titles = (T(lang, "made by the rule", "wytworzona przez regułę"),
              T(lang, "the same numbers, shuffled",
                "te same liczby, przetasowane"))
    for col, (xs, colour, title) in enumerate(
            zip((RULE, SHUF), (BLUE, AMBER), titles, strict=True)):
        top, bottom = axes[0][col], axes[1][col]
        top.plot(range(100), xs[:100], "-o", ms=1.8, lw=0.5, color=colour)
        top.set_title(title)
        top.set_xlabel(T(lang, "step n", "krok n"))
        top.set_ylim(-0.03, 1.03)
        bottom.hist(xs, bins=20, range=(0.0, 1.0), color=colour,
                    edgecolor="white", linewidth=0.4)
        bottom.set_xlabel(T(lang, "value", "wartość"))
    axes[0][0].set_ylabel(T(lang, "value", "wartość"))
    axes[1][0].set_ylabel(T(lang, "how many", "ile razy"))
    fig.tight_layout()
    return fig


@plot("ch15-return-maps")
def return_maps(lang: str):
    fig, (left, right) = new(height=3.0, ncols=2)
    for ax, xs, colour, title in (
            (left, RULE, BLUE, T(lang, "made by the rule",
                                 "wytworzona przez regułę")),
            (right, SHUF, AMBER, T(lang, "shuffled", "przetasowana"))):
        pairs = return_pairs(xs)
        _grid(ax)
        ax.plot([a for a, _ in pairs], [b for _, b in pairs], "o",
                ms=1.2, color=colour, alpha=0.7)
        ax.set_title(title)
        ax.set_xlabel(T(lang, "this value", "ta wartość"))
    left.set_ylabel(T(lang, "the next value", "następna wartość"))
    fig.tight_layout()
    return fig


@plot("ch15-forecast")
def forecast(lang: str):
    fig, ax = new(height=2.5)
    steps = range(1, 13)
    ax.semilogy(steps, [mean_error(RULE, h) for h in steps], "-o", ms=3,
                color=BLUE, label=T(lang, "made by the rule",
                                    "wytworzona przez regułę"))
    ax.semilogy(steps, [mean_error(SHUF, h) for h in steps], "-s", ms=3,
                color=AMBER, label=T(lang, "shuffled", "przetasowana"))
    ax.set_xlabel(T(lang, "steps ahead", "kroki naprzód"))
    ax.set_ylabel(T(lang, "average miss", "średni błąd"))
    ax.set_xticks(list(steps))
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    return fig


@plot("ch15-noisy")
def noisy(lang: str):
    fig, axes = new(height=2.35, ncols=3)
    for ax, size in zip(axes, (0.01, 0.05, 0.2), strict=True):
        pairs = return_pairs(with_noise(RULE, size))
        _grid(ax)
        ax.set_xlim(-0.22, 1.22)
        ax.set_ylim(-0.22, 1.22)
        ax.plot([a for a, _ in pairs], [b for _, b in pairs], "o",
                ms=0.9, color=BLUE, alpha=0.6)
        ax.set_title(T(lang, "noise up to ", "szum do ")
                     + num(lang, size, ".2g"))
        ax.set_xlabel(T(lang, "this value", "ta wartość"))
    axes[0].set_ylabel(T(lang, "the next value", "następna wartość"))
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    main()
