"""Copy a demo run (the tool's demo/run_demo.py output folder) into the docs page's sources.

Usage (from the site root): ../.venv/bin/python src/every-comment-answered/collect_runs.py <demo run folder> [<playwright python>]

- src/every-comment-answered/runs/: the terminal output of `start`, `changes` and `check`, the agent's answer and
  its time and cost, verbatim;
- tools/every-comment-answered/samples/: the decision letter, the response after the agent's pass, check.md,
  report.html and the revised PDF, as they came out;
- assets/shots/every-comment-answered/: crops of report.html at the page's width (760 css px, 2x).
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parent.parent
RUNS = HERE / "runs"
SAMPLES = SITE / "tools" / "every-comment-answered" / "samples"
SHOTS = SITE / "assets" / "shots" / "every-comment-answered"

SHOT = r'''
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
src, out = Path(sys.argv[1]), Path(sys.argv[2])
exe = sorted(Path.home().glob("Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-mac-arm64/chrome-headless-shell"))[-1]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=str(exe))
    pg = b.new_page(viewport={"width": 760, "height": 900}, device_scale_factor=2)
    pg.goto(src.resolve().as_uri())
    pg.wait_for_timeout(300)
    top = pg.locator("h1").bounding_box()["y"] - 8
    tiles = pg.locator(".tiles").bounding_box()
    pg.screenshot(path=str(out / "report-summary.png"), full_page=True,
                  clip={"x": 0, "y": top, "width": 760, "height": tiles["y"] + tiles["height"] + 16 - top})
    rows = pg.locator("tbody tr")
    flagged = [i for i in range(rows.count()) if rows.nth(i).locator(".p-high, .p-medium").count()]
    head = pg.locator("thead").first.bounding_box()
    first, last = rows.nth(flagged[0]).bounding_box(), rows.nth(flagged[-1]).bounding_box()
    pg.screenshot(path=str(out / "report-problems.png"), full_page=True,
                  clip={"x": 0, "y": first["y"] - 2, "width": 760, "height": last["y"] + last["height"] - first["y"] + 4})
    b.close()
'''


def section(text: str, cmd: str) -> str:
    m = re.search(r"^\$ " + re.escape(cmd) + r"\n(.*?)(?=^\$ |\Z)", text, re.S | re.M)
    return m.group(1).rstrip() + "\n" if m else ""


def main():
    run = Path(sys.argv[1])
    pw = sys.argv[2] if len(sys.argv) > 2 else sys.executable
    RUNS.mkdir(parents=True, exist_ok=True)
    SAMPLES.mkdir(parents=True, exist_ok=True)
    SHOTS.mkdir(parents=True, exist_ok=True)
    term = (run / "terminal.txt").read_text()
    (RUNS / "start.txt").write_text(section(term, "every-comment start decision-letter.txt --old submitted --new revised"))
    (RUNS / "changes.txt").write_text(section(term, "every-comment changes"))
    (RUNS / "check.txt").write_text(section(term, "every-comment check"))
    agent = json.loads((run / "agent.json").read_text())
    (RUNS / "agent.txt").write_text(agent["result"].strip() + "\n")
    (RUNS / "agent.json").write_text(json.dumps({k: v for k, v in agent.items() if k != "result"}, indent=1) + "\n")
    for name in ("decision-letter.txt", "response.md", "check.md", "report.html"):
        shutil.copy2(run / name, SAMPLES / name)
    shutil.copy2(run / "revised-paper.pdf", SAMPLES / "revised-paper.pdf")
    tmp = HERE / "_shot.py"
    tmp.write_text(SHOT)
    try:
        subprocess.run([pw, "-I", str(tmp), str(SAMPLES / "report.html"), str(SHOTS)], check=True)
    finally:
        tmp.unlink()
    for p in list(RUNS.glob("*")) + list(SAMPLES.glob("*")):
        if p.suffix in (".txt", ".md", ".html", ".json") and re.search(r"/Users/|/home/\w", p.read_text(errors="ignore")):
            raise SystemExit(f"{p} names a home folder")
    print("runs, samples and shots written")


if __name__ == "__main__":
    main()
