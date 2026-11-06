"""Copy the demo runs into the site: python src/local-transcripts/collect_runs.py <demo dir> <playwright python>

<demo dir> holds what the tool's demo produced (see the tool repository's demo/README):
  interview/console.txt                 the command and its output, verbatim
  interview/transcripts/...             the project (consultation folder, shareable/, anonymisation/)
  lecture/console.txt, lecture/transcripts/<talk>/ (lecture.html, slides/, notes.md, notes.pdf), lecture/agent.json
Writes runs/interview.html and runs/lecture.html (the page's run sections), samples (review page, shareable copy,
notes PDF, lecture page) under tools/local-transcripts/samples/, and screenshots under assets/shots/local-transcripts/.
"""
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parent.parent
SAMPLES = SITE / "tools" / "local-transcripts" / "samples"
SHOTS = SITE / "assets" / "shots" / "local-transcripts"
RUNS = HERE / "runs"


def esc(s: str) -> str:
    return html.escape(s.rstrip("\n"))


def first_turns(txt: str, n: int) -> str:
    body = [b for b in txt.split("\n\n") if b.startswith("[")]
    return "\n\n".join(body[:n])


def shot(py: str, src: Path, out: Path, width: int = 760, height: int = 900, selector: str = "") -> None:
    code = f"""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.connect_over_cdp("http://localhost:9222")
    page = b.contexts[0].new_page()
    page.emulate_media(color_scheme="light")
    page.set_viewport_size({{"width": {width}, "height": {height}}})
    page.goto({src.resolve().as_uri()!r}, wait_until="load")
    page.wait_for_timeout(600)
    page.screenshot(path={str(out)!r}, full_page=False)
    page.close()
"""
    subprocess.run([py, "-I", "-c", code], check=True)


def names_block(demo: Path) -> str:
    """The pseudonymising demo: a made-up interview with planted names, run with a names list."""
    nv = demo / "interview-names"
    if not nv.exists():
        return ""
    proj = nv / "transcripts"
    rec = next(p for p in proj.iterdir() if (p / "transcript.json").exists())
    stem = rec.name
    raw = (rec / f"{stem}.txt").read_text(encoding="utf-8")
    shared = (proj / "shareable" / f"{stem}.txt").read_text(encoding="utf-8")
    key = (proj / "anonymisation" / "key.csv").read_text(encoding="utf-8").splitlines()
    key = [k for k in key if "-part" not in k][:9]
    shutil.copyfile(proj / "shareable" / f"{stem}.txt", SAMPLES / f"{stem}-pseudonymised.txt")
    return f"""<h3>Pseudonymising</h3>
<p>{(nv / "about.html").read_text(encoding="utf-8")}</p>
<pre class="term">{esc((nv / "names.txt").read_text(encoding="utf-8"))}</pre>
<pre class="term">{esc((nv / "console.txt").read_text(encoding="utf-8"))}</pre>
<p>As said (<code>{stem}/{stem}.txt</code>):</p>
<pre class="term">{esc(first_turns(raw, 4))}</pre>
<p>As shared (<code>shareable/{stem}.txt</code>):</p>
<pre class="term">{esc(first_turns(shared, 4))}</pre>
<p>The key, kept apart from the shareable files (<code>anonymisation/key.csv</code>; edit a replacement to write
<code>[a town in the north]</code> instead, or empty it to keep the word):</p>
<pre class="term">{esc(chr(10).join(key))}</pre>
<p><a href="samples/{stem}-pseudonymised.txt">The whole shareable transcript</a>.</p>"""


