"""Chapter 12's plots: the Mandelbrot set and two zooms into it, two Julia
sets, and the real axis laid over Chapter 8's bifurcation diagram.

Pictures need hundreds of thousands of points, so the escape time here is
the chapter's rule run on whole numpy arrays at once. It is the same rule as
chaoslab.escape_time -- square, add c, stop when the length passes 2 -- with
the real and imaginary parts written out. Plots are not gated; the page's
numbers come from code/measure/ch12.py.
"""

from __future__ import annotations

import numpy as np
from _style import BLUE, RED, T, main, new, num, plot
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle

from chaoslab import r_to_c

# White far outside, the book's blue near the edge; the set itself is ink.
SHADE = LinearSegmentedColormap.from_list(
    "escape", ["#FFFFFF", "#C9D8E8", "#6A93BF", BLUE, "#0B1D30"])
INK = "#111111"
Box = tuple[float, float, float, float]


def escape_grid(zx: np.ndarray, zy: np.ndarray, cx: np.ndarray,
                cy: np.ndarray, limit: int) -> np.ndarray:
    """The escape step of every point of a grid; `limit` means never."""
    shape = np.shape(zx)
    x = zx.astype(float).ravel()
    y = zy.astype(float).ravel()
    ax = np.broadcast_to(cx, shape).astype(float).ravel()
    ay = np.broadcast_to(cy, shape).astype(float).ravel()
    steps = np.full(x.shape, limit)
    alive = np.arange(x.size)
    for n in range(limit):
        out = x * x + y * y > 4.0
        steps[alive[out]] = n
        keep = ~out
        alive, x, y, ax, ay = alive[keep], x[keep], y[keep], ax[keep], ay[keep]
        x, y = x * x - y * y + ax, 2.0 * x * y + ay
    return steps.reshape(shape)


def picture(ax, box: Box, steps: np.ndarray, limit: int,
            aspect: str = "equal") -> None:
    """Draw escape steps as an image: ink for the set, shades outside."""
    out = steps < limit
    shade = np.log1p(steps[out])
    ax.set_facecolor(INK)
    ax.imshow(np.ma.masked_where(~out, np.log1p(steps)), origin="lower",
              extent=box, cmap=SHADE, interpolation="nearest",
              vmin=shade.min(), vmax=shade.max(), aspect=aspect)
    ax.set_xlim(box[0], box[1])
    ax.set_ylim(box[2], box[3])


def mandelbrot(box: Box, nx: int, limit: int) -> np.ndarray:
    """Escape steps of the orbit of 0 for every c on an nx-wide grid."""
    x0, x1, y0, y1 = box
    ny = int(round(nx * (y1 - y0) / (x1 - x0)))
    cx, cy = np.meshgrid(np.linspace(x0, x1, nx), np.linspace(y0, y1, ny))
    zero = np.zeros_like(cx)
    return escape_grid(zero, zero, cx, cy, limit)


def square(ax, box: Box, name: str) -> None:
    ax.add_patch(Rectangle((box[0], box[2]), box[1] - box[0],
                           box[3] - box[2], fill=False, ec=RED, lw=0.9))
    ax.text(box[1] + 0.03, box[3], name, color=RED, fontsize=8,
            va="bottom")


def bare(ax) -> None:
    ax.set_xticks([])
    ax.set_yticks([])
    for side in ax.spines.values():
        side.set_visible(False)


