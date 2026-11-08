"""Write guides/transcribe-interviews-offline/index.html: transcribing research interviews on your own computer.

Run from the site root: ../.venv/bin/python src/guides/transcribe-interviews-offline/page.py
Every command and output in runs/ was run on 2026-11-08 and is copied verbatim (the recording is PriMock57's mock
consultation day1_consultation01, CC BY 4.0, the same one the Local Transcripts page uses). Facts about other tools and
QDA formats come from the vendors' pages, read 2026-11-06 (Intelligence notes for step 19); gating of pyannote's
models was read from Hugging Face's API on 2026-11-08.
"""
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parent.parent.parent
OUT = SITE / "guides" / "transcribe-interviews-offline" / "index.html"
RUNS = HERE / "runs"
URL = "https://the-aurora-lab.github.io/guides/transcribe-interviews-offline/"
CHECKED = "8 November 2026"
GOATCOUNTER = ('<script data-goatcounter="https://auroralabskills.goatcounter.com/count" async '
               'src="//gc.zgo.at/count.js"></script>')


def run(name):
    return html.escape((RUNS / name).read_text(encoding="utf-8").rstrip("\n"))


TITLE = "Transcribe Research Interviews Without Uploading Them"
DESC = ("A free way to transcribe interviews on your own computer with Whisper, run for real: the commands, the "
        "install error you will hit today and its fix, working offline, and what it leaves to you: speakers, names "
        "and your analysis software.")

SECTIONS = [
    ("why", "Why keep recordings on your computer", f"""
<p>Consent forms and ethics approvals usually say where interview recordings are kept and who may process them. A
cloud transcription service is one more party that receives the audio and processes it on its own servers. Before you
upload anything, check what your approval and your data management plan allow.</p>
<p>You may not need to upload at all. Whisper, the open speech-recognition model, runs on an ordinary laptop. After a
one-time model download it needs no internet connection. The rest of this page shows the free route step by step,
exactly as it ran on {CHECKED}.</p>
"""),
    ("free-route", "The free route, step by step", f"""
<p>You need Python 3.10 or newer and about 2 GB of disk space for the model. Make a folder, put your recording in it as
<code>interview.wav</code> (MP3, M4A and most other formats work too), and save this script beside it as
<code>transcribe.py</code>:</p>
<pre class="term">{run("transcribe.py")}</pre>
<p>It uses <a href="https://github.com/SYSTRAN/faster-whisper">faster-whisper</a>, a fast build of Whisper that runs
on the processor of any Mac, Windows or Linux computer. <code>large-v3-turbo</code> is a faster version of Whisper's largest model;
<code>vad_filter=True</code> skips silence. Each line gets the time it starts, in the <code>[hh:mm:ss]</code> form
MAXQDA, ATLAS.ti and QualCoder read.</p>
<h3>The install error you will hit today</h3>
<p>Installed the obvious way, it fails as soon as it opens the recording:</p>
<pre class="term">{run("naive.txt")}</pre>
<p>faster-whisper 1.2.1, the current release, does not work with PyAV 17 or newer, the library it uses to read audio.
Installing PyAV below version 17 next to it fixes that. On Windows, the commands use
<code>whisper-env\\Scripts\\pip</code> and <code>whisper-env\\Scripts\\python</code> instead.</p>
<pre class="term">{run("fixed.txt")}</pre>
<p>That is a 7.6-minute mock doctor-patient consultation from the
<a href="https://github.com/babylonhealth/primock57">PriMock57</a> set (CC BY 4.0), transcribed in two and a half
minutes on the processor of an Apple M3 Max laptop. The first run also downloads the model (1.6 GB) from Hugging Face;
later runs use the copy on disk.</p>
<h3>Proof that it works offline</h3>
<p>On a Mac, <code>sandbox-exec</code> can run a command with all network access denied. <code>curl</code> cannot reach
Hugging Face inside it (exit code 6), and the transcription still runs. <code>HF_HUB_OFFLINE=1</code> tells the
library not to look for a newer model online.</p>
<pre class="term">{run("offline.txt")}</pre>
"""),
    ("gaps", "What the free route leaves to you", f"""
<p><strong>Who said what.</strong> Whisper writes words, not speakers. In the run above, the doctor's and the patient's
words share lines: "Hello. Hello, how are you? Hi. ... Good morning, sir. How can I help you this morning?" is both of
them. Adding speakers yourself usually means pyannote. Its speaker models on Hugging Face are gated: you need an
account, must accept the model's conditions, and must pass an access token to the code (checked {CHECKED}).</p>
<p><strong>Names.</strong> The transcript holds every name, place and organisation anyone said. To share it with
co-authors, an archive or a coding team, you replace them, and the same person must get the same tag in every
interview. That takes a key of who is who. Archives such as the UK Data Service advise keeping that log separate from
the anonymised files. While the key exists, the data are pseudonymised, not anonymous.</p>
<p><strong>Your analysis software.</strong> The script's <code>[hh:mm:ss]</code> lines suit MAXQDA, ATLAS.ti and
QualCoder when you link the recording. NVivo for Windows imports a table with a Timespan and a Content column. NVivo
for Mac wants <code>Name: </code> at the start of each turn, timestamps without brackets, and no other colons in the
text.</p>
<p><strong>Hard audio.</strong> On a noisy phone line the silence filter can throw away most of the speech: in our own
tests it kept 161 seconds of a 48-minute call. If a transcript is much shorter than the recording, run it again with
<code>vad_filter=False</code>.</p>
"""),
    ("free-tools", "Free tools that do more", f"""
<p>If you would rather not write code, three free programs run Whisper on your own computer with a window to click
in (as their own pages described them in November 2026):</p>
<div class="doc-table"><table><thead><tr><th>Tool</th><th>Licence</th><th>Computers</th><th>Speakers</th></tr></thead><tbody>
<tr><td><a href="https://github.com/kaixxx/noScribe">noScribe</a></td><td>Free, GPL-3.0</td><td>Windows, macOS (Apple silicon), Linux</td><td>Yes (pyannote, models included)</td></tr>
<tr><td><a href="https://github.com/aTrainTranscription/aTrain">aTrain</a> (University of Graz)</td><td>Free, AGPL-3.0</td><td>Windows, Linux; macOS through pip</td><td>Yes (pyannote)</td></tr>
<tr><td><a href="https://github.com/chidiwilliams/buzz">Buzz</a></td><td>Free, MIT</td><td>macOS, Windows, Linux</td><td>Yes, on some computers</td></tr>
</tbody></table></div>
<p>None of them replaces names, keeps a key, or writes files laid out for NVivo on a Mac.</p>
"""),
    ("local-transcripts", "Or let one command do all of it", f"""
<p><a href="../../tools/local-transcripts/?ref=guide">Local Transcripts</a> is our tool for this job. It runs on your
computer in the same way and adds the parts above: who said what, a pseudonymised copy with the key kept apart, and
files for MAXQDA, NVivo (Windows and Mac), ATLAS.ti and QualCoder. Here it is on the same consultation, on Apple
silicon:</p>
<pre class="term">{run("local-transcripts.txt")}</pre>
<p>On interviews it had never seen, it replaced 86 of 96 people's names in the shareable copy and gave 97.5 to 99.7%
of words the right speaker in two-person interviews when told there were two speakers. The <a href="../../tools/local-transcripts/?ref=guide#how-well">full
results</a>, the weak cases included, are on its page. It costs $29 once, or $99 for a research group of five.</p>
"""),
    ("checklist", "Before you transcribe", """
<ul>
<li>Check what your consent form, ethics approval and data management plan say about storage and processing.</li>
<li>Name recordings by participant code, not by name: the file name ends up in every transcript and export.</li>
<li>Keep the recordings, the full transcripts and any key on an encrypted disk, apart from what you share.</li>
<li>Read every transcript against the recording before you quote from it. Whisper mishears names and numbers.</li>
<li>Before sharing, search the shareable copy for the names you know were said.</li>
</ul>
"""),
]

