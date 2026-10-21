"""Write bundles/index.html: the 4 Aurora Lab bundles with Agensi, Gumroad and Polar buy links.

Run from the site root: ../.venv/bin/python src/bundles_page.py
Bundle copy comes from ../research-pipeline/listings/_bundles/<name>/bundle.json; store links are listed below
(source of truth: ../_notes/stores.md).
"""
import html
import json
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
BUNDLES = SITE.parent / "research-pipeline" / "listings" / "_bundles"
AGENSI = {"figures-tables": "publication-ready-figures-tables", "submission-manuscript": "submission-ready-manuscript",
          "talks-posters": "talks-posters-present-your-research", "research-code": "research-code-ready-to-share"}
STORES = {  # name: (gumroad, polar)
    "figures-tables": ("https://theauroralab.gumroad.com/l/figures-tables",
                       "https://buy.polar.sh/polar_cl_kRFA2xypRjnMjlXTKgywf3q2o8btjW7sYyrmB3r4Iar"),
    "submission-manuscript": ("https://theauroralab.gumroad.com/l/submission-manuscript",
                              "https://buy.polar.sh/polar_cl_PXHkEscRBh7FXNjzVs2DrUARpa7u8oUciBzDZ3RcC7X"),
    "talks-posters": ("https://theauroralab.gumroad.com/l/talks-posters",
                      "https://buy.polar.sh/polar_cl_eZSAxJLy8EvYPiJEsPwfwCVDQtPRm4pKV4PMy28Q0xl"),
    "research-code": ("https://theauroralab.gumroad.com/l/research-code",
                      "https://buy.polar.sh/polar_cl_vcqlGQmHwOeqqUiaqb7plqDT1z3G1WMGFBpo40a9M1C"),
}
SLUG = {"Paper Figures": "paper-figures", "Figure Editor": "figure-editor", "Figure Audit": "figure-audit",
        "Table Design": "table-design", "Claim Check": "claim-check", "Scientific Voice": "scientific-voice",
        "Journal House Style": "journal-house-style", "Slide Architect": "slide-architect", "Talk Coach": "talk-coach",
        "Q&A Prep": "qa-prep", "Poster Layout": "poster-layout", "Research Software": "research-software",
        "Instructions Writer": "instructions-writer"}

sections = []
for name, (gum, pol) in STORES.items():
    b = json.loads((BUNDLES / name / "bundle.json").read_text())
    lede = html.escape(b["description"].split("\n")[0])
    items = "".join(f'<li><a href="../skills/{SLUG[s]}/">{html.escape(s)}</a></li>' for s in b["skills"])
    sections.append(f"""      <section id="{name}">
        <h2>{html.escape(b["name"])}</h2>
        <p><strong>${b["price"]} on Agensi</strong> · ${2 * b["price"]} as a direct download · {len(b["skills"])} skills</p>
        <p>{lede}</p>
        <ul>{items}</ul>
        <p class="bundle-buy">
          <a class="btn btn-small" href="https://www.agensi.io/bundles/{AGENSI[name]}">On Agensi (${b["price"]})</a>
          <a class="btn btn-small btn-ghost" href="{gum}">Download via Gumroad (${2 * b["price"]})</a>
          <a class="btn btn-small btn-ghost" href="{pol}">Download via Polar (${2 * b["price"]})</a>
        </p>
      </section>""")

page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Bundles · Aurora Lab</title>
  <meta name="description" content="Aurora Lab skill bundles for researchers: figures and tables, submission-ready manuscripts, talks and posters, research code. On Agensi, or as direct downloads via Gumroad or Polar.">
  <meta property="og:title" content="Bundles · Aurora Lab">
  <meta property="og:image" content="https://the-aurora-lab.github.io/assets/fig/bifurcation-after.png">
  <meta name="theme-color" content="#0b1020">
  <link rel="canonical" href="https://the-aurora-lab.github.io/bundles/">
  <link rel="icon" type="image/png" href="../assets/img/avatar.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/css/site.css">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="nav">
    <div class="wrap nav-inner">
      <a class="brand" href="../" aria-label="Aurora Lab home">
        <img src="../assets/img/avatar.png" alt="" width="32" height="32">
        <span>Aurora Lab</span>
      </a>
      <nav aria-label="Primary">
        <a href="../#skills">Skills</a>
        <a class="btn btn-small" href="https://www.agensi.io/creators/aurora-lab">Skills on Agensi</a>
      </nav>
    </div>
  </header>

  <main id="main">
    <section class="docs-hero">
      <div class="aurora" aria-hidden="true"></div>
      <div class="wrap">
        <p class="crumbs"><a href="../">Aurora Lab</a> / Bundles</p>
        <h1>Bundles</h1>
        <p class="lede">Four bundles, one research job each. Use them through Agensi, the simplest and cheapest way: your agent loads the latest version whenever you need it. Or buy a direct download you keep (a zip of skill folders with install steps for Claude Code, Codex, Cursor and Gemini CLI, for offline use) via Gumroad or Polar.</p>
      </div>
    </section>
    <div class="wrap docs docs-single">
      <article class="prose-doc">
{chr(10).join(sections)}
      </article>
    </div>
  </main>

  <footer class="footer">
    <div class="wrap footer-inner">
      <span class="brand"><img src="../assets/img/avatar.png" alt="" width="24" height="24"> Aurora Lab</span>
      <nav aria-label="Footer">
        <a href="https://www.agensi.io/creators/aurora-lab">Agensi</a>
        <a href="https://github.com/the-aurora-lab/skills">Free skills on GitHub</a>
        <a href="https://x.com/theauroralab">X</a>
      </nav>
    </div>
  </footer>
</body>
</html>
"""
(SITE / "bundles").mkdir(exist_ok=True)
(SITE / "bundles" / "index.html").write_text(page)
print("wrote bundles/index.html")
