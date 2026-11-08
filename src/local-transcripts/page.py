"""Write tools/local-transcripts/index.html, the docs page for Local Transcripts ($29 personal, $99 lab).

Run from the site root: ../.venv/bin/python src/local-transcripts/page.py
The runs shown are real: an openly licensed mock consultation (PriMock57, CC BY 4.0) through `local-transcripts
interview`, and an openly licensed talk (35C3 "Quantum Mechanics", CC BY 4.0) through `local-transcripts lecture`
plus one unattended Claude Code session writing the notes. collect_runs.py copies their outputs verbatim into
src/local-transcripts/runs/, tools/local-transcripts/samples/ and assets/shots/local-transcripts/. Evaluation numbers
come from the tool's held-out results (scored once). Store links live in STORES; rerun after any change.
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
OUT = SITE / "tools" / "local-transcripts" / "index.html"
RUNS = HERE / "runs"
VERSION = "1.0.3"
PRICE = "$29 once · lab $99"
STORES = {    # published by the owner 2026-11-06 (step 19)
    "Gumroad": "https://theauroralab.gumroad.com/l/local-transcripts",
    "Polar": "https://buy.polar.sh/polar_cl_RVhDknqZx3cFxYTuzCnuFCxxkXrRFyZpKMX6M1dRMmD",
}
GOATCOUNTER = ('<script data-goatcounter="https://auroralabskills.goatcounter.com/count" async '
               'src="//gc.zgo.at/count.js"></script>')
HELDOUT = json.loads((RUNS / "heldout.json").read_text(encoding="utf-8")) if (RUNS / "heldout.json").exists() else {}


def run(name):
    return html.escape((RUNS / name).read_text(encoding="utf-8").rstrip("\n"))


def table(head, rows, num_cols=()):
    th = "".join(f"<th>{h}</th>" for h in head)
    trs = "".join("<tr>" + "".join(f'<td class="num">{c}</td>' if i in num_cols else f"<td>{c}</td>"
                                   for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="doc-table"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def heldout() -> str:
    if not HELDOUT:
        return "<p>Held-out results are added before release.</p>"
    h = HELDOUT
    return f"""<p>{h["intro"]}</p>
{table(h["interview_head"], h["interview_rows"])}
{h.get("interview_after", "")}
{table(h["lecture_head"], h["lecture_rows"])}
{h.get("lecture_after", "")}"""


if STORES:
    buy = " ".join(f'<a class="btn btn-small{"" if i == 0 else " btn-ghost"}" href="{u}">Get it on {s}</a>'
                   for i, (s, u) in enumerate(STORES.items()))
    get = ("<p><strong>$29 once for one person, $99 for a lab of up to five.</strong> A zip with the Python wheel (the "
           "<code>local-transcripts</code> command and the Claude Code skill), a quickstart and the full guide. Updates "
           "for 12 months. No licence key, so nothing ever checks in with a server.</p>"
           f'<p class="bundle-buy">{buy}</p>')
else:
    get = ("<p><strong>Coming to Gumroad and Polar: $29 once for one person, $99 for a lab of up to five.</strong> A zip "
           "with the Python wheel (the <code>local-transcripts</code> command and the Claude Code skill), a quickstart and "
           "the full guide. Updates for 12 months. No licence key.</p>")

def run_block(kind: str) -> str:
    p = RUNS / f"{kind}.html"
    return p.read_text(encoding="utf-8") if p.exists() else "<p>Run shown before release.</p>"


EXPORTS = table(["Software", "File", "How"], [
    ["MAXQDA", "<code>p07.txt</code> or <code>.docx</code>", "Import › Transcripts › Transcript with Timestamps, then the recording"],
    ["MAXQDA, speakers as codes", "<code>p07.maxqda.txt</code>", "Import › Focus Group Transcripts (f4 timestamps <code>#hh:mm:ss-x#</code>)"],
    ["NVivo, Windows", "<code>p07.nvivo.tsv</code>", "Open the audio, edit mode, Import Rows: tab-delimited, header row; map Timespan, Speaker, Content"],
    ["NVivo, Mac", "<code>p07.maxqda.txt</code>", "Import › Files › Transcript Rows"],
    ["ATLAS.ti", "<code>p07.docx</code> or <code>.vtt</code>", "Import Transcript with the recording; the .vtt codes each speaker"],
    ["QualCoder", "<code>p07.txt</code>", "Paste into the recording's transcript; <code>[hh:mm:ss]</code> and <code>Name:</code> are recognised"],
    ["Anything else", "<code>.srt</code>, <code>.vtt</code>, <code>.csv</code>", "Subtitles, spreadsheets, R, Python"],
])

BODY = f"""
<section id="what-it-does">
<h2>What it does</h2>
<h3>Interviews and focus groups</h3>
<ul>
<li><strong>Transcribes on your computer</strong> with Whisper large-v3-turbo: on the GPU of an Apple Silicon Mac
(about 2 minutes for an hour of audio on an M3 Max) or on any CPU.</li>
<li><strong>Finds who spoke when</strong> with pyannote's segmentation model and WeSpeaker voice prints, then gives
every word its speaker. Give the number of speakers, or let it estimate them; name them (Interviewer, Participant 7)
and merge or fix them afterwards.</li>
<li><strong>Makes a pseudonymised copy</strong>: people, places, organisations, full dates, emails and phone numbers
become <code>[Person 1]</code>, <code>[Place 2]</code>…, the same tag for the same person across every interview of
the project. Your own list of names is matched even when Whisper misspells them. The key and the log stay apart from
the shareable files; a list of suspects shows what to check by eye; <code>forget-key</code> deletes the link when
the study no longer needs it.</li>
<li><strong>Writes the files your software imports</strong>, timestamped and with speakers, and a review page where
any time plays that moment of the recording and unsure words are underlined.</li>
</ul>
<h3>Lectures and seminars</h3>
<ul>
<li><strong>Lays the transcript out under a still of each slide</strong>, in the order shown. Camera cuts make no
still, builds are followed to the fullest version, a slide shown twice keeps one still, and the slide is cropped out
of a speaker-beside-slides layout.</li>
<li><strong>Study notes, when you want them</strong>: your coding agent (Claude Code with the included skill) reads
the stills and the transcript and writes notes with every equation in LaTeX; <code>notes check</code> confirms every
slide is covered and every equation compiles, and <code>notes tex --pdf</code> makes a document.</li>
</ul>
</section>

