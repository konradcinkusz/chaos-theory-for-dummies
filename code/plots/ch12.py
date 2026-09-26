"""Chapter 12's plots: the Mandelbrot set and a zoom into its edge, two
Julia sets, and the real axis laid over Chapter 8's bifurcation diagram.

Pictures need hundreds of thousands of points, so the escape time here is
the chapter's rule run on whole numpy arrays at once. It is the same rule as
chaoslab.escape_time -- square, add c, stop when the length passes 2 -- with
the real and imaginary parts written out; the plots are not gated, and only
the page's numbers come from code/measure/ch12.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch12"))

from _style import BLUE, GREY, RED, T, main, new, num, plot
from chaoslab import r_to_c

# White far outside, the book's blue near the edge; the set itself is ink.
SHADE = LinearSegmentedColormap.from_list(
    "escape", ["#FFFFFF", "#C9D8E8", "#6A93BF", BLUE, "#0B1D30"])
INK = "#111111"


def escape_grid(zx: np.ndarray, zy: np.ndarray, cx: np.ndarray,
                cy: np.ndarray, limit: int) -> np.ndarray:
    """The escape step of every point of a grid; `limit` means never."""
    shape = np.shape(zx)
    zx, zy = zx.astype(float).ravel(), zy.astype(float).ravel()
    cx = np.broadcast_to(cx, shape).astype(float).ravel()
    cy = np.broadcast_to(cy, shape).astype(float).ravel()
    steps = np.full(zx.shape, limit)
    alive = np.arange(zx.size)
    x, y, ax, ay = zx.copy(), zy.copy(), cx.copy(), cy.copy()
    for n in range(limit):
        out = x * x + y * y > 4.0
        steps[alive[out]] = n
        keep = ~out
        alive, x, y, ax, ay = alive[keep], x[keep], y[keep], ax[keep], ay[keep]
        x, y = x * x - y * y + ax, 2.0 * x * y + ay
    return steps.reshape(shape)


def picture(ax, x0: float, x1: float, y0: float, y1: float, steps,
            limit: int) -> None:
    """Draw escape steps as an image: ink for the set, shades outside."""
    outside = np.ma.masked_where(steps >= limit, np.log1p(steps))
    ax.set_facecolor(INK)
    ax.imshow(outside, origin="lower", extent=(x0, x1, y0, y1),
              cmap=SHADE, interpolation="nearest",
              vmin=0.0, vmax=np.log1p(limit))
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)


def mandelbrot(x0: float, x1: float, y0: float, y1: float, nx: int,
               limit: int) -> np.ndarray:
    ny = int(round(nx * (y1 - y0) / (x1 - x0)))
    cx, cy = np.meshgrid(np.linspace(x0, x1, nx), np.linspace(y0, y1, ny))
    zero = np.zeros_like(cx)
    return escape_grid(zero, zero, cx, cy, limit)


@plot("ch12-mandelbrot")
def the_set(lang: str):
    fig, (left, right) = new(height=2.9, ncols=2)
    box = (-0.775, -0.715, 0.075, 0.135)   # the zoom, drawn on the left
    whole = (-2.2, 0.6, -1.25, 1.25)
    picture(left, *whole, mandelbrot(*whole, 700, 200), 200)
    left.add_patch(Rectangle((box[0], box[2]), box[1] - box[0],
                             box[3] - box[2], fill=False, ec=RED, lw=0.9))
    left.set_aspect("equal")
    left.set_xlabel(T(lang, "real part of c", "część rzeczywista c"))
    left.set_ylabel(T(lang, "imaginary part of c", "część urojona c"))
    left.set_title(T(lang, "The whole set", "Cały zbiór"))
    picture(right, *box, mandelbrot(*box, 700, 600), 600)
    right.set_aspect("equal")
    right.set_xlabel(T(lang, "real part of c", "część rzeczywista c"))
    right.set_title(T(lang, "The red square, magnified 45 times",
                      "Czerwony kwadrat, powiększony 45 razy"))
    fig.tight_layout()
    return fig


def julia(c: complex, nx: int = 700, limit: int = 300) -> np.ndarray:
    x0, x1, y0, y1 = -1.8, 1.8, -1.1, 1.1
    ny = int(round(nx * (y1 - y0) / (x1 - x0)))
    zx, zy = np.meshgrid(np.linspace(x0, x1, nx), np.linspace(y0, y1, ny))
    return escape_grid(zx, zy, np.array(c.real), np.array(c.imag), limit)


@plot("ch12-julia")
def two_julias(lang: str):
    fig, (left, right) = new(height=2.2, ncols=2)
    for ax, c, en, pl in (
        (left, complex(-1.0, 0.0), "one piece", "jeden kawałek"),
        (right, complex(-0.8, 0.2), "dust", "pył"),
    ):
        picture(ax, -1.8, 1.8, -1.1, 1.1, julia(c), 300)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        if c.imag == 0:
            name = f"c = {num(lang, c.real, '.0f')}"
        else:
            name = (f"c = {num(lang, c.real, '.1f')}"
                    f" + {num(lang, c.imag, '.1f')}i")
        ax.set_title(f"{name}: {T(lang, en, pl)}")
    fig.tight_layout()
    return fig


@plot("ch12-real-axis")
def real_axis(lang: str):
    fig, (top, bottom) = new(height=4.1, nrows=2, sharex=True,
                             gridspec_kw={"height_ratios": [1.0, 1.25]})
    strip = (-2.05, 0.35, -0.5, 0.5)
    picture(top, *strip, mandelbrot(*strip, 900, 200), 200)
    top.set_ylabel(T(lang, "imag. part of c", "część urojona c"))
    top.set_title(T(lang, "The Mandelbrot set near the real axis",
                    "Zbiór Mandelbrota przy osi rzeczywistej"))
    # Chapter 8's diagram, drawn against c instead of r.
    cs, xs = [], []
    for r in np.linspace(1.0, 4.0, 1500):
        x = 0.3
        for _ in range(600):
            x = r * x * (1.0 - x)
        c = r_to_c(float(r))
        for _ in range(120):
            x = r * x * (1.0 - x)
            cs.append(c)
            xs.append(x)
    bottom.plot(cs, xs, ",", color=BLUE, alpha=0.5, rasterized=True)
    bottom.set_ylim(0.0, 1.0)
    bottom.set_xlim(strip[0], strip[1])
    bottom.set_xlabel(T(lang, "c", "c"))
    bottom.set_ylabel(T(lang, "where x settles", "gdzie osiada x"))
    marks = ((3.0, ".0f"), (1 + 6 ** 0.5, ".2f"),
             (3.5699456718695445, ".3f"), (1 + 8 ** 0.5, ".2f"))
    for r, fmt in marks:
        c = r_to_c(r)
        for ax in (top, bottom):
            ax.axvline(c, color=RED, lw=0.6, ls="--")
        bottom.text(c + 0.015, 0.97, f"r = {num(lang, r, fmt)}", color=RED,
                    fontsize=7, rotation=90, va="top", ha="left")
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    main()
