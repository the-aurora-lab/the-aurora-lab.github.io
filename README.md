# Aurora Lab

Source for [the-aurora-lab.github.io](https://the-aurora-lab.github.io): sample outputs of the Aurora Lab agent skills for researchers. The skills themselves are on [Agensi](https://www.agensi.io/creators/aurora-lab).

Static HTML/CSS/JS, no build step. GitHub Pages serves `main` as-is.

## Regenerating the figures

Every figure and number on the page comes from one script:

```bash
pip install numpy matplotlib
python src/figures.py
```

It writes `assets/fig/*` and `src/feigenbaum.json`, and stops with an error if a computed value drifts from its reference (Feigenbaum's δ, known superstable parameters, Lyapunov signs).

The table in `index.html` is copied from `src/feigenbaum.json`.

## Reference Verifier page

`tools/reference-verifier/index.html` is written by `src/reference-verifier/page.py` (run from the site root with
`../.venv/bin/python`). Its terminal transcripts (`src/reference-verifier/runs/`), screenshots
(`assets/shots/reference-verifier/`), sample reports (`tools/reference-verifier/samples/`, kept out of search engines
by `robots.txt`) and demo outputs come from real runs of the released builds on `tools/reference-verifier/demo/`.
The icon is drawn by `src/reference-verifier/logo.py`.

## Analytics

Every page loads GoatCounter (`auroralabskills.goatcounter.com`; no cookies, no personal data). Pages written by the
generators get the tag from their templates; `site_check.py` fails a page without it. Sample reports are left as the
tools wrote them.
