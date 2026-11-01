"""Reference Verifier icon: a numbered reference list, three entries checked, one flagged.
Run from the site root: ../.venv/bin/python src/reference-verifier/logo.py  (uses research-pipeline's logo_base)."""
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parents[2]
sys.path += [str(d / "research-pipeline" / "tools") for d in (SITE.parent, SITE.parent.parent)]  # checkout or _work/ worktree
from logo_base import INK, MUTED, ORANGE, TEAL, make_logo  # noqa: E402


def glyph(ax):
    cap = dict(solid_capstyle="round", zorder=3)
    rows = [0.665, 0.575, 0.485, 0.395, 0.305]
    lengths = [0.25, 0.20, 0.24, 0.17, 0.22]
    for i, (y, ln) in enumerate(zip(rows, lengths)):
        ax.plot([0.27, 0.29], [y, y], color=INK, lw=2.4, **cap)  # the list number
        ax.plot([0.33, 0.33 + ln], [y, y], color=MUTED, lw=2.2, **cap)
        if i == 3:  # the one that is not found: an orange cross
            ax.plot([0.655, 0.705], [y - 0.025, y + 0.025], color=ORANGE, lw=2.0, **cap)
            ax.plot([0.655, 0.705], [y + 0.025, y - 0.025], color=ORANGE, lw=2.0, **cap)
        else:
            ax.plot([0.652, 0.673, 0.712], [y, y - 0.024, y + 0.03], color=TEAL, lw=2.0,
                    solid_capstyle="round", solid_joinstyle="round", zorder=4)


make_logo(glyph, str(SITE / "assets" / "img" / "reference-verifier.png"))