<section id="privacy">
<h2>What stays on your computer</h2>
<p><code>local-transcripts setup</code> downloads the models once, each from its publisher with a pinned checksum or
revision: Whisper from huggingface.co, the speaker models and the name finder from github.com. After that <strong>no
command uses the network</strong>: no account, no licence key, no telemetry. We ran an interview and a lecture with
the network blocked by the operating system (macOS <code>sandbox-exec</code>, deny network): both finished.</p>
<p>The one step that sends anything anywhere is optional and yours: <strong>lecture notes</strong> are written by your
own coding agent, which reads the lecture's transcript and stills and so sends them to the AI service it runs on.
Interview transcripts are never part of that; the included skill tells the agent not to open interview files and not
to ask you for names.</p>
<p>To see the free route first, our guide <a href="../../guides/transcribe-interviews-offline/">Transcribe
research interviews without uploading them</a> runs Whisper by hand, offline, and shows what it leaves to you.</p>
</section>

<section id="an-interview">
<h2>An interview, start to finish</h2>
{run_block("interview")}
</section>

<section id="a-lecture">
<h2>A lecture, start to finish</h2>
{run_block("lecture")}
</section>

<section id="software">
<h2>Into your analysis software</h2>
{EXPORTS}
<p>The formats follow each vendor's manual (2026); put the recording beside the transcript with the same base name
and the software finds it. We did not import into every program ourselves.</p>
</section>

<section id="how-well">
<h2>How well it works</h2>
{heldout()}
</section>

