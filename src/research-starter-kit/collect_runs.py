"""Copy the real runs' outputs into src/research-starter-kit/runs/ and tools/research-starter-kit/samples/.

    ../.venv/bin/python src/research-starter-kit/collect_runs.py <demo project> <demo runs> <hooks-only project> <hooks-only runs>

The demo project is the kit's demo/make_demo.py study with the kit installed from the store zip; the runs folders are
what the kit's evals/ledger/run_sessions.py wrote. Everything is produced by the kit inside those projects
(`kit.py ledger`, `kit.py disclose`) or rebuilt from their ledgers with the kit's own message functions, so the page
shows what the agent and the user saw.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parent.parent
RUNS = HERE / "runs"
SAMPLES = SITE / "tools" / "research-starter-kit" / "samples"


def kit(project: Path, *args: str) -> str:
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(project))
    r = subprocess.run([sys.executable, str(project / ".research-kit" / "kit.py"), *args], capture_output=True,
                       text=True, env=env, check=True)
    return r.stdout


def ledger(project: Path) -> list:
    return [json.loads(line) for line in (project / "ai-use" / "ledger.jsonl").read_text().splitlines() if line]


def answer(runs: Path, name: str) -> str:
    return json.loads((runs / f"{name}.json").read_text()).get("result", "").strip()


def main(demo: Path, demo_runs: Path, hooks: Path, hooks_runs: Path) -> None:
    RUNS.mkdir(parents=True, exist_ok=True)
    SAMPLES.mkdir(parents=True, exist_ok=True)
    (RUNS / "ledger.txt").write_text(kit(demo, "ledger"))
    for venue, extra in (("elsevier", ()), ("cvpr", ()), ("jama", ("--prompts",))):
        (SAMPLES / f"statement-{venue}.txt").write_text(kit(demo, "disclose", "--venue", venue, *extra))
    full = (SAMPLES / "statement-elsevier.txt").read_text()
    start = full.index("## Declaration of generative AI")
    end = full.index("## What the policy asks for")
    (RUNS / "disclose-elsevier-excerpt.txt").write_text(full[start:end].rstrip() + "\n")

    rows = [json.loads(line) for line in (demo_runs / "results.jsonl").read_text().splitlines() if line]
    changed = sum(len(r["changed"]) for r in rows)
    named = sum(len(r["changed"]) - len(r["missing"]) for r in rows)
    secs = sum(r["seconds"] for r in rows)
    cost = sum(r["cost_usd"] or 0 for r in rows)
    (RUNS / "ledger-completeness.txt").write_text(
        f"In the eight sessions above ({secs // 60} min {secs % 60} s in all, ${cost:.2f} of Claude usage), git saw "
        f"{changed} files change, and the ledger named {named} of them: edits made through shell commands and "
        "scripts included, with the section of the paper each text change touched. Each session started from a "
        "commit, so the files git saw change are exactly that session's.\n")
    (RUNS / "results.json").write_text(json.dumps(rows, indent=1) + "\n")

    # The hooks-only runs, with the kit's own messages rebuilt from the ledger.
    sys.path.insert(0, str(hooks / ".research-kit"))
    from research_kit import config as config_mod, refs
    from research_kit.guard import Hit, describe
    cfg = config_mod.load(hooks)
    recs = ledger(hooks)
    hrows = [json.loads(line) for line in (hooks_runs / "results.jsonl").read_text().splitlines() if line]
    out = []
    for r in hrows:
        sid = r["session"]
        prompt = next(x["text"] for x in recs if x.get("s") == sid and x["ev"] == "prompt")
        out.append(f'$ claude -p "{prompt}"')
        for x in recs:
            if x.get("s") != sid:
                continue
            if x["ev"] == "denied":
                via = (x.get("cmd") or "Bash").split()[0]
                hits = [Hit(p, x["actions"][0], via) for p in x["paths"]]
                out.append(f"  Bash  {x.get('cmd', '').splitlines()[0].split(' && ')[0]}")
                out.append("  refused by the kit's pre-tool hook, which tells the agent:")
                out.append("    " + describe(hits, cfg.raw, cfg.derived))
            elif x["ev"] in ("edit", "write"):
                where = f" ({x['where']})" if x.get("where") else ""
                out.append(f"  {x['tool']}  {x['file']}{where}  +{x.get('added', 0)} -{x.get('removed', 0)}")
            elif x["ev"] == "changed" and x.get("edits"):
                for f, e in x["edits"].items():
                    out.append(f"  (by a command)  {f}  +{e['added']} -{e['removed']}")
            elif x["ev"] == "check" and x["kind"] == "references" and x.get("blocking"):
                rr = refs.RefResult(checked=x["checked"], problems=x["problems"],
                                    blocking=[p for p in x["problems"] if p["key"] in x["blocking"]])
                out.append("  turn ends: the kit's end-of-turn hook checks the new entry and sends the agent back:")
                out.append("    " + refs.describe(rr).replace("\n", "\n    "))
        text = answer(hooks_runs, r["name"])
        para = text.split("\n\n")[0]
        out.append("  Claude: " + para)
        out.append("")
    (RUNS / "hooks-only.txt").write_text("\n".join(out).rstrip() + "\n")

    for p in list(RUNS.glob("*")) + list(SAMPLES.glob("*")):
        t = p.read_text()
        for bad in ("/private/", "/Users/", "/tmp/"):
            if bad in t:
                raise SystemExit(f"{p.name} contains {bad}")
    print("runs and samples written")


if __name__ == "__main__":
    main(*(Path(a) for a in sys.argv[1:5]))
