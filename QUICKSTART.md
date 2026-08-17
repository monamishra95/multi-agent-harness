# Quickstart

Five minutes to your first gated build.

## 1. Install into a project (2 min)

```bash
git clone https://github.com/<you>/multi-agent-harness
cp -r multi-agent-harness/harness/claude-config  your-project/.claude
sh multi-agent-harness/hooks/install-hooks.sh    your-project
```

That third command installs the G3 pre-commit hook: a secret scan over your working tree and git history, plus a hygiene check. It is the one gate that can never be waived. Committing with `--no-verify` defeats the check that prevents the expensive class of mistake.

Verify it works:

```bash
python multi-agent-harness/checks/run_gates.py your-project --pre-commit
```

## 2. Write the build contract (2 min)

Two files in your project root. Without them, G0 refuses to start the build.

**`spec.md`** — intent (the *why*, and who it's for), goals, non-goals, audience, tier, build mode.

**`acceptance.yaml`** — numbered criteria, each with a verification method:

```yaml
tier: T1                 # T0 sandbox | T1 portfolio | T2 production
build_mode: one-shot     # one-shot | staged
criteria:
  - id: AC-1
    text: Ridge point for the reference chip computes to 295 ±2
    verify: golden-test
  - id: AC-2
    text: Every rendered figure carries a visible citation tag
    verify: citation-lint
  - id: AC-3
    text: No secrets in the client bundle or git history
    verify: security-scan
```

Allowed methods: `golden-test`, `citation-lint`, `fact-audit`, `smoke`, `security-scan`, `rubric`, `manual`.

Keep `manual` under 20% of criteria (40% for your first two projects while you're learning to write machine-checkable criteria). If a criterion can't be checked mechanically, it's usually under-specified rather than genuinely subjective.

## 3. Run the loop (1 min to start)

In a Claude Code session inside your project:

```
/build
```

The orchestrator checks G0, then runs Scout (parallel research) → Builder (artifact + claims manifest + tests) → Verifier (fresh context: fact audit and functional run) → Red-team (fresh context: rubric scoring), looping on RED verdicts, and finishes with the hard gates.

**The one rule that protects everything:** never paste Builder's reasoning into Verifier or Red-team. Fresh context is the quality mechanism; contaminating it fails silently. The agents are instructed to detect and report contamination, but the orchestrator not causing it is the real control.

## 4. Close the project

```
/retro
```

Librarian routes every defect filed during the build into the memory of the agent that could have caught it earliest, adds the regression check, and promotes repeat offenders to hard rules. Skipping this step turns the harness back into a fancy prompt — the next build starts no smarter.

## Calibrate the rubric

Red-team's thresholds ship uncalibrated on purpose. Before they gate anything, score two or three artifacts you've already shipped against `agents/red-team/rubric.md`, then set the threshold one notch below your best past score. The gate's job is catching regressions against your demonstrated standard, not enforcing someone else's aspiration.

Record the result in `agents/red-team/rubric.md` and freeze it after your second rubric revision.

## Adopt in waves

Building the whole harness before running anything through it is the most common failure mode. Suggested order:

1. **Wave 1** — contracts (`factsheet.json`, `claims.json`), the G3 hook, and a defect log. Ship one real project this way.
2. **Wave 2** — Verifier and Red-team as fresh-context agents with gate authority; Librarian routing; rubric calibration.
3. **Wave 3** — agent benchmarks (grown from real defects, never invented), improvement metrics, Mechanic on cadence.

Advance a wave only when the previous one survived contact with a real build. Anything you quietly stopped doing should be fixed or deleted, not re-mandated.

## Troubleshooting

**G3 fails on a placeholder key.** Files ending in `.example`/`.sample` are skipped, and values matching `YOUR_*` or `MY_*` are allowlisted. Use those conventions rather than disabling the check.

**Citation lint over-flags.** It's a heuristic screen, advisory by default. Verifier uses it to find candidates; a human decides. Use `--strict` only when you want it to fail a build.

**Builder says `blocked`.** By design: it can't invent missing facts or resolve scope questions. Check whether the factsheet has a gap or the spec has an ambiguity, then resolve it and re-run.

**Nothing improves after several projects.** Check that `/retro` is actually running and that defect records have both a lesson file and a regression artifact. Repeat defects mean routing is broken — suspect Librarian first.