<section id="get-it">
<h2>Get it and start</h2>
{get}
<pre><code>pip install "local_transcripts-{VERSION}-py3-none-any.whl[mac]"   # Apple Silicon; without [mac] elsewhere
local-transcripts setup                                  # once: the models, about 2 GB
local-transcripts interview recordings/ --speakers 2 --roles "Interviewer,Participant" --names names.txt
local-transcripts lecture lecture-07.mp4
local-transcripts setup skill                            # then ask Claude Code to "transcribe the interviews in recordings/"</code></pre>
<p>Python 3.10–3.13 and ffmpeg. macOS, Windows and Linux. Works without Claude Code.</p>
</section>

<section id="limits">
<h2>Limits</h2>
<ul>
<li>Transcripts are drafts: names, numbers and technical terms need a human check, which the review page is made for.
Overlapping speech goes to one speaker.</li>
<li>Speaker labels are best with the number of speakers given; similar voices, phone lines and meetings of many people
give more mistakes.</li>
<li>Pseudonymisation is a strong first pass, not a guarantee: read the shareable copy before sharing. Indirect
identifiers (a job title, a rare event) are not detected, and a name Whisper misheard badly may be missed.</li>
<li>Slide stills need slides on screen; a filmed whiteboard gives none, and a scrolled document gives one still per
scroll stop.</li>
<li>Name finders for English, German, Spanish and French; other languages use a multilingual one.</li>
<li>Works on files you have; it does not download from YouTube or the web.</li>
<li>Tested on macOS (Apple Silicon) with Python 3.10–3.14 and ffmpeg 8; Windows and Linux are untested.</li>
</ul>
</section>
"""


SECTIONS = [("what-it-does", "What it does"), ("privacy", "What stays on your computer"),
            ("an-interview", "An interview"), ("a-lecture", "A lecture"), ("software", "Into your software"),
            ("how-well", "How well it works"), ("get-it", "Get it and start"), ("limits", "Limits")]
TOC = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in SECTIONS)
TITLE = "Local Transcripts: Interviews Ready to Code, Lectures to Study"
DESC = ("Transcribe interviews and lectures on your own computer: who said what with timestamps, a pseudonymised copy "
        "for MAXQDA, NVivo, ATLAS.ti or QualCoder, and lectures laid out under their slides, with study notes and LaTeX "
        "equations when you ask your coding agent. Held-out evaluation published.")
BUY_CTA = '\n          <a class="btn" href="#get-it">Get it, from $29</a>' if STORES else ""

LD = _seo.software_ld("local-transcripts", TITLE, DESC)

PAGE = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{TITLE} · Aurora Lab</title>
  <meta name="description" content="{html.escape(DESC)}">
  <meta property="og:title" content="{TITLE} · Aurora Lab">
  <meta property="og:description" content="{html.escape(DESC)}">
  <meta property="og:image" content="https://the-aurora-lab.github.io/assets/img/local-transcripts.png">
  <meta property="og:url" content="https://the-aurora-lab.github.io/tools/local-transcripts/">
  <link rel="canonical" href="https://the-aurora-lab.github.io/tools/local-transcripts/">
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
        <a class="btn btn-small" href="#get-it">Get it</a>
      </nav>
    </div>
  </header>

  <main id="main">
    <section class="docs-hero">
      <div class="aurora" aria-hidden="true"></div>
      <div class="wrap">
        <p class="crumbs"><a href="../../">Aurora Lab</a> / <a href="../../#tools">Tools</a> / Local Transcripts</p>
        <h1>{TITLE}</h1>
        <p class="lede">Your recordings, transcribed on your own computer. Interviews become who-said-what transcripts
        with timestamps, a pseudonymised copy and files your analysis software imports. Lectures become the transcript
        under each slide, and study notes with the equations in LaTeX when you ask your coding agent. Nothing leaves
        your computer after a one-time model download.</p>
        <ul class="meta" aria-label="Tool facts"><li>v{VERSION}</li><li>Runs on your computer</li><li>MAXQDA · NVivo · ATLAS.ti · QualCoder</li><li>Claude Code skill included</li><li>{PRICE}</li></ul>
        <div class="cta">{BUY_CTA}
          <a class="btn{' btn-ghost' if STORES else ''}" href="#an-interview">See an interview</a>
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