def main():
    demo, py = Path(sys.argv[1]), sys.argv[2]
    for d in (SAMPLES, SHOTS, RUNS):
        d.mkdir(parents=True, exist_ok=True)
    # interview
    iv = demo / "interview"
    proj = iv / "transcripts"
    rec = next(p for p in proj.iterdir() if (p / "transcript.json").exists())
    stem = rec.name
    raw = (rec / f"{stem}.txt").read_text(encoding="utf-8")
    shared = (proj / "shareable" / f"{stem}.txt").read_text(encoding="utf-8")
    maxqda = (proj / "shareable" / f"{stem}.maxqda.txt").read_text(encoding="utf-8")
    nvivo = (proj / "shareable" / f"{stem}.nvivo.tsv").read_text(encoding="utf-8")
    shutil.copyfile(proj / "shareable" / f"{stem}.txt", SAMPLES / f"{stem}-pseudonymised.txt")
    shutil.copyfile(proj / "shareable" / f"{stem}.docx", SAMPLES / f"{stem}-pseudonymised.docx")
    review = (rec / "review.html").read_text(encoding="utf-8")
    review = re.sub(r'<audio id="m"[^>]*></audio>', "", review)  # the recording itself is not republished
    (SAMPLES / "review.html").write_text(review, encoding="utf-8")
    shot(py, SAMPLES / "review.html", SHOTS / "review.png", 760, 620)
    (RUNS / "interview-console.txt").write_text((iv / "console.txt").read_text(encoding="utf-8"), encoding="utf-8")
    n = int((iv / "turns_shown.txt").read_text().strip()) if (iv / "turns_shown.txt").exists() else 8
    (RUNS / "interview.html").write_text(f"""
<p>{(iv / "about.html").read_text(encoding="utf-8")}</p>
<pre class="term">{esc((iv / "console.txt").read_text(encoding="utf-8"))}</pre>
<p>The opening of the transcript (<code>{stem}/{stem}.txt</code>, also the file you edit):</p>
<pre class="term">{esc(first_turns(raw, n))}</pre>
<p>The review page: click a time to hear that moment, unsure words underlined (the recording itself is not
included in the sample):</p>
<p><a href="samples/review.html"><img class="shot" src="../../assets/shots/local-transcripts/review.png"
alt="Review page: turns with speakers in colour, times on the left, unsure words underlined" width="760"></a></p>
<p>For MAXQDA's focus-group import (<code>shareable/{stem}.maxqda.txt</code>):</p>
<pre class="term">{esc(chr(10).join(maxqda.splitlines()[:7]))}</pre>
<p>For NVivo on Windows (<code>shareable/{stem}.nvivo.tsv</code>):</p>
<pre class="term">{esc(chr(10).join(nvivo.splitlines()[:4]))}</pre>
<p>Open them whole: <a href="samples/{stem}-pseudonymised.txt">the transcript</a>,
<a href="samples/{stem}-pseudonymised.docx">as Word</a>, <a href="samples/review.html">the review page</a>.</p>
{names_block(demo)}
""", encoding="utf-8")
    # lecture
    lv = demo / "lecture"
    lp = next(p for p in (lv / "transcripts").iterdir() if (p / "slides.json").exists())
    for f in ("lecture.html", "notes.md"):
        if (lp / f).exists():
            shutil.copyfile(lp / f, SAMPLES / f)
    if (SAMPLES / "slides").exists():
        shutil.rmtree(SAMPLES / "slides")
    (SAMPLES / "slides").mkdir()
    for png in sorted((lp / "slides").glob("*.png")):  # lighter stills for the web: JPEG, 1100 px wide
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(png), "-vf", "scale='min(1100,iw)':-2",
                        "-q:v", "4", str(SAMPLES / "slides" / (png.stem + ".jpg"))], check=True)
    lec = (SAMPLES / "lecture.html").read_text(encoding="utf-8")
    lec = re.sub(r'<video id="m"[^>]*></video>', "", lec).replace(".png\"", ".jpg\"")
    (SAMPLES / "lecture.html").write_text(lec, encoding="utf-8")
    md = (SAMPLES / "notes.md").read_text(encoding="utf-8").replace(".png)", ".jpg)")
    (SAMPLES / "notes.md").write_text(md, encoding="utf-8")
    if (lp / "notes.tex").exists():  # the sample PDF, rebuilt with the lighter stills and in UTC
        import os
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            shutil.copytree(SAMPLES / "slides", Path(d) / "slides")
            (Path(d) / "notes.tex").write_text((lp / "notes.tex").read_text(encoding="utf-8").replace(".png}", ".jpg}"),
                                               encoding="utf-8")
            env = dict(os.environ, TZ="UTC", SOURCE_DATE_EPOCH="1767225600", FORCE_SOURCE_DATE="1")
            for _ in range(2):
                subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "notes.tex"], cwd=d,
                               capture_output=True, env=env)
            shutil.copyfile(Path(d) / "notes.pdf", SAMPLES / "notes.pdf")
    shot(py, SAMPLES / "lecture.html", SHOTS / "lecture.png", 760, 760)
    if (SAMPLES / "notes.pdf").exists():
        subprocess.run(["pdftoppm", "-r", "90", "-png", "-f", "3", "-l", "3", str(SAMPLES / "notes.pdf"),
                        str(SHOTS / "notes-page")], check=True)
    agent = json.loads((lv / "agent.json").read_text()) if (lv / "agent.json").exists() else {}
    notes = (lp / "notes.md").read_text(encoding="utf-8") if (lp / "notes.md").exists() else ""
    sec = notes.split("\n## ")
    pick = next((i for i, x in enumerate(sec) if i >= 10 and x.count("$$") >= 4), 3)
    excerpt = "## " + sec[pick]
    (RUNS / "lecture.html").write_text(f"""
<p>{(lv / "about.html").read_text(encoding="utf-8")}</p>
<pre class="term">{esc((lv / "console.txt").read_text(encoding="utf-8"))}</pre>
<p><code>lecture.html</code>: each slide's still with what was said while it was on screen:</p>
<p><a href="samples/lecture.html"><img class="shot" src="../../assets/shots/local-transcripts/lecture.png"
alt="Lecture page: a slide still with the transcript of what was said under it" width="760"></a></p>
<p>Then one unattended Claude Code session (Claude Sonnet 5.5) with the skill installed got the request a student would
type: write study notes with the equations in LaTeX. It took {agent.get("seconds", "?")} seconds and cost
${agent.get("cost_usd", 0):.2f}; <code>notes check</code> then reported {html.escape(agent.get("check", ""))}. One
section of its <code>notes.md</code>, as written:</p>
<pre class="term">{esc(excerpt.strip())}</pre>
<p>And a page of <code>notes.pdf</code> from <code>notes tex --pdf</code>:</p>
<p><a href="samples/notes.pdf"><img class="shot" src="../../assets/shots/local-transcripts/notes-page-03.png"
alt="A page of the notes PDF: a slide still, the notes and equations typeset" width="760"></a></p>
<p>Open them whole: <a href="samples/lecture.html">lecture.html</a>, <a href="samples/notes.md">notes.md</a>,
<a href="samples/notes.pdf">notes.pdf</a>.</p>
""", encoding="utf-8")
    print("collected", stem, lp.name)


if __name__ == "__main__":
    main()
