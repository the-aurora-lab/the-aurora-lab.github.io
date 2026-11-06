"""Every Comment Answered icon: a reviewer's comment (speech bubble, ticked) linked to the changed line of a page.
Run from the site root: ../.venv/bin/python src/every-comment-answered/logo.py  (uses research-pipeline's logo_base)."""
import sys
from pathlib import Path

from matplotlib.patches import FancyBboxPatch, Polygon

SITE = Path(__file__).resolve().parents[2]
sys.path += [str(d / "research-pipeline" / "tools") for d in (SITE.parent, SITE.parent.parent)]  # checkout or _work/ worktree
from logo_base import INK, MUTED, ORANGE, TEAL, make_logo  # noqa: E402


def glyph(ax):
    # the page, lower right
    ax.add_patch(FancyBboxPatch((0.47, 0.25), 0.26, 0.33, boxstyle="round,pad=0,rounding_size=0.02",
                                fc="white", ec=INK, lw=1.4, zorder=3))
    for i, y in enumerate((0.51, 0.455, 0.40, 0.345, 0.29)):
        x1 = 0.68 if i != 4 else 0.61
        if i == 2:
            ax.add_patch(FancyBboxPatch((0.505, y - 0.017), 0.19, 0.034, boxstyle="round,pad=0,rounding_size=0.012",
                                        fc=TEAL, ec="none", alpha=0.22, zorder=4))
            ax.plot([0.52, x1], [y, y], color=TEAL, lw=1.6, solid_capstyle="round", zorder=5)
        else:
            ax.plot([0.52, x1], [y, y], color=MUTED, lw=1.2, solid_capstyle="round", zorder=5)
    # the comment bubble, upper left
    ax.add_patch(FancyBboxPatch((0.25, 0.53), 0.25, 0.17, boxstyle="round,pad=0,rounding_size=0.04",
                                fc="white", ec=INK, lw=1.4, zorder=6))
    ax.add_patch(Polygon([(0.30, 0.535), (0.285, 0.48), (0.345, 0.535)], closed=True, fc="white", ec="none", zorder=7))
    ax.plot([0.30, 0.285, 0.345], [0.531, 0.48, 0.531], color=INK, lw=1.4, solid_joinstyle="round", zorder=7)
    ax.plot([0.315, 0.355, 0.43], [0.615, 0.575, 0.66], color=TEAL, lw=2.0, solid_capstyle="round",
            solid_joinstyle="round", zorder=8)
    # the link from the comment to the changed line
    ax.plot([0.46, 0.505], [0.545, 0.40], color=ORANGE, lw=1.3, ls=(0, (2, 1.6)), zorder=4)
    ax.scatter([0.505], [0.40], s=10, color=ORANGE, zorder=9, lw=0)


make_logo(glyph, str(SITE / "assets" / "img" / "every-comment-answered.png"))
