"""Write tools/every-comment-answered/index.html, the docs page for Every Comment Answered ($19).

Run from the site root: ../.venv/bin/python src/every-comment-answered/page.py
The revision shown is the tool's synthetic demo (demo/run_demo.py in the tool's repository): `every-comment start`,
the authors' replies written in, one unattended Claude Code session with the skill, `every-comment check`. Its
outputs are copied verbatim by collect_runs.py into src/every-comment-answered/runs/ and
tools/every-comment-answered/samples/. Evaluation numbers come from the tool's evals/README.md (held-out set,
scored once). Store links live in STORES; rerun after any change.
"""
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parent.parent
OUT = SITE / "tools" / "every-comment-answered" / "index.html"
RUNS = HERE / "runs"
VERSION = "1.0.1"
PRICE = "$19 once"
STORES = {    # published by the owner 2026-11-06 (step 18)
    "Gumroad": "https://theauroralab.gumroad.com/l/every-comment-answered",
    "Polar": "https://buy.polar.sh/polar_cl_BB0hKEoHAf45E3ZIudWovwK71uI1pAi3S4xkR0FtYyw",
}
GOATCOUNTER = ('<script data-goatcounter="https://auroralabskills.goatcounter.com/count" async '
               'src="//gc.zgo.at/count.js"></script>')
HELDOUT_ROWS = [
    ["Reviewer points found by the split", "276 / 278 (99%)", "97–100%", ""],
    ["… given a comment of their own", "165 / 278 (59%)", "54–65%", ""],
    ["A change holding the answer among the top 3 suggestions", "44 / 64 (69%)", "57–79%", "35 / 45 (78%)"],
    ["Claude Code linked a change holding the answer", "<strong>58 / 64 (91%)</strong>", "81–96%", "43 / 45 (96%)"],
    ["Missing promised changes flagged by the check", "21 / 37 (57%)", "41–71%", "<strong>13 / 22 (59%)</strong>"],
    ["Points flagged although nothing was missing", "64 / 239 (27%)", "22–33%", "23 / 143 (16%)"],
]


def heldout() -> str:
    t = table(["Version 1.0.0, held-out", "All 278 points", "95% CI", "Points with their own comment"], HELDOUT_ROWS)
    return f"""<p>Measured once, on 13 real revisions the tool was never tuned on: 9 SciPost papers (LaTeX from arXiv;
astronomy, mathematical physics, particle physics, condensed matter, cosmology) and 4 F1000Research papers (Word, with
the tracked changes made by Microsoft Word's own Compare; pharmacognosy, biochemistry, clinical pharmacy,
bioinformatics). The reviewers' reports, the authors' real replies and both versions of each paper are public
(CC BY). An independent agent, which never ran the tool or read its code, labelled 278 reviewer points: where each
point is, what the authors replied, and phrases of the revised text that show each change. In a copy of each paper it
then took out again the changes that answer 37 points whose replies still promise them. One Claude Code session
per paper (Sonnet 5.5, a median of 55 seconds, $3.30 for all 13) got the request a user would type, then
<code>every-comment check</code> ran.</p>
{t}
<p>"Points with their own comment" is the cleaner measure of the check: when the split puts several points in one
comment, the authors' replies to all of them sit together, and a flag earned by one is charged to all. The seven
points the authors left without any reply were all flagged as such; those flags are right and not counted above.</p>
<ul>
<li><strong>Every miss among the missing changes</strong> (9 of 22) was a reply the check did not read as a promise:
terse ones such as "Addressed", "→ fixed", "Removed from paper.", "Stated that explicitly", and "we propose to change
…". Version {VERSION} reads these too; that has not been re-measured, and the next held-out set will.</li>
<li><strong>Splitting</strong> finds the points but often keeps neighbours together: reports written as paragraphs
that hold several requests (most F1000Research reports) gave 21 of 65 points a comment of their own, SciPost 144 of
213. Read <code>comments.md</code> once and split by hand where needed.</li>
<li><strong>False alarms</strong> (23): the agent's own "only partly answered" notes on links the labels count as
answers; promises about software or figures, which the tool cannot see; quotes of a paper's title or of text with
math; numbers and places a reply names.</li>
<li>Links to changes the labels do not name are not judged: the labels give one to three phrases per point, not every
change. Page and line numbers were not part of this test (the held-out sources were not compiled); the test suite
checks them against compiled PDFs.</li>
</ul>
<p>The guide in the download carries the same results.</p>"""


