"""Paper Radar (the kit) icon: a radar sweep rising over the horizon like the morning sun, three papers picked out.
Run from the site root: ../.venv/bin/python src/paper-radar/logo.py  (uses research-pipeline's logo_base)."""
import sys
from pathlib import Path

import numpy as np
from matplotlib.patches import Wedge

SITE = Path(__file__).resolve().parents[2]
sys.path += [str(d / "research-pipeline" / "tools") for d in (SITE.parent, SITE.parent.parent)]  # checkout or _work/ worktree
from logo_base import INK, MUTED, ORANGE, TEAL, make_logo  # noqa: E402

CX, CY = 0.5, 0.39


def glyph(ax):
    t = np.linspace(0, np.pi, 200)
    for r in (0.07, 0.14, 0.21):
        ax.plot(CX + r * np.cos(t), CY + r * np.sin(t), color=MUTED, lw=0.9, zorder=2)
    ax.plot([CX - 0.24, CX + 0.24], [CY, CY], color=INK, lw=1.6, solid_capstyle="round", zorder=3)   # the horizon
    ax.add_patch(Wedge((CX, CY), 0.21, 55, 105, fc=TEAL, ec="none", alpha=0.18, zorder=2))
    a = np.deg2rad(105)
    ax.plot([CX, CX + 0.21 * np.cos(a)], [CY, CY + 0.21 * np.sin(a)], color=TEAL, lw=1.8,
            solid_capstyle="round", zorder=4)
    ax.add_patch(Wedge((CX, CY), 0.035, 0, 180, fc=ORANGE, ec="none", zorder=4))                     # the sun
    rng = np.random.default_rng(11)
    for _ in range(12):
        r, th = rng.uniform(0.06, 0.2), rng.uniform(0.15, np.pi - 0.15)
        ax.scatter([CX + r * np.cos(th)], [CY + r * np.sin(th)], s=4, color=MUTED, zorder=3, lw=0)
    for r, deg, col in ((0.165, 84, TEAL), (0.1, 64, TEAL), (0.185, 60, ORANGE)):
        th = np.deg2rad(deg)
        ax.scatter([CX + r * np.cos(th)], [CY + r * np.sin(th)], s=14, color=col, zorder=5, lw=0)


make_logo(glyph, str(SITE / "assets" / "img" / "paper-radar-kit.png"))
