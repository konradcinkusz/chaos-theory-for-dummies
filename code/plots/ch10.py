"""Chapter 10's plots: a square stretched and folded, the attractor on its
basin, and two zooms into the attractor.

Plots are not gated for drift, so numpy is used freely here: many orbits are
run side by side, which is what makes the deep zoom possible in seconds.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from matplotlib.patches import Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch10"))

from _style import AMBER, BLUE, GREY, RED, TEAL, T, main, new, plot
from henon import A, B

LIGHT = "#E8ECF1"


def _step(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return 1.0 - A * x * x + y, B * x


def _attractor(points: int = 60_000) -> tuple[np.ndarray, np.ndarray]:
    """One long run, settled, as two arrays."""
    x, y = 0.0, 0.0
    for _ in range(1000):
        x, y = 1.0 - A * x * x + y, B * x
    xs, ys = np.empty(points), np.empty(points)
    for i in range(points):
        x, y = 1.0 - A * x * x + y, B * x
        xs[i], ys[i] = x, y
    return xs, ys


def _window(box: tuple[float, float, float, float], orbits: int,
            steps: int) -> tuple[np.ndarray, np.ndarray]:
    """Points of many settled orbits inside box = (x0, x1, y0, y1)."""
    rng = np.random.default_rng(10)
    x = rng.uniform(-0.1, 0.1, orbits)
    y = rng.uniform(-0.1, 0.1, orbits)
    for _ in range(200):
        x, y = _step(x, y)
    keep_x, keep_y = [], []
    x0, x1, y0, y1 = box
    for _ in range(steps):
        x, y = _step(x, y)
        inside = (x > x0) & (x < x1) & (y > y0) & (y < y1)
        if inside.any():
            keep_x.append(x[inside])
            keep_y.append(y[inside])
    return np.concatenate(keep_x), np.concatenate(keep_y)


@plot("ch10-square-folds")
def square_folds(lang: str):
    fig, axes = new(height=4.4, ncols=3, nrows=2, sharex=True, sharey=True)
    g = np.linspace(-0.6, 0.6, 260)
    x, y = np.meshgrid(g, g)
    x, y = x.ravel(), y.ravel()
    colour = x.copy()                 # colour each point by where it began
    cmap = LinearSegmentedColormap.from_list("ba", [BLUE, TEAL, AMBER])
    for step, ax in enumerate(axes.ravel()):
        alive = np.abs(x) + np.abs(y) < 10
        ax.scatter(x[alive], y[alive], c=colour[alive], cmap=cmap,
                   s=0.15, lw=0, vmin=-0.6, vmax=0.6, rasterized=True)
        ax.set_title(T(lang, f"after {step} steps" if step != 1 else
                       "after 1 step",
                       f"po {step} krokach" if step != 1 else
                       "po 1 kroku"))
        ax.set_xlim(-1.6, 1.6)
        ax.set_ylim(-0.7, 0.7)
        with np.errstate(over="ignore", invalid="ignore"):
            x, y = _step(x, y)
    for ax in axes[1]:
        ax.set_xlabel("$x$")
    for ax in axes[:, 0]:
        ax.set_ylabel("$y$")
    fig.tight_layout()
    return fig


@plot("ch10-attractor")
def attractor(lang: str):
    fig, ax = new(height=3.2)
    # The basin: which starts on a grid stay, and which leave for good.
    gx = np.linspace(-2.5, 2.5, 700)
    gy = np.linspace(-2.0, 2.0, 560)
    x, y = np.meshgrid(gx, gy)
    x0, y0 = x.copy(), y.copy()
    gone = np.zeros_like(x, dtype=bool)
    with np.errstate(over="ignore", invalid="ignore"):
        for _ in range(60):
            x, y = _step(x, y)
            gone |= ~(np.abs(x) + np.abs(y) < 10)
            x[gone], y[gone] = 0.0, 0.0
    ax.imshow(gone, origin="lower", extent=(-2.5, 2.5, -2.0, 2.0),
              cmap=ListedColormap(["white", LIGHT]), aspect="auto",
              interpolation="nearest", rasterized=True)
    ax_x, ax_y = _attractor()
    ax.plot(ax_x, ax_y, ",", color=BLUE)
    del x0, y0
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.0, 2.0)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.text(1.55, 1.55, T(lang, "leaves for good", "ucieka na zawsze"),
            color=GREY, ha="center", fontsize=8)
    ax.text(0.0, -0.7, T(lang, "lands on the attractor",
                         "ląduje na atraktorze"),
            color=BLUE, ha="center", fontsize=8)
    fig.tight_layout()
    return fig


ZOOM1 = (0.55, 0.72, 0.14, 0.22)
ZOOM2 = (0.615, 0.645, 0.183, 0.195)


@plot("ch10-zooms")
def zooms(lang: str):
    fig, axes = new(height=2.5, ncols=3)
    full_x, full_y = _attractor()
    z1x, z1y = _window(ZOOM1, 4000, 600)
    z2x, z2y = _window(ZOOM2, 20_000, 1500)
    panels = [(full_x, full_y, (-1.5, 1.5, -0.45, 0.45), ZOOM1),
              (z1x, z1y, ZOOM1, ZOOM2),
              (z2x, z2y, ZOOM2, None)]
    titles = [T(lang, "the whole attractor", "cały atraktor"),
              T(lang, "the box, enlarged", "powiększona ramka"),
              T(lang, "its box, enlarged", "jej ramka, powiększona")]
    for ax, (px, py, lim, box), title in zip(axes, panels, titles,
                                             strict=True):
        ax.plot(px, py, ",", color=BLUE)
        ax.set_xlim(lim[0], lim[1])
        ax.set_ylim(lim[2], lim[3])
        ax.set_title(title)
        ax.set_xlabel("$x$")
        ax.locator_params(nbins=3)
        if box is not None:
            ax.add_patch(Rectangle((box[0], box[2]), box[1] - box[0],
                                   box[3] - box[2], fill=False,
                                   edgecolor=RED, lw=1.2))
    axes[0].set_ylabel("$y$")
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    main()
