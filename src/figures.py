"""Generate every figure and number shown on the site.

Run from the repo root:  python src/figures.py
Writes assets/fig/*.png|svg and src/feigenbaum.json. Fails loudly if a
computed value drifts from its known reference.
"""
import json
import math
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, PowerNorm

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "assets" / "fig"
FIG.mkdir(parents=True, exist_ok=True)
CHECK_DIR = os.environ.get("CHECK_DIR")      # optional: also write PNG previews of vector figures here

R_MIN, R_MAX = 2.8, 4.0
W_PX, H_PX, DPI = 1600, 1000, 200          # before/after must match exactly for the slider
AXES_RECT = [0.085, 0.12, 0.885, 0.76]      # shared plot area, so r lines up across the slider handle
R1, R2 = 3.0, 1 + math.sqrt(6)             # first two period-doubling points (exact)
R_INF = 3.569945672                        # accumulation point of the cascade
R_P3 = 1 + math.sqrt(8)                    # birth of the period-3 window
DELTA = 4.669201609102990                  # Feigenbaum's constant (reference)

AURORA = LinearSegmentedColormap.from_list(
    "aurora", ["#99f6e4", "#2dd4bf", "#0d9488", "#115e59", "#0b1020"])
INK, TEAL, VIOLET, MUTED = "#0b1020", "#0d9488", "#7c3aed", "#64748b"


def orbit_samples(r, n_transient=1000, n_keep=600, x0=0.31):
    """Iterate every r in parallel; return the post-transient states, shape (n_keep, len(r))."""
    x = np.full_like(r, x0)
    for _ in range(n_transient):
        x = r * x * (1 - x)
    out = np.empty((n_keep, r.size))
    for k in range(n_keep):
        x = r * x * (1 - x)
        out[k] = x
    return out


def lyapunov(r, n_transient=1000, n_avg=3000, x0=0.31):
    x = np.full_like(r, x0)
    for _ in range(n_transient):
        x = r * x * (1 - x)
    acc = np.zeros_like(r)
    for _ in range(n_avg):
        x = r * x * (1 - x)
        acc += np.log(np.maximum(np.abs(r * (1 - 2 * x)), 1e-300))
    return acc / n_avg


def publication_style():
    plt.rcParams.update({
        "font.family": "STIXGeneral", "mathtext.fontset": "stix", "font.size": 11,
        "axes.edgecolor": INK, "axes.labelcolor": INK, "axes.linewidth": 0.8,
        "xtick.color": INK, "ytick.color": INK, "xtick.direction": "out", "ytick.direction": "out",
        "axes.spines.top": False, "axes.spines.right": False,
    })


def density_image(ax, x_bins, r_cols=W_PX, n_keep=1500):
    """x_bins should match the axes height in pixels, or thin branches alias into dashes."""
    r = np.linspace(R_MIN, R_MAX, r_cols)
    xs = orbit_samples(r, n_keep=n_keep)
    hist = np.zeros((x_bins, r_cols))
    idx = np.clip((xs * x_bins).astype(int), 0, x_bins - 1)
    for col in range(r_cols):
        np.add.at(hist[:, col], idx[:, col], 1)
    hist[hist == 0] = np.nan
    ax.imshow(hist, origin="lower", aspect="auto", extent=(R_MIN, R_MAX, 0, 1),
              cmap=AURORA, norm=PowerNorm(gamma=0.35, vmin=1, vmax=0.25 * n_keep), interpolation="antialiased")
    ax.set_xlim(R_MIN, R_MAX)
    ax.set_ylim(0, 1)


def annotate_cascade(ax, y_text=1.02, labels=True):
    marks = [(R1, r"$r_1=3$"), (R2, r"$r_2=1+\sqrt{6}$"), (R_INF, r"$r_\infty$"), (R_P3, "period 3")]
    for r, lab in marks:
        ax.axvline(r, color=VIOLET if r == R_INF else MUTED, lw=0.7, ls=(0, (3, 3)), zorder=0)
        if labels:
            ax.text(r, y_text, lab, transform=ax.get_xaxis_transform(), ha="center", va="bottom",
                    fontsize=9.5, color=VIOLET if r == R_INF else MUTED)


def fig_before():
    with plt.style.context("default"):
        plt.rcdefaults()
        fig = plt.figure(figsize=(W_PX / DPI, H_PX / DPI), dpi=DPI)
        ax = fig.add_axes(AXES_RECT)               # default look, but the same geometry as "after"
        r = np.linspace(R_MIN, R_MAX, 1200)
        xs = orbit_samples(r, n_keep=200)
        ax.plot(np.broadcast_to(r, xs.shape).ravel(), xs.ravel(), "b.", markersize=1)
        ax.set_xlim(R_MIN, R_MAX)
        ax.set_ylim(0, 1)
        ax.set_title("bifurcation")
        ax.set_xlabel("r")
        ax.set_ylabel("x")
        fig.savefig(FIG / "bifurcation-before.png", dpi=DPI)
        corners = ax.transData.transform([(R_MIN, 0), (R_MAX, 1)])
        plt.close(fig)
        return corners


def fig_after():
    publication_style()
    fig = plt.figure(figsize=(W_PX / DPI, H_PX / DPI), dpi=DPI)
    ax = fig.add_axes(AXES_RECT)
    density_image(ax, x_bins=int(0.76 * H_PX))
    annotate_cascade(ax)
    ax.set_xlabel(r"growth parameter $r$")
    ax.set_ylabel(r"long-run state $x$")
    ax.text(3.08, 0.08, r"$x_{n+1} = r\,x_n(1-x_n)$", fontsize=12, color=INK)
    ax.text(3.585, 0.035, "chaos + periodic windows", fontsize=9.5, color=MUTED)
    fig.savefig(FIG / "bifurcation-after.png", dpi=DPI)
    corners = ax.transData.transform([(R_MIN, 0), (R_MAX, 1)])
    plt.close(fig)
    return corners


