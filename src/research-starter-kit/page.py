"""Write tools/research-starter-kit/index.html, the docs page for the Research Starter Kit (pay what you want).

Run from the site root: ../.venv/bin/python src/research-starter-kit/page.py
The real project comes from the released zip on a simulated study (the kit's demo project): eight unattended Claude
Code sessions, then `kit.py ledger` and `kit.py disclose`; and two sessions in a copy without the rules. Their
outputs are in src/research-starter-kit/runs/ (copied verbatim), the whole statements in
tools/research-starter-kit/samples/. Evaluation numbers are copied from the kit's evals/guard/README.md (held-out set,
scored once). Store links live in STORES; rerun after any change.
"""
import html
import json
from pathlib import Path
import importlib.util as _ilu

_spec = _ilu.spec_from_file_location("seo", Path(__file__).resolve().parent.parent / "seo.py")
_seo = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_seo)
HERE = Path(__file__).resolve().parent
SITE = HERE.parent.parent
OUT = SITE / "tools" / "research-starter-kit" / "index.html"
RUNS = HERE / "runs"
VERSION = "1.0.0"
PRICE = "Pay what you want"
STORES = {    # published by the owner 2026-11-05 (step 17)
    "Gumroad": "https://theauroralab.gumroad.com/l/research-starter-kit",
    "Polar": "https://buy.polar.sh/polar_cl_9ie2DAXVNtoOvRcbShswIiOFe8fErbo0A4hCq0tStDs",
}
GOATCOUNTER = ('<script data-goatcounter="https://auroralabskills.goatcounter.com/count" async '
               'src="//gc.zgo.at/count.js"></script>')


def run(name):
    return html.escape((RUNS / name).read_text(encoding="utf-8").rstrip("\n"))


