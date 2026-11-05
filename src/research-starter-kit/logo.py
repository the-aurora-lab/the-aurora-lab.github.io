"""Research Starter Kit icon: a shield (the guards) holding the lines of a ledger (the record of AI use).
Run from the site root: ../.venv/bin/python src/research-starter-kit/logo.py  (uses research-pipeline's logo_base)."""
import sys
from pathlib import Path

from matplotlib.patches import Polygon

SITE = Path(__file__).resolve().parents[2]
sys.path += [str(d / "research-pipeline" / "tools") for d in (SITE.parent, SITE.parent.parent)]  # checkout or _work/ worktree
from logo_base import INK, MUTED, ORANGE, TEAL, make_logo  # noqa: E402


def glyph(ax):
    cx, top, bot, w = 0.5, 0.69, 0.25, 0.19
    pts = [(cx - w, top - 0.03), (cx, top + 0.01), (cx + w, top - 0.03), (cx + w, 0.47),
           (cx + 0.11, 0.33), (cx, bot), (cx - 0.11, 0.33), (cx - w, 0.47)]
    ax.add_patch(Polygon(pts, closed=True, fc=TEAL, ec="none", alpha=0.14, zorder=2))
    ax.add_patch(Polygon(pts, closed=True, fc="none", ec=INK, lw=1.5, joinstyle="round", zorder=3))
    for i, (y, length) in enumerate(((0.56, 0.17), (0.49, 0.2), (0.42, 0.14))):
        x0 = cx - 0.1
        ax.plot([x0 + 0.045, x0 + 0.045 + length], [y, y], color=MUTED if i else INK, lw=1.3,
                solid_capstyle="round", zorder=4)
        ax.scatter([x0], [y], s=12, color=TEAL if i < 2 else ORANGE, zorder=5, lw=0)


make_logo(glyph, str(SITE / "assets" / "img" / "research-starter-kit.png"))