def fig_panel():
    publication_style()
    fig, (a, b) = plt.subplots(2, 1, figsize=(8, 6.2), dpi=DPI, sharex=True,
                               gridspec_kw={"height_ratios": [1.5, 1], "hspace": 0.08})
    density_image(a, x_bins=650)
    annotate_cascade(a)
    annotate_cascade(b, labels=False)
    a.set_ylabel(r"$x$")
    r = np.linspace(R_MIN, R_MAX, 2400)
    lam = lyapunov(r)
    b.axhline(0, color=INK, lw=0.6)
    b.fill_between(r, 0, lam, where=lam > 0, color=TEAL, alpha=0.35, lw=0)
    b.plot(r, lam, color=INK, lw=0.6)
    b.set_ylim(-2.2, 0.9)
    b.set_ylabel(r"Lyapunov exponent $\lambda$")
    b.set_xlabel(r"$r$")
    b.text(2.83, 0.45, r"$\lambda>0$: chaotic", color=TEAL, fontsize=10)
    for ax, tag in ((a, "a"), (b, "b")):
        ax.text(-0.12, 1.0, f"({tag})", transform=ax.transAxes, fontsize=12, fontweight="bold", va="top")
    fig.savefig(FIG / "panel.png", dpi=DPI, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    return r, lam


def fig_cobwebs():
    publication_style()
    cases = [(2.8, "fixed point"), (3.2, "period 2"), (3.5, "period 4"), (3.9, "chaos")]
    fig, axes = plt.subplots(1, 4, figsize=(10, 2.8), sharey=True)
    grid = np.linspace(0, 1, 400)
    for ax, (r, lab) in zip(axes, cases):
        ax.plot(grid, r * grid * (1 - grid), color=INK, lw=1)
        ax.plot([0, 1], [0, 1], color=MUTED, lw=0.6, ls=(0, (3, 3)))
        x = 0.1
        if r > 3:                                  # cycles/chaos: settle first, then draw the attractor's web
            for _ in range(300):                   # (a fixed point would collapse to a dot, so show the spiral in)
                x = r * x * (1 - x)
        px, py = [x], [x]
        for _ in range(60):
            y = r * x * (1 - x)
            px += [x, y]
            py += [y, y]
            x = y
        ax.plot(px, py, color=TEAL, lw=0.8)
        ax.set_title(f"$r={r}$  ·  {lab}", fontsize=10.5, color=INK)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal")
        ax.set_xticks([0, 0.5, 1])
        ax.set_yticks([0, 0.5, 1])
        ax.set_xlabel(r"$x_n$")
    axes[0].set_ylabel(r"$x_{n+1}$")
    fig.tight_layout()
    fig.savefig(FIG / "cobweb.svg", metadata={"Date": None})   # no timestamp: reruns give identical files
    if CHECK_DIR:
        fig.savefig(Path(CHECK_DIR) / "cobweb-check.png", dpi=150)
    plt.close(fig)


def superstable_parameters(n_max=11):
    # n_max=11 is the sweet spot in float64: delta's error is 7e-8 there, then grows (1e-6 at 12, third decimal by 16).
    """R_n: parameter where x=1/2 lies on a superstable 2^n-cycle. Newton on g(r)=f_r^{2^n}(1/2)-1/2."""
    R = [2.0, 1 + math.sqrt(5)]
    for n in range(2, n_max + 1):
        r = R[-1] + (R[-1] - R[-2]) / DELTA         # Feigenbaum scaling gives an excellent first guess
        for _ in range(60):
            x, dx = 0.5, 0.0
            for _ in range(2 ** n):
                x, dx = r * x * (1 - x), x * (1 - x) + r * (1 - 2 * x) * dx
            step = (x - 0.5) / dx
            r -= step
            if abs(step) < 1e-15:
                break
        R.append(r)
    return R


def main():
    before_px = fig_before()
    after_px = fig_after()
    r, lam = fig_panel()
    fig_cobwebs()

    R = superstable_parameters()
    rows = []
    for n, rn in enumerate(R):
        d = (R[n - 1] - R[n - 2]) / (rn - R[n - 1]) if n >= 2 else None
        rows.append({"n": n, "period": 2 ** n, "R": rn, "delta": d})
    (ROOT / "src" / "feigenbaum.json").write_text(json.dumps(rows, indent=2))

    # Invariants: if any of these fail, the site would be showing a wrong number or a broken slider.
    from matplotlib.image import imread
    b, a = imread(FIG / "bifurcation-before.png"), imread(FIG / "bifurcation-after.png")
    assert b.shape[:2] == a.shape[:2] == (H_PX, W_PX), (b.shape, a.shape)
    assert np.allclose(before_px, after_px, atol=0.5), (before_px, after_px)   # slider: same data->pixel map
    assert abs(R[1] - (1 + math.sqrt(5))) < 1e-12
    assert abs(R[2] - 3.498561699327702) < 1e-9, R[2]
    assert abs(R[3] - 3.554640862768825) < 1e-9, R[3]
    assert all(R[i] < R[i + 1] < R_INF for i in range(len(R) - 1)), "R_n must increase toward r_inf"
    assert abs(rows[-1]["delta"] - DELTA) < 1e-4, rows[-1]["delta"]
    assert lam[np.searchsorted(r, 3.9)] > 0 and lam[np.searchsorted(r, 3.2)] < 0, "chaos/periodic sign check"
    w = (r > 3.8284) & (r < 3.8415)                 # inside the period-3 window lambda must be negative
    assert lam[w].max() < 0, lam[w].max()

    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