def run(name):
    return html.escape((RUNS / name).read_text(encoding="utf-8").rstrip("\n"))


def table(head, rows, num_cols=()):
    th = "".join(f"<th>{h}</th>" for h in head)
    trs = "".join("<tr>" + "".join(f'<td class="num">{c}</td>' if i in num_cols else f"<td>{c}</td>"
                                   for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="doc-table"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


AGENT = json.loads((RUNS / "agent.json").read_text(encoding="utf-8"))
AGENT_MD = (RUNS / "agent.txt").read_text(encoding="utf-8")


def md_inline(s: str) -> str:
    s = html.escape(s)
    import re
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def agent_html(md: str) -> str:
    """The agent's answer (Markdown: paragraphs, lists, one table) as plain HTML, word for word."""
    out, lines, i = [], md.split("\n"), 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("|") and i + 1 < len(lines) and set(lines[i + 1].replace("|", "").strip()) <= set("-: "):
            head = [c.strip() for c in l.strip("|").split("|")]
            rows = []
            i += 2
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([md_inline(c.strip()) for c in lines[i].strip("|").split("|")])
                i += 1
            out.append(table([md_inline(h) for h in head], rows))
            continue
        if l.lstrip().startswith(("- ", "1. ", "2. ", "3. ", "4. ", "5. ")):
            items = []
            while i < len(lines) and lines[i].lstrip().startswith(("- ", "1. ", "2. ", "3. ", "4. ", "5. ")):
                items.append("<li>" + md_inline(lines[i].lstrip()[2:].lstrip(". ")) + "</li>")
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue
        if l.strip():
            out.append(f"<p>{md_inline(l.strip())}</p>")
        i += 1
    return "\n".join(out)


if STORES:
    buy = " ".join(f'<a class="btn btn-small{"" if i == 0 else " btn-ghost"}" href="{u}">Get it on {s}</a>'
                   for i, (s, u) in enumerate(STORES.items()))
    get = ("<p><strong>$19, once.</strong> A zip with the Python wheel (the <code>every-comment</code> command and the "
           "Claude Code skill), a quickstart and the full guide. Updates for 12 months. Personal-use licence; no "
           "licence key.</p>"
           f'<p class="bundle-buy">{buy}</p>')
else:
    get = ("<p><strong>Coming to Gumroad and Polar at $19, once</strong>: a zip with the Python wheel (the "
           "<code>every-comment</code> command and the Claude Code skill), a quickstart and the full guide. Updates for "
           "12 months. Personal-use licence; no licence key.</p>")

BODY = f"""
<section id="what-it-does">
<h2>What it does</h2>
<ol>
<li><strong>Splits the decision letter into numbered comments.</strong> E.1 for the editor, R1.3 for reviewer 1's
third point, each quoted exactly. It reads the layouts journals send: Editorial Manager and ScholarOne letters, PLOS
questionnaires, eLife reviews, SciPost reports, Copernicus comments, F1000Research reports, OJS, with numbered,
lettered, bulleted, line-referenced and section-referenced points.</li>
<li><strong>Finds every change</strong> between the version you submitted and the revised one: LaTeX from a git
tag, a folder or an Overleaf zip (following <code>\\input</code> and <code>\\include</code>), or Word, from a file with
tracked changes or two files. Each change knows its place: section, figure, table, equation, and the page and line
of the revised PDF.</li>
<li><strong>Links each comment to the changes that answer it.</strong> It ranks the likely changes for every comment;
you, or Claude Code with the included skill, confirm each link after reading it.</li>
<li><strong>Writes the response scaffold</strong> in Markdown, LaTeX or Word: every comment quoted, room for your
reply, and the changes listed with their places, kept up to date as you keep editing.</li>
<li><strong>Checks before you resubmit</strong> that every comment has a reply, that every change a reply promises is
linked to a real change, that text a reply quotes is in the paper, that numbers a reply gives are in the paper, and
that the section, figure or page a reply names is where the change is. It also lists changes no comment
explains.</li>
</ol>
<p>It never writes your replies. JAMA's 2026 guidance lists author responses to reviewer and editor comments as not
an acceptable use of AI, and other journals ask authors to disclose AI-written text; Springer Nature lists
structuring reviewer comments as a permitted use. Every Comment Answered stays on the tracking side of that line.</p>
</section>

<section id="a-revision">
<h2>A revision, start to finish</h2>
<p>A short paper made up for this demonstration (bicycle-mounted temperature sensors and urban heat), its submitted
and revised LaTeX versions with line numbers, and a decision letter from an editor and two reviewers. The authors'
replies were written into the scaffold with three mistakes planted for the check to find.</p>
<pre class="term"><span class="p">$ every-comment start decision-letter.txt --old submitted --new revised</span>
{run("start.txt")}</pre>
<p>Every change with its place in the revised PDF:</p>
<pre class="term"><span class="p">$ every-comment changes</span>
{run("changes.txt")}</pre>
<h3>Claude Code links the comments</h3>
<p>Then one unattended Claude Code session (Claude Sonnet 5.5) with the skill installed got the request an author
would type: link each comment to the changes that answer it, refresh the response, check it and say what is missing.
It took {AGENT["seconds"]} seconds and cost ${AGENT["cost_usd"]:.2f}. Its answer, word for word:</p>
<blockquote class="agent">
{agent_html(AGENT_MD)}
</blockquote>
<h3>The check</h3>
<pre class="term"><span class="p">$ every-comment check</span>
{run("check.txt")}</pre>
<p>The same results on one page, <code>revision/report.html</code>:</p>
<p><a href="samples/report.html"><img class="shot" src="../../assets/shots/every-comment-answered/report-summary.png"
alt="Revision check summary: comments with a reply, high and medium problems, changes linked" width="760"></a></p>
<p><a href="samples/report.html"><img class="shot" src="../../assets/shots/every-comment-answered/report-problems.png"
alt="Rows of the revision check with the problems found: a quote not in the paper, no reply, a promised change missing"
width="760"></a></p>
<p>Open them as they came out: <a href="samples/report.html">report.html</a>,
<a href="samples/response.md">response.md</a> (the scaffold with the changes filled in),
<a href="samples/check.md">check.md</a>, <a href="samples/decision-letter.txt">the decision letter</a> and
<a href="samples/revised-paper.pdf">the revised PDF</a>.</p>
</section>

<section id="how-well">
<h2>How well it works</h2>
{heldout()}
</section>

<section id="formats">
<h2>What it reads</h2>
{table(["Input", "Accepted"], [
    ["Decision letter", "Text, Markdown, a saved email (.eml), HTML, Word, or PDF (with <code>pdftotext</code>)"],
    ["LaTeX manuscript", "The current folder against a git tag or commit, another folder, a .tex file or an Overleaf zip; "
     "<code>\\input</code>, <code>\\include</code>, <code>\\subfile</code> and <code>\\import</code> followed; the .aux file's "
     "numbers and pages used when present"],
    ["Word manuscript", "One .docx with tracked changes (insertions, deletions, moves; Word's author and date kept), or "
     "two .docx files without them"],
    ["Page and line numbers", "From the revised PDF built with SyncTeX (<code>pdflatex -synctex=1</code>, latexmk's default), "
     "with <code>\\usepackage{{lineno}}</code> for line numbers; Word gives the page as it last laid the file out"],
    ["Response", "Markdown, LaTeX or Word; your replies are kept every time it is refreshed"],
])}
<p>You can tag a change yourself, <code>% R1.3</code> beside it in LaTeX or a Word comment saying R1.3, and it is
suggested first for that comment.</p>
</section>

<section id="get-it">
<h2>Get it and start</h2>
{get}
<pre><code>pip install every_comment_answered-{VERSION}-py3-none-any.whl
cd my-paper
every-comment start decision-letter.pdf --old submitted     # a git tag, a folder or an Overleaf zip
every-comment setup skill                                    # then ask Claude Code to "help me answer the reviewers"
every-comment check                                          # before resubmitting</code></pre>
<p>Python 3.9 or newer, nothing else installed with it. Works without Claude Code: <code>every-comment changes --near
R1.3</code> and <code>every-comment link R1.3 C12</code> do the linking by hand.</p>
</section>

<section id="privacy">
<h2>What it sends where</h2>
<ul>
<li>Nothing. The command reads your letter and your manuscript and writes a <code>revision/</code> folder beside them;
it makes no network requests and has no telemetry.</li>
<li>With Claude Code, the skill runs the same commands on your computer. Claude Code sends what the agent reads to
Anthropic as it always does; the tool adds nothing to that.</li>
</ul>
</section>

<section id="limits">
<h2>Limits</h2>
<ul>
<li>LaTeX and Word only; a manuscript that exists only as a PDF cannot be compared.</li>
<li>Splitting follows the letter's layout; a letter written as unbroken prose splits by paragraph. Read
<code>comments.md</code> once and merge or split what needs it.</li>
<li>Suggestions come from shared words, quoted phrases, the places a comment names and your tags. A person or the
agent confirms each link; a wrong link hides a missing change from the check.</li>
<li>The check recognises the usual ways of saying the manuscript changed; a promise in unusual words may pass.</li>
<li>Figure images and software are not compared: a redrawn figure shows only through its caption.</li>
<li>Tested on macOS with Python 3.9 and 3.14, TeX Live 2026, Microsoft Word for Mac and Claude Code 2.1.319. Windows is
untested.</li>
</ul>
</section>
"""

SECTIONS = [("what-it-does", "What it does"), ("a-revision", "A revision, start to finish"),
            ("how-well", "How well it works"), ("formats", "What it reads"), ("get-it", "Get it and start"),
            ("privacy", "What it sends where"), ("limits", "Limits")]
TOC = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in SECTIONS)
TITLE = "Every Comment Answered: Each Reviewer Point Matched to Your Changes"
DESC = ("Split the decision letter into numbered comments, see every change in your LaTeX or Word manuscript with its "
        "page and line, link each comment to the changes that answer it, and check before resubmitting that every "
        "promised change is there. It never writes your replies. Held-out evaluation published.")
BUY_CTA = '\n          <a class="btn" href="#get-it">Get it, $19</a>' if STORES else ""

PAGE = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{TITLE} · Aurora Lab</title>
  <meta name="description" content="{html.escape(DESC)}">
  <meta property="og:title" content="{TITLE} · Aurora Lab">
  <meta property="og:description" content="{html.escape(DESC)}">
  <meta property="og:image" content="https://the-aurora-lab.github.io/assets/img/every-comment-answered.png">
  <meta property="og:url" content="https://the-aurora-lab.github.io/tools/every-comment-answered/">
  <link rel="canonical" href="https://the-aurora-lab.github.io/tools/every-comment-answered/">
  <meta name="theme-color" content="#0b1020">
  <link rel="icon" type="image/png" href="../../assets/img/avatar.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../assets/css/site.css">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="nav">
    <div class="wrap nav-inner">
      <a class="brand" href="../../" aria-label="Aurora Lab home">
        <img src="../../assets/img/avatar.png" alt="" width="32" height="32">
        <span>Aurora Lab</span>
      </a>
      <nav aria-label="Primary">
        <a href="../../#skills">Skills</a>
        <a href="../../#tools">Tools</a>
        <a class="btn btn-small" href="#get-it">Get it</a>
      </nav>
    </div>
  </header>

  <main id="main">
    <section class="docs-hero">
      <div class="aurora" aria-hidden="true"></div>
      <div class="wrap">
        <p class="crumbs"><a href="../../">Aurora Lab</a> / <a href="../../#tools">Tools</a> / Every Comment Answered</p>
        <h1>{TITLE}</h1>
        <p class="lede">For papers coming back from review: the decision letter split into numbered comments, every
        change in your LaTeX or Word manuscript with its page and line, each comment linked to the changes that answer
        it, and a check before you resubmit that every comment has a reply and every promised change is really in the
        paper. Your replies stay your own.</p>
        <ul class="meta" aria-label="Tool facts"><li>v{VERSION}</li><li>Python 3.9+, standard library only</li><li>Runs on your computer</li><li>Claude Code skill included</li><li>{PRICE}</li></ul>
        <div class="cta">{BUY_CTA}
          <a class="btn{' btn-ghost' if STORES else ''}" href="#a-revision">See a revision</a>
          <a class="btn btn-ghost" href="#how-well">How well it works</a>
        </div>
      </div>
    </section>

    <div class="wrap docs">
      <nav class="toc" aria-label="On this page">
        <p>On this page</p>
        <ol>{TOC}</ol>
      </nav>
      <article class="prose-doc">
{BODY}
      </article>
    </div>
  </main>

  <footer class="footer">
    <div class="wrap footer-inner">
      <span class="brand"><img src="../../assets/img/avatar.png" alt="" width="24" height="24"> Aurora Lab</span>
      <nav aria-label="Footer">
        <a href="https://www.agensi.io/creators/aurora-lab">Skills on Agensi</a>
        <a href="https://github.com/the-aurora-lab">GitHub</a>
        <a href="https://x.com/theauroralab">X</a>
      </nav>
    </div>
  </footer>
  {GOATCOUNTER}
</body>
</html>
"""

if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(PAGE, encoding="utf-8")
    print(f"wrote {OUT.relative_to(SITE)}")
