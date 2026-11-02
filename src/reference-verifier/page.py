"""Write tools/reference-verifier/index.html, the docs page for Reference Verifier (free core + Pro).

Run from the site root: ../.venv/bin/python src/reference-verifier/page.py
The terminal transcripts come from runs/ (real runs of the released builds on tools/reference-verifier/demo/, copied
verbatim); the screenshots in assets/shots/reference-verifier/ and the sample reports in tools/reference-verifier/samples/
are outputs of the same runs. Benchmark numbers are copied from the two READMEs ("How well it works"): held-out sets only.
Store links live in STORES; rerun after any change.
"""
import html
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parent.parent
OUT = SITE / "tools" / "reference-verifier" / "index.html"
REPO = "https://github.com/the-aurora-lab/reference-verifier"
VERSION = "0.2.1"
STORES = {  # the store products (step 11, 2026-11-02): Gumroad's page has the three versions, Polar's link the three products
    "Gumroad": "https://theauroralab.gumroad.com/l/reference-verifier-pro",
    "Polar": "https://buy.polar.sh/polar_cl_MTAwd6EOC2wKKewaLmLvxkOETpuChf4Y0oVPD47vr1s",
}
TIERS = [("Personal", "one person, for their own work", "3", "$24"),
         ("Course", "one instructor, for checking their students' work", "3", "$99"),
         ("Lab", "one research group", "10", "$149")]
GOATCOUNTER = ('<script data-goatcounter="https://auroralabskills.goatcounter.com/count" async '
               'src="//gc.zgo.at/count.js"></script>')


def run(name: str) -> str:
    return html.escape((HERE / "runs" / name).read_text(encoding="utf-8").rstrip("\n"))


