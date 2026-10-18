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
