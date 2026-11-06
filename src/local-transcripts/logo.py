"""Local Transcripts icon: a sound wave becoming lines of a transcript, one name on it replaced by a tag.
Run from the site root: ../.venv/bin/python src/local-transcripts/logo.py  (uses research-pipeline's logo_base)."""
import sys
from pathlib import Path

from matplotlib.patches import FancyBboxPatch

SITE = Path(__file__).resolve().parents[2]
sys.path += [str(d / "research-pipeline" / "tools") for d in (SITE.parent, SITE.parent.parent)]  # checkout or _work/ worktree
from logo_base import INK, MUTED, ORANGE, TEAL, make_logo  # noqa: E402


def glyph(ax):
    # the sound wave, left
    heights = [0.04, 0.09, 0.16, 0.11, 0.2, 0.13, 0.07, 0.15, 0.1, 0.05]
    for i, h in enumerate(heights):
        x = 0.26 + i * 0.022
        ax.plot([x, x], [0.48 - h / 2, 0.48 + h / 2], color=TEAL, lw=1.5, solid_capstyle="round", zorder=4)
    # the page, right
    ax.add_patch(FancyBboxPatch((0.5, 0.27), 0.25, 0.42, boxstyle="round,pad=0,rounding_size=0.02",
                                fc="white", ec=INK, lw=1.4, zorder=3))
    ys = (0.62, 0.565, 0.51, 0.455, 0.40, 0.345)
    for i, y in enumerate(ys):
        ax.scatter([0.535], [y], s=7, color=TEAL if i % 2 == 0 else ORANGE, zorder=6, lw=0)
        if i == 2:  # a name replaced by a tag
            ax.plot([0.555, 0.585], [y, y], color=MUTED, lw=1.2, solid_capstyle="round", zorder=5)
            ax.add_patch(FancyBboxPatch((0.595, y - 0.018), 0.085, 0.036, boxstyle="round,pad=0,rounding_size=0.01",
                                        fc="white", ec=ORANGE, lw=1.1, zorder=5))
            ax.plot([0.69, 0.715], [y, y], color=MUTED, lw=1.2, solid_capstyle="round", zorder=5)
        else:
            x1 = 0.715 if i not in (1, 5) else 0.66
            ax.plot([0.555, x1], [y, y], color=MUTED, lw=1.2, solid_capstyle="round", zorder=5)


make_logo(glyph, str(SITE / "assets" / "img" / "local-transcripts.png"))