def table(head, rows, num_cols=()):
    th = "".join(f"<th>{h}</th>" for h in head)
    trs = "".join("<tr>" + "".join(f'<td class="num">{c}</td>' if i in num_cols else f"<td>{c}</td>"
                                   for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="doc-table"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


SESSIONS = json.loads((RUNS / "sessions.json").read_text(encoding="utf-8"))
SESSION_ROWS = "<ol>" + "".join(
    f'<li><strong>You asked:</strong> {html.escape(s["asked"])}<br><strong>The agent:</strong> {s["did"]}<br>'
    f'<strong>In the ledger:</strong> {s["ledger"]}</li>' for s in SESSIONS) + "</ol>"

if STORES:
    buy = " ".join(f'<a class="btn btn-small{"" if i == 0 else " btn-ghost"}" href="{u}">Get it on {s}</a>'
                   for i, (s, u) in enumerate(STORES.items()))
    get = ("<p><strong>Pay what you want, from $0 ($5 suggested).</strong> A zip with the kit, the four skills, the "
           "demo project, a quickstart and the full guide. MIT licence: the copy in your project can go wherever your "
           "project goes.</p>"
           f'<p class="bundle-buy">{buy}</p>')
else:
    get = ("<p><strong>Coming to Gumroad and Polar, pay what you want from $0 ($5 suggested)</strong>: a zip with the "
           "kit, the four skills, the demo project, a quickstart and the full guide. MIT licence.</p>")

GUARD_HELDOUT = table(["Held-out shell commands (168)", "Result", "95% CI"], [
    ["Raw-data changes stopped before the command ran", "<strong>63 / 84 (75%)</strong>", "65–83%"],
    ["… or noticed right after it ran, while git can still restore the files", "<strong>84 / 84</strong>", ""],
    ["Harmless commands let through without a false alarm", "72 / 84 (86%)", "77–92%"],
])

VENUES = table(["Venue", "Where the statement goes"], [
    ["Elsevier (and Cell Press)", "Its own section before the references, <em>Declaration of generative AI and "
     "AI-assisted technologies in the manuscript preparation process</em>, with Elsevier's wording; research uses in "
     "the Methods"],
    ["Springer Nature, Nature Portfolio", "The Methods (or a suitable alternative part); even language editing is "
     "described"],
    ["Wiley", "Acknowledgments for writing help, Methods for research uses, with version and dates"],
    ["Taylor &amp; Francis", "A <em>Declaration of AI use</em> statement: tool and version, how, why"],
    ["PLOS", "A part of the Methods, the Acknowledgements or the figure legend, with how outputs were checked"],
    ["IEEE", "The acknowledgments: system, sections, level of use"],
    ["ICMJE journals, JAMA Network", "Cover letter and acknowledgment; JAMA's fixed fields, prompts for research use"],
    ["ACL and ARR, NeurIPS, ICLR 2027, CVPR 2027", "Each conference's own rule: ARR's checklist item E1, NeurIPS only "
     "for method use, ICLR's mandatory section, CVPR's <em>LLM Usage Statement</em> before the references"],
    ["arXiv, NSF, UKRI, European Commission (Horizon Europe, ERC)", "Where each asks, with what counts as substantial "
     "use"],
    ["NIH, Science, ACM, MDPI, APA", "Their pages refused automated reading on 5 November 2026: marked \"check the "
     "policy yourself\". For NIH, the sections an agent wrote, against its originality rule"],
])

BODY = f"""
<section id="what-you-get">
<h2>What it does</h2>
<ul>
<li><strong>Rules your agent reads.</strong> <code>AGENTS.md</code> (for any agent) and <code>CLAUDE.md</code> (for
Claude Code) say what a research project expects: raw data stays as received, every number comes from code,
references come from records, the paper keeps building. To clean data, the agent writes a script and a new file in
<code>data/processed/</code>.</li>
<li><strong>Guards that hold when rules are not enough.</strong> Claude Code hooks refuse any change to raw data, by
any tool or shell command, and notice when a script changed it anyway. When a turn changed the paper, the paper is
built; new <code>.bib</code> entries are checked against Crossref, OpenAlex, DBLP and arXiv, and the agent is sent
back on an error, a new undefined citation, or a reference no registry lists. A git pre-commit check and a notebook
filter work whoever commits.</li>
<li><strong>A record of AI use.</strong> Every Claude Code session goes into <code>ai-use/ledger.jsonl</code> as it
happens: models and versions, what you asked, which files and which sections of the paper changed, the commands and
searches, what the guards refused and what the checks found. <code>kit.py disclose --venue &lt;venue&gt;</code> turns
it into a draft AI-use statement in the form that venue asks for.</li>
<li><strong>Four free skills.</strong> <a href="../../skills/bib-check/">bib-check</a>,
<a href="../../skills/paper-radar/">paper-radar</a>, <a href="../../skills/test-readers/">test-readers</a> and
<a href="../../skills/py-lib/">py-lib</a>.</li>
</ul>
<p>Everything is standard-library Python 3.9+, copied into your project, so the hooks need nothing installed and your
collaborators get them with the repository. Claude Code runs the hooks and writes the ledger; Codex, Cursor and
Gemini CLI get the rules, the git checks and <code>kit.py protect</code>, which makes raw files read-only for every
program.</p>
</section>

<section id="real-project">
<h2>A real project</h2>
<p>A small study made up for the demo (it comes with the kit): three soil-moisture sensors calibrated against
gravimetric samples, raw readings with four logger glitches, an analysis script, a notebook and a LaTeX paper with
three references. The kit {VERSION} was installed from the store zip. Then eight requests, each an unattended Claude
Code session (Claude Sonnet 5.5), as a researcher might make them while working on the paper:</p>
{SESSION_ROWS}
<p>What the ledger then held:</p>
<pre class="term"><span class="p">$ python3 .research-kit/kit.py ledger</span>
{run("ledger.txt")}</pre>
<h3>The statement it drafts</h3>
<p>For an Elsevier journal, the kit puts the writing uses in Elsevier's declaration, with Elsevier's own wording,
and the research uses in a paragraph for the Methods. Text in [brackets] is the authors' to write.</p>
<pre class="term"><span class="p">$ python3 .research-kit/kit.py disclose --venue elsevier</span>
{run("disclose-elsevier-excerpt.txt")}</pre>
<p>Each statement also says what need not be declared at that venue, what the policy asks for and what the ledger can
supply, the record file by file, and what the record cannot know. Open the whole statements as they came out:
<a href="samples/statement-elsevier.txt">Elsevier</a>, <a href="samples/statement-cvpr.txt">CVPR 2027</a>,
<a href="samples/statement-jama.txt">JAMA (with the prompts)</a>.</p>
<h3>When the rules are not enough</h3>
<p>With the kit's rules in place, the agent never tried to edit raw data or cite a paper it could not find. So the
same requests went to a copy of the project with the rules taken out, as if an agent had ignored them. The hooks
then did the work:</p>
<pre class="term">{run("hooks-only.txt")}</pre>
</section>

<section id="how-well">
<h2>How well it works</h2>
<h3>The raw-data guard, on commands it never saw</h3>
<p>An independent agent, which never saw the guard's code, wrote 168 shell commands of the kind an AI agent types in
a research project. They cover over 45 programs: <code>rm</code>, <code>sed -i</code>, redirects,
<code>find -delete</code>, <code>xargs</code>, archives, <code>git</code>, Python one-liners, heredocs and loops. It
labelled each by running it in a fresh copy of a project and checking whether raw files changed. The guard was then
scored once, after its rules were fixed on separate development commands.</p>
{GUARD_HELDOUT}
<ul>
<li>The 21 changes not stopped in advance are command shapes the guard does not model: archives extracted into the
current folder, <code>git reset --hard</code> to another branch, Python's <code>fileinput</code> in place,
<code>ed</code>, <code>node -e</code>. All 21 were caught by the second check, right after they ran.</li>
<li>The 12 false alarms are commands that are harmless only because of what is in the folder: deleting
<code>*.tmp</code> files where there are none, <code>cp -n</code>, <code>touch</code>.</li>
<li>A check that reads commands cannot know what a script does inside; that is what the after-the-command check and
<code>kit.py protect</code> are for.</li>
</ul>
<h3>The ledger, on real sessions</h3>
<p>{(RUNS / "ledger-completeness.txt").read_text(encoding="utf-8").strip()}</p>
<h3>The statements</h3>
<p>Each venue's profile comes from its own policy page, read on 5 November 2026: where the statement goes, its
heading, the fields it asks for, the wording it mandates or recommends, what is exempt. The page and the date are
printed with every statement, because policies change (Springer Nature and ICMJE rewrote theirs in 2026).</p>
</section>

<section id="statements">
<h2>AI-use statements, venue by venue</h2>
{VENUES}
<p>A statement says only what the ledger shows. It never writes paper text, and it leaves to you what only you know:
AI used outside Claude Code or outside the project, which of the agent's changes survived your editing, and how you
checked the work. <code>--since</code>, <code>--until</code> and <code>--path</code> narrow it to one paper or one
period; <code>ledger import</code> adds Claude Code sessions from before the kit was installed.</p>
</section>

<section id="get-it">
<h2>Get it and start</h2>
{get}
<pre><code>unzip research-starter-kit-{VERSION}.zip
python3 research-starter-kit/kit.py init ~/projects/my-paper     # --skeleton for a new project
# open the project in Claude Code and accept "trust this folder"
python3 .research-kit/kit.py doctor                               # everything in place?
python3 .research-kit/kit.py disclose --venue elsevier            # or --list</code></pre>
<p><code>init</code> never overwrites what you wrote: your <code>CLAUDE.md</code>, <code>AGENTS.md</code>,
<code>.gitignore</code> and <code>.gitattributes</code> get a marked block, your <code>.claude/settings.json</code>
keeps its other settings and hooks, and a pre-commit hook you already have is kept, unchanged, and runs first.
<code>init</code> also finds your raw-data folder (<code>data/raw</code>, <code>raw_data</code>, <code>raw</code> …) and says
what it protects. Collaborators run <code>kit.py doctor --fix</code> once after cloning. Needs Python 3.9+ and git; LaTeX only for the
build check.</p>
</section>

<section id="privacy">
<h2>What it sends where</h2>
<ul>
<li>The kit itself sends nothing anywhere and has no telemetry. The ledger stays in your project.</li>
<li>When new <code>.bib</code> entries are checked, bib-check sends their titles, authors, years and identifiers to
Crossref, doi.org, OpenAlex, DBLP's query service and arXiv. <code>[references] check = off</code> stops it.</li>
<li>paper-radar sends your topic to arXiv, OpenAlex and bioRxiv/medRxiv, only when you ask for it.</li>
<li>The ledger keeps your prompts word for word unless you set <code>prompts = none</code>, and it is committed with
the project unless you add <code>ai-use/</code> to <code>.gitignore</code>. Shell commands are recorded with keys,
tokens and passwords masked.</li>
<li>Claude Code sends your sessions to Anthropic as it always does; the kit adds nothing to that.</li>
</ul>
</section>

<section id="limits">
<h2>Limits</h2>
<ul>
<li>It is a seatbelt, not a sandbox. The shell check reads commands; a script that changes raw data is caught right
after it runs, from the files' size, time and permissions, and a tool that restores both an old size and an old time
would slip past. <code>kit.py protect</code> is the hard guard.</li>
<li>Only Claude Code writes the ledger. Other agents get the rules and the git checks.</li>
<li>The ledger records what the agent did, not what is in your final text.</li>
<li>Policies change. Five venues' pages could not be read automatically and are marked; check every statement against
the venue's current page before you submit.</li>
<li>Tested on macOS with Python 3.9 and 3.14, git 2.54, TeX Live 2026 and Claude Code 2.1.318. Windows is
untested.</li>
</ul>
</section>
"""

SECTIONS = [("what-you-get", "What it does"), ("real-project", "A real project"), ("how-well", "How well it works"),
            ("statements", "AI-use statements"), ("get-it", "Get it and start"), ("privacy", "What it sends where"),
            ("limits", "Limits")]
TOC = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in SECTIONS)
TITLE = "Research Starter Kit: Your Data Protected, Your AI Use on Record"
DESC = ("Rules your AI agent reads, guards that keep raw data, the paper and the references safe, and a record of "
        "every Claude Code session that becomes the AI-use statement your journal asks for. Held-out evaluation "
        "published.")
BUY_CTA = '\n          <a class="btn" href="#get-it">Get it, pay what you want</a>' if STORES else ""

LD = _seo.software_ld("research-starter-kit", TITLE, DESC)

PAGE = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{TITLE} · Aurora Lab</title>
  <meta name="description" content="{html.escape(DESC)}">
  <meta property="og:title" content="{TITLE} · Aurora Lab">
  <meta property="og:description" content="{html.escape(DESC)}">
  <meta property="og:image" content="https://the-aurora-lab.github.io/assets/img/research-starter-kit.png">
  <meta property="og:url" content="https://the-aurora-lab.github.io/tools/research-starter-kit/">
  <link rel="canonical" href="https://the-aurora-lab.github.io/tools/research-starter-kit/">
  {LD}
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
        <a class="btn btn-small" href="#get-it">Get the kit</a>
      </nav>
    </div>
  </header>

  <main id="main">
    <section class="docs-hero">
      <div class="aurora" aria-hidden="true"></div>
      <div class="wrap">
        <p class="crumbs"><a href="../../">Aurora Lab</a> / <a href="../../#tools">Tools</a> / Research Starter Kit</p>
        <h1>{TITLE}</h1>
        <p class="lede">For research projects where an AI agent works beside you: rules it reads, guards that keep your
        raw data as received and your paper and references sound when it does not follow them, and a record of every
        session that becomes the AI-use statement your journal, conference or funder asks for.</p>
        <ul class="meta" aria-label="Tool facts"><li>v{VERSION}</li><li>Python 3.9+, standard library only</li><li>Claude Code hooks; git checks for any agent</li><li>{PRICE}</li></ul>
        <div class="cta">{BUY_CTA}
          <a class="btn{' btn-ghost' if STORES else ''}" href="#real-project">See a real project</a>
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