def table(head: list[str], rows: list[list[str]], num_cols=()) -> str:
    th = "".join(f"<th>{h}</th>" for h in head)
    trs = "".join("<tr>" + "".join(f'<td class="num">{c}</td>' if i in num_cols else f"<td>{c}</td>"
                                   for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="doc-table"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def shot(file: str, alt: str, caption: str, href: str) -> str:
    """A crop of a real report, linked to the whole report (readable on a phone, where the crop is small)."""
    return (f'<figure><a href="{href}"><img src="../../assets/shots/reference-verifier/{file}" alt="{html.escape(alt)}" '
            f'loading="lazy"></a><figcaption>{caption}</figcaption></figure>')


if STORES:
    buy = " ".join(f'<a class="btn btn-small{"" if i == 0 else " btn-ghost"}" href="{u}">Buy on {s}</a>'
                   for i, (s, u) in enumerate(STORES.items()))
    pro_get = (table(["Licence", "For", "Computers", "Price"], [[f"<strong>{t}</strong>", w, c, p] for t, w, c, p in TIERS])
               + "<p>Every licence includes all of Pro, a licence key, and 12 months of updates. You get a zip with the "
               "Python wheel, a quickstart, the full guide and the licence terms. Pick the licence at checkout:</p>"
               f'<p class="bundle-buy">{buy}</p>')
else:
    pro_get = ("<p><strong>Pro goes on sale soon on Gumroad and Polar</strong>: one Python wheel and a licence key. Until "
               "then, the free core is the way to try it.</p>")

CHECKS = table(["Check", "Free core", "Pro"], [
    ["References no registry lists (invented papers, garbled titles)", "Yes", "Yes"],
    ["DOIs that are not registered, or belong to another paper", "Yes", "Yes, with the likely correct DOI"],
    ["Retracted, withdrawn and corrected papers, expressions of concern", "—", "Yes: Crossref's notices and the Retraction Watch database"],
    ["Authors, year, venue, pages, volume and issue against the publisher's record", "—", "Yes"],
    ["The same work under two keys; cite keys that are missing, mistyped or unused", "—", "Yes"],
    ["Preprints that have since been published", "—", "Yes, with the DOI and venue to cite"],
    ["A corrected copy of your <code>.bib</code> and a diff to review (<code>--fix</code>)", "—", "Yes"],
    ["A dated HTML audit report to keep or share", "—", "Yes"],
    ["A class's papers (<code>.docx</code>, <code>.odt</code>, PDF, text, Markdown) in any citation style", "—", "Yes"],
    ["Source support: the passages of each open-access cited work that best match your sentence", "—", "Yes"],
    ["Pre-commit hook, GitHub Actions annotations, a SKILL.md and read-only MCP tools for your agent", "—", "Yes"],
    ["Licence", "MIT, free", "Licence key, from $24" if STORES else "Paid licence key"],
])

FREE_HELDOUT = table(["Measure", "Result", "95% CI"], [
    ["Real references found", "94 of 95", "94.3–99.8%"],
    ["Fabricated references flagged", "54 of 54", "93.4–100%"],
    ["Wrong DOIs flagged as a DOI problem", "30 of 30", "88.6–100%"],
    ["Retracted papers found (they exist; flagging the retraction is Pro's job)", "35 of 35", "90.1–100%"],
    ["Precision: flags that were on a fabricated or wrong-DOI entry", "84 of 85", "93.6–99.8%"],
])

PRO_HELDOUT = table(["Check", "Result", "95% CI"], [
    ["Wrong pages, volumes and issues reported with the publisher's value", "40 of 40", "91–100%"],
    ["Wrong year or first author reported", "16 of 16", "81–100%"],
    ["Wrong venue reported", "6 of 8", "41–93%"],
    ["Wrong title words reported", "7 of 8", "53–98%"],
    ["Wrong DOI: the likely correct DOI offered", "28 of 30", "79–98%"],
    ["Preprints linked to their published version", "13 of 14", "69–99%"],
    ["Retractions, expressions of concern, corrections and notice DOIs exactly right", "34 of 34", "90–100%"],
    ["Retracted papers cited with their DOI: retraction reported", "35 of 35", "90–100%"],
    ["Clean look-alikes of retracted papers left alone", "5 of 6", "44–97%"],
    ["Duplicates and look-alikes told apart", "10 of 10", "72–100%"],
    ["Cite-key cases (missing, mistyped, case-mismatched, unused)", "6 of 6", "61–100%"],
    ["Genuine entries given a medium-or-worse finding (false alarms)", "1 of 130", "0–4%"],
    ["Fabricated entries given field findings", "0 of 54", "0–7%"],
])

BATCH_HELDOUT = table(["Reference strings", "Result", "95% CI"], [
    ["Real references found", "59 of 60", "91–99.7%"],
    ["Real references given a high result", "0 of 60", "0–6%"],
    ["Fabricated references flagged (19 high, 5 medium)", "24 of 25", "80–99%"],
    ["Wrong DOIs reported as the DOI of another work", "10 of 10", "72–100%"],
    ["Retracted papers found and reported retracted", "10 of 10", "72–100%"],
    ["A real title with invented authors reported as \"other authors\"", "7 of 8", "53–98%"],
])

BODY = f"""
<section id="what-it-checks">
<h2>What it checks</h2>
<p>Reference Verifier reads your <code>.bib</code> file, or your LaTeX paper and the bibliography it uses, and looks every
cited entry up in Crossref, OpenAlex, DBLP, arXiv and PubMed. The free core answers one question: does each reference
exist as written? Pro checks each one against the publisher's record and the retraction databases, and fixes what the
record settles.</p>
{CHECKS}
</section>

<section id="real-run">
<h2>A real run</h2>
<p>A ten-entry demo paper with eight planted problems: a DOI with a typo, ResNet cited with the DOI of the paper next to
it (YOLO), an invented paper, Wakefield's 1998 <em>Lancet</em> paper (retracted in 2010), one paper under two keys, a
wrong volume, a 2018 arXiv preprint that has since been published, and a cite key typed in the wrong case. Download it
and run it yourself: <a href="demo/paper.tex">paper.tex</a>, <a href="demo/refs.bib">refs.bib</a>.</p>
<p>Both runs below used the released {VERSION} builds and an empty cache, on 1 November 2026. DBLP's search was
turning automated requests away that day; the tool says so and carries on with the other registries.</p>

<h3>Free core: 4 seconds</h3>
<pre class="term"><span class="p">$ refverify paper.tex</span>
{run("free.txt")}</pre>
<p>Three of the eight problems are about existence, and the free core flags all three. The other five are not: Wakefield
1998 exists (it was retracted), and so do the duplicated paper, the paper with the wrong volume, the preprint and the
entry behind the mistyped key.</p>

<h3>Pro: 10 seconds, all eight</h3>
<div class="shots">
{shot("01-audit-findings.png", "The audit report's summary and its Needs attention list: the mistyped key, the two wrong DOIs with their likely correct DOIs, the invented paper, the retraction with its date, notice and reasons, the duplicate and the wrong volume.", "The top of the audit report from <code>--html</code>: every high and medium problem, the record it was compared with, and the value to use.", "samples/audit.html")}
{shot("02-audit-fixes.png", "The Fixes section of the audit report: a diff that corrects the two DOIs, turns the BERT preprint into the published NAACL 2019 entry and sets the volume to 529.", "<code>--fix --fix-published</code> wrote <code>refs.fixed.bib</code> and this diff (<a href=\"demo/refs.fix.diff\">refs.fix.diff</a>); <code>refs.bib</code> itself was not touched. The retraction, the duplicate and the key are left to you.", "samples/audit.html")}
</div>
<p><a href="samples/audit.html">Open the whole audit report</a> (every reference, the sources consulted and the input
files with their SHA-256).</p>
<details>
<summary>The terminal output</summary>
<pre class="term"><span class="p">$ refverify-pro paper.tex --fix --fix-published --html audit.html --json pro.json</span>
{run("pro.err.txt")}
{run("pro.txt")}</pre>
</details>

<h3>A class's papers</h3>
<p><code>refverify-batch</code> takes a folder, or the <code>.zip</code> your learning platform downloads, finds each
paper's reference list and looks up every reference as written, whatever the citation style.</p>
<div class="shots">
{shot("03-class-summary.png", "The class summary: 12 papers, 2 that could not be read (a scan and an old .doc), 109 references checked, 76 found, and per paper the number of high, medium and low results.", "The summary page for a class of 12 papers. Unreadable files are listed with the reason.", "samples/class/index.html")}
{shot("04-paper-report.png", "One paper's report: a retracted paper with its notice and reasons, a DOI that belongs to another work with the likely correct DOI, and two conference papers no registry lists.", "One paper's report: each problem reference as written, and what the registries say about it.",
     "samples/class/papers/Student-02_1002_assignsubmission_file___essay-final.docx.html")}
</div>
<p><a href="samples/class/index.html">Open the class summary</a>. This class is synthetic: twelve papers we made in
<code>.docx</code>, <code>.odt</code>, PDF, text and Markdown, plus a scan and an old <code>.doc</code>, zipped the way
Moodle downloads submissions. Their references come from our development data, in six citation styles: real ones,
invented ones taken from public compilations of hallucinated citations, wrong DOIs and retracted papers. It shows what
you get, not how accurate the tool is; the next section does that.</p>
</section>

<section id="how-well">
<h2>How well it works</h2>
<p>Every number here comes from a held-out set: references collected and labelled by an independent agent that never
ran the tool, with no overlap with the data the rules were tuned on, scored once with no changes afterwards. Intervals
are 95% Wilson intervals. Measured with 0.2.0; {VERSION} changes only how output is shown.</p>

<h3>Free core: does each reference exist?</h3>
{FREE_HELDOUT}
<ul>
<li>246 references. The real ones were drawn across computer science, biomedicine, physics, mathematics, the social
sciences and the humanities, written the messy ways real <code>.bib</code> files are.</li>
<li>The one real reference it missed is a DOI-less ICLR 2022 paper that only DBLP indexes; DBLP's search turned the tool
away during the run.</li>
<li>The fabricated references come from public compilations of hallucinated citations found in ACL-family papers and
ICLR 2026 submissions, so all 54 are computer science. "Fabricated" means listed there and found neither in any registry
nor by a web search for the exact title.</li>
<li>Sources, licences and labelling rules: <a href="{REPO}/blob/main/benchmark/heldout-0.2/HELDOUT.md">HELDOUT.md</a>;
rerun it with the command in the <a href="{REPO}#how-well-it-works">README</a>.</li>
</ul>

<h3>Pro: field checks, notices, duplicates, keys</h3>
{PRO_HELDOUT}
<p><code>--fix</code> on the same items restored 40 of 40 pages, volumes and issues, 28 of 30 DOIs and 12 of 14
published versions, and changed 1 of 130 genuine entries it should have left alone.</p>

<h3>Pro: a class's reference lists</h3>
{BATCH_HELDOUT}
<ul>
<li>120 reference strings: 60 real ones copied from open-access articles' reference lists (Vancouver, APA, Harvard,
Chicago, IEEE, Nature and ACS styles) and constructed ones checked absent from every registry.</li>
<li>Misses: a real reference with a typo in its author's name (reported as other authors), an invented title matched to
a real paper with a longer title, and a web page written like an article, which got a high "not found".</li>
<li>Small sets: one item moves a rate by several points; the intervals say how much.</li>
</ul>
</section>

<section id="install">
<h2>Install and use</h2>
<h3>Free core</h3>
<pre><code>pip install git+{REPO}@v{VERSION}

refverify refs.bib                  # every entry in a .bib
refverify main.tex                  # only the keys main.tex cites
refverify main.tex --json out.json  # machine-readable results too</code></pre>
<p>Python 3.10 or newer. The exit status is 1 when a journal or conference reference is missing or has a bad DOI, so
it can gate a script or a CI job. Set <code>REFVERIFY_MAILTO</code> to your email for Crossref's and PubMed's polite
pools, and <code>OPENALEX_API_KEY</code> (free at openalex.org) for your own OpenAlex budget. Source and issues:
<a href="{REPO}">GitHub</a>.</p>
<h3 id="pro">Pro</h3>
{pro_get}
<pre><code>pip install reference_verifier_pro-{VERSION}-py3-none-any.whl   # also installs the free core
refverify-setup licence activate &lt;KEY&gt;

refverify-pro paper.tex                      # every check, cited entries only
refverify-pro paper.tex --fix --html audit.html
refverify-batch "Essay 2 - Download all submissions.zip"
refverify-support paper.tex                  # source support: an evidence pack</code></pre>
<p>The key is checked with the store that sold it, then once a week; offline, Pro keeps working for 30 days from the
last check. Only the key, the store's product id and a random install id are sent.</p>
</section>

<section id="workflow">
<h2>In your workflow</h2>
<ul>
<li><strong>Before each commit.</strong> <code>refverify-setup hook</code> installs a git pre-commit hook that checks only
the <code>.bib</code> entries a commit adds or changes, in seconds, and stops the commit on a wrong DOI, a reference no
registry lists, a retracted paper or an undefined key. Offline, it says so and lets the commit through.</li>
<li><strong>On every pull request.</strong> <code>refverify-setup ci</code> writes a GitHub Actions workflow: problems
appear as annotations on the changed lines, the job summary lists them, and the audit report is kept with the run.</li>
<li><strong>In your AI agent.</strong> <code>refverify-setup skill</code> installs a SKILL.md that tells your agent when
to check and how to report ("no registry lists it", never "fake"; fixes as copies you review), and
<code>refverify-mcp</code> gives it five read-only tools: the reference checks and source support.</li>
</ul>
</section>

<section id="privacy">
<h2>What it sends where</h2>
<ul>
<li>Titles, author names, years and identifiers from your bibliography go to the public registries: Crossref, doi.org,
OpenAlex, DBLP, arXiv and PubMed. Your <code>.tex</code> files and your papers' text never leave your machine.</li>
<li>Pro downloads the Retraction Watch database from Crossref's public repository at most once a day; retraction lookups
are local. Batch mode sends each reference string, never the paper around it.</li>
<li>Answers are cached for 30 days on your machine, and every registry gets polite request rates (arXiv: one request
every three seconds, as it asks).</li>
<li>Reports name files relative to your working folder and are dated in UTC, so you can share them.</li>
</ul>
</section>

<section id="limits">
<h2>Limits</h2>
<ul>
<li>"Not found" means no registry lists it, not that it was invented: books, theses, reports, regional journals and
very new papers are often missing. Check before you change anything.</li>
<li>Registries make mistakes too; every finding names the record it was compared with.</li>
<li>Many computer science venues publish without DOIs. When DBLP turns automated requests away, those papers can go
unconfirmed for the run; the report says so.</li>
<li>Batch mode reads PDFs with a text layer (no OCR) and common reference-list layouts; each report shows the list as
read, so a misread is visible. Web pages are not checked unless you ask for <code>--check-links</code>.</li>
<li>Source support works only with open-access full texts, and ranks passages by shared words: it finds evidence for
you or your agent to judge; it does not judge claims itself.</li>
</ul>
</section>
"""

PRO_CTA = '\n          <a class="btn btn-ghost" href="#pro">Get Pro</a>' if STORES else ""
SECTIONS = [("what-it-checks", "What it checks"), ("real-run", "A real run"), ("how-well", "How well it works"),
            ("install", "Install and use"), ("workflow", "In your workflow"), ("privacy", "What it sends where"),
            ("limits", "Limits")]
TOC = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in SECTIONS)
TITLE = "Reference Verifier: Every Reference Checked"
DESC = ("Check every reference in your paper before a reviewer does: invented papers, wrong DOIs, retracted work and "
        "field errors against Crossref, OpenAlex, DBLP, arXiv and PubMed. Free core on GitHub, held-out benchmark published.")

PAGE = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{TITLE} · Aurora Lab</title>
  <meta name="description" content="{html.escape(DESC)}">
  <meta property="og:title" content="{TITLE} · Aurora Lab">
  <meta property="og:description" content="{html.escape(DESC)}">
  <meta property="og:image" content="https://the-aurora-lab.github.io/assets/img/reference-verifier.png">
  <meta property="og:url" content="https://the-aurora-lab.github.io/tools/reference-verifier/">
  <link rel="canonical" href="https://the-aurora-lab.github.io/tools/reference-verifier/">
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
        <a class="btn btn-small" href="{REPO}">Free on GitHub</a>
      </nav>
    </div>
  </header>

  <main id="main">
    <section class="docs-hero">
      <div class="aurora" aria-hidden="true"></div>
      <div class="wrap">
        <p class="crumbs"><a href="../../">Aurora Lab</a> / <a href="../../#tools">Tools</a> / Reference Verifier</p>
        <h1>{TITLE}</h1>
        <p class="lede">Check every reference in your paper before a reviewer does. The free core finds references no
        registry lists and DOIs that point nowhere or to another paper. Pro adds retractions, field-by-field checks
        against the publisher's record, fixes you review, audit reports and a mode for a whole class's papers.</p>
        <ul class="meta" aria-label="Tool facts"><li>v{VERSION}</li><li>Python 3.10+</li><li>Runs on your machine</li><li>Free core: MIT</li></ul>
        <div class="cta">
          <a class="btn" href="#install">Install the free core</a>
          <a class="btn btn-ghost" href="#real-run">See a real run</a>{PRO_CTA}
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
        <a href="{REPO}">Reference Verifier on GitHub</a>
        <a href="https://www.agensi.io/creators/aurora-lab">Skills on Agensi</a>
        <a href="https://x.com/theauroralab">X</a>
      </nav>
    </div>
  </footer>
  {GOATCOUNTER}
</body>
</html>
"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(PAGE, encoding="utf-8")
print(f"wrote {OUT.relative_to(SITE)}")