TOC = "".join(f'<li><a href="#{i}">{html.escape(t)}</a></li>' for i, t, _ in SECTIONS)
BODY = "\n".join(f'<section id="{i}">\n<h2>{html.escape(t)}</h2>{b}</section>' for i, t, b in SECTIONS)
LD = json.dumps({
    "@context": "https://schema.org", "@type": "TechArticle", "headline": TITLE, "description": DESC, "url": URL,
    "dateModified": "2026-11-08", "author": {"@type": "Organization", "name": "Aurora Lab",
                                            "url": "https://the-aurora-lab.github.io/"},
    "about": ["interview transcription", "Whisper", "qualitative research", "pseudonymisation"],
}, ensure_ascii=False).replace("</", "<\\/")

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
  <meta property="og:url" content="{URL}">
  <meta property="og:type" content="article">
  <link rel="canonical" href="{URL}">
  <script type="application/ld+json">{LD}</script>
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
        <a class="btn btn-small" href="../../tools/local-transcripts/?ref=guide">Local Transcripts</a>
      </nav>
    </div>
  </header>

  <main id="main">
    <section class="docs-hero">
      <div class="aurora" aria-hidden="true"></div>
      <div class="wrap">
        <p class="crumbs"><a href="../../">Aurora Lab</a> / Guides / Interviews offline</p>
        <h1>{TITLE}</h1>
        <p class="lede">A free way to transcribe interviews on your own computer, run for real: the commands, the install
        error you will hit today and its fix, proof that it works offline, and what it leaves to you.</p>
        <ul class="meta" aria-label="Guide facts"><li>Checked {CHECKED}</li><li>macOS · Windows · Linux</li><li>Python 3.10+</li><li>Free</li></ul>
        <div class="cta">
          <a class="btn" href="#free-route">Start transcribing</a>
          <a class="btn btn-ghost" href="#gaps">What it leaves to you</a>
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