@plot("ch12-mandelbrot")
def the_set(lang: str):
    fig, axes = new(height=4.3, nrows=2, ncols=2)
    whole: Box = (-2.2, 0.6, -1.25, 1.25)
    a: Box = (-0.80, -0.70, 0.05, 0.15)          # the seahorse valley
    inner: Box = (-0.7475, -0.7425, 0.1075, 0.1125)
    b: Box = (-1.80, -1.70, -0.05, 0.05)         # on the needle
    width = whole[1] - whole[0]

    def closer(box: Box) -> str:
        return num(lang, width / (box[1] - box[0]), ".0f")

    top_left, top_right = axes[0]
    low_left, low_right = axes[1]
    picture(top_left, whole, mandelbrot(whole, 600, 200), 200)
    square(top_left, a, "A")
    square(top_left, b, "B")
    top_left.set_xlabel(T(lang, "real part of c", "część rzeczywista c"),
                        labelpad=1)
    top_left.set_ylabel(T(lang, "imaginary part", "część urojona"))
    top_left.set_title(T(lang, "The whole set", "Cały zbiór"))

    picture(top_right, a, mandelbrot(a, 500, 1000), 1000)
    square(top_right, inner, "")
    bare(top_right)
    top_right.set_title(T(lang, f"Square A, {closer(a)} times closer",
                          f"Kwadrat A, {closer(a)} razy bliżej"))

    picture(low_left, inner, mandelbrot(inner, 500, 1000), 1000)
    bare(low_left)
    low_left.set_title(T(lang, f"Inside A, {closer(inner)} times closer",
                         f"Wewnątrz A, {closer(inner)} razy bliżej"))

    picture(low_right, b, mandelbrot(b, 500, 1000), 1000)
    bare(low_right)
    low_right.set_title(T(lang, f"Square B, {closer(b)} times closer",
                          f"Kwadrat B, {closer(b)} razy bliżej"))
    fig.tight_layout(h_pad=0.8)
    return fig


def julia(c: complex, box: Box, nx: int, limit: int) -> np.ndarray:
    """Escape steps of every START z on an nx-wide grid, for a fixed c."""
    x0, x1, y0, y1 = box
    ny = int(round(nx * (y1 - y0) / (x1 - x0)))
    zx, zy = np.meshgrid(np.linspace(x0, x1, nx), np.linspace(y0, y1, ny))
    return escape_grid(zx, zy, np.array(c.real), np.array(c.imag), limit)


def label(lang: str, c: complex) -> str:
    re_part = num(lang, c.real, ".0f" if c.real.is_integer() else ".1f")
    text = f"c = {re_part}"
    if c.imag:
        text += f" + {num(lang, c.imag, '.1f')}i"
    return text.replace("-", "−")


@plot("ch12-julia")
def two_julias(lang: str):
    fig, (left, right) = new(height=2.2, ncols=2)
    box: Box = (-1.8, 1.8, -1.1, 1.1)
    for ax, c, en, pl in (
        (left, complex(-1.0, 0.0), "one piece", "jeden kawałek"),
        (right, complex(-0.8, 0.2), "dust", "pył"),
    ):
        picture(ax, box, julia(c, box, 700, 300), 300)
        bare(ax)
        ax.set_title(f"{label(lang, c)}: {T(lang, en, pl)}")
    fig.tight_layout()
    return fig


@plot("ch12-real-axis")
def real_axis(lang: str):
    fig, (top, bottom) = new(height=4.1, nrows=2, sharex=True,
                             gridspec_kw={"height_ratios": [1.0, 1.3]})
    strip: Box = (-2.05, 0.35, -0.4, 0.4)
    picture(top, strip, mandelbrot(strip, 900, 300), 300, aspect="auto")
    top.set_ylabel(T(lang, "imaginary part", "część urojona"))
    top.set_title(T(lang, "The Mandelbrot set along the real axis",
                    "Zbiór Mandelbrota wzdłuż osi rzeczywistej"))
    # Chapter 8's diagram, each r drawn at its c = r/2 - r*r/4.
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
    bottom.set_xlabel("c")
    bottom.set_ylabel(T(lang, "where x settles", "gdzie osiada x"))
    marks = ((3.0, ".0f"), (1 + 6 ** 0.5, ".2f"),
             (3.5699456718695445, ".2f"), (1 + 8 ** 0.5, ".2f"))
    for r, fmt in marks:
        c = r_to_c(r)
        for ax in (top, bottom):
            ax.axvline(c, color=RED, lw=0.7, ls="--")
        bottom.text(c + 0.012, 0.03, f"r = {num(lang, r, fmt)}", color=RED,
                    fontsize=7, rotation=90, va="bottom", ha="left",
                    bbox={"fc": "white", "ec": "none", "pad": 0.6})
    fig.tight_layout(h_pad=0.4)
    return fig


if __name__ == "__main__":
    main()
