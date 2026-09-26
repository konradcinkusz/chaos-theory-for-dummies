"""Chapter 5's plots: four time series, four cobwebs, a window of order
inside the chaos, and a preview of two nearby starts parting company."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch05"))

from _style import AMBER, BLUE, GREY, T, main, new, num, plot

from chaoslab import cobweb, logistic, orbit

RATES = (2.8, 3.2, 3.5, 3.9)


def _r_is(lang: str, r: float) -> str:
    """A panel title. The number stays OUT of maths mode, where a Polish
    decimal comma would be set with a space after it."""
    return "$r$ = " + num(lang, r, "g")


def _series(ax, r: float, x0: float, n: int, color: str, lang: str,
            label: str | None = None) -> None:
    """Dots for the values, a thin grey line to guide the eye."""
    xs = orbit(logistic(r), x0, n)
    ax.plot(range(n + 1), xs, "-", color=color, lw=0.4, alpha=0.6)
    ax.plot(range(n + 1), xs, "o", ms=2.2, color=color, label=label)
    ax.set_ylim(0, 1)


@plot("ch05-four-series")
def four_series(lang: str):
    fig, axes = new(height=3.9, ncols=2, nrows=2, sharex=True, sharey=True)
    for ax, r in zip(axes.flat, RATES, strict=True):
        _series(ax, r, 0.2, 60, BLUE, lang)
        ax.set_title(_r_is(lang, r))
    for ax in axes[1]:
        ax.set_xlabel(T(lang, "step $n$", "krok $n$"))
    for ax in axes[:, 0]:
        ax.set_ylabel("$x_n$")
    fig.tight_layout()
    return fig


@plot("ch05-four-cobwebs")
def four_cobwebs(lang: str):
    fig, axes = new(height=3.3, ncols=2, nrows=2)
    grid = [i / 200 for i in range(201)]
    # r = 2.8 and 3.9 start at 0.2, as in the text. The two cycles start a
    # hair to the right of the crossing, so the picture shows the path being
    # pushed AWAY from the fixed point before it is caught on its loop.
    starts = {2.8: (0.2, 40), 3.2: (1 - 1 / 3.2 + 0.004, 40),
              3.5: (1 - 1 / 3.5 + 0.004, 40), 3.9: (0.2, 45)}
    for ax, r in zip(axes.flat, RATES, strict=True):
        f = logistic(r)
        x0, n = starts[r]
        ax.plot([0, 1], [0, 1], color=GREY, lw=0.6)
        ax.plot(grid, [f(x) for x in grid], color=BLUE, lw=1.1)
        corners = cobweb(f, x0, n)
        ax.plot([p[0] for p in corners], [p[1] for p in corners],
                color=AMBER, lw=0.4)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title(_r_is(lang, r))
        ax.set_xticks([0, 0.5, 1])
        ax.set_yticks([0, 0.5, 1])
    for ax in axes[1]:
        ax.set_xlabel("$x_n$")
    for ax in axes[:, 0]:
        ax.set_ylabel("$x_{n+1}$")
    fig.tight_layout()
    return fig


@plot("ch05-window")
def window(lang: str):
    fig, axes = new(height=2.3, ncols=2, sharey=True)
    for ax, r in zip(axes, (3.83, 3.9), strict=True):
        _series(ax, r, 0.2, 80, BLUE, lang)
        ax.set_title(_r_is(lang, r))
        ax.set_xlabel(T(lang, "step $n$", "krok $n$"))
    axes[0].set_ylabel("$x_n$")
    fig.tight_layout()
    return fig


@plot("ch05-two-starts")
def two_starts(lang: str):
    fig, ax = new(height=2.4)
    _series(ax, 3.9, 0.2, 60, BLUE, lang,
            label=T(lang, "from ", "od ") + num(lang, 0.2, ".1f"))
    _series(ax, 3.9, 0.200001, 60, AMBER, lang,
            label=T(lang, "from ", "od ") + num(lang, 0.200001, ".6f"))
    ax.set_xlabel(T(lang, "step $n$", "krok $n$"))
    ax.set_ylabel("$x_n$")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), frameon=False,
              ncols=2)
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    main()
