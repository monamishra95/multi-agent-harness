# multi-agent-harness

[![gates](https://github.com/monamishra95/multi-agent-harness/actions/workflows/ci.yml/badge.svg)](https://github.com/monamishra95/multi-agent-harness/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

A six-agent build harness that makes AI-assisted work verifiable, gated, and self-correcting. Agents are durable entities with editable brains, earned memories, and regression benchmarks — not prompts you retype each project.

It exists to make three guarantees:

1. **Nothing fabricated ships.** Every figure in an output traces to a sourced fact or a shown derivation.
2. **Nothing broken ships.** Gates block; they don't advise.
3. **No mistake happens twice.** Every defect is routed to the agent that could have caught it earliest and becomes a permanent rule or automated check.

The target is not zero defects — it's zero *escaped* defects: every error cheap to catch, impossible to ship, impossible to repeat.

## Quickstart

```bash
git clone https://github.com/monamishra95/multi-agent-harness
cp -r multi-agent-harness/harness/claude-config  your-project/.claude
sh multi-agent-harness/hooks/install-hooks.sh    your-project
```

Then in your project: `/build` runs the loop, `/retro` closes it, `/mechanic` audits on cadence. Full walkthrough in [QUICKSTART.md](QUICKSTART.md).

## The six agents

| Agent | Role | Key constraint |
|---|---|---|
| **Scout** | Research → a sourced, dated, confidence-labeled factsheet | Never fabricates, never averages conflicting figures; tiered sources per claim type |
| **Builder** | Constructs the artifact from spec + factsheet | Cannot declare "done" — only `ready-for-verification` or `blocked` |
| **Verifier** | Fact audit + functional verification | **Fresh context.** Binary GREEN/RED. Reports, never repairs |
| **Red-team** | Adversarial review against a versioned rubric | **Fresh context.** Exactly three weaknesses, every time, with quoted evidence |
| **Librarian** | Routes every defect into the right agent's memory | The *only* agent permitted to edit brains |
| **Mechanic** | Audits the harness itself: cost, parallelism, unused capabilities | Cadence-only. Proposes; never commits |

Fresh context for Verifier and Red-team is the core quality mechanism. Self-critique in the same session that produced the work is weaker than an independent reviewer that never saw the reasoning — so the harness structurally prevents that context from leaking.

## The loop

```
spec (G0) → Scout → Builder → Verifier ⇄ Builder → Red-team → gates → ship → retro → mechanic
                                  ↑                                            ↓
                                  └──────── smarter agents next run ───────────┘
```

Each agent is a directory: `agent.md` (binding rules), `memory/` (earned lessons), `evals/` (regression benchmark). The harness improves because corrections compound — a stale figure caught in verification becomes a lesson in Scout's memory, then a lint that enforces it forever.

## Gates

| Gate | Checks | Blocks |
|---|---|---|
| G0 | Spec + acceptance criteria exist, each machine-verifiable | Build start |
| G1 | Claims coverage 100%, fact audit, zero fabrication | Verification |
| G2 | Golden tests, citation lint, smoke, screenshots reviewed | Verification |
| G3 | Secret scan, hygiene — **unwaivable, pre-commit hook** | Every commit |
| G4 | Red-team score threshold | Release |
| G5 | Placeholder lint, honest limitations, deploy smoke | Release |
| G6 | Post-release watch (freshness, uptime) | Nothing — feeds the defect log |

Tiers set the load: **T0** sandbox (no gates, never published), **T1** portfolio (G0–G4 + light release), **T2** production (all gates). Promoting an artifact up a tier means passing the target tier's gates from scratch — demos don't silently become products.

Run them yourself:

```bash
python checks/run_gates.py <path> --pre-commit   # G3: secrets + hygiene (hard fail)
python checks/run_gates.py <path> --release      # + placeholder (hard) + citation screen (advisory)
```

---

## For agent knowledge governance

This harness is also a working implementation of a pattern many teams need independently of code: **governing what an AI agent knows, who may change it, and how you prove a change helped.**

**Deterministic context vs. model reasoning.** The harness draws this line explicitly and in two places. In agent knowledge: `agent.md` holds hard rules (binding, always loaded, never negotiable), `memory/` holds lessons (advisory context the model reasons with). In verification: every gate is an automated check where one is possible, an agent judgment where it isn't, and never a vibe. Deciding which side of that line a piece of knowledge belongs on is a design act, and the harness forces it to be explicit rather than implicit.

**Fixing the brain from failed runs.** The defect-routing protocol ([PROTOCOL.md](docs/PROTOCOL.md), Part 1) is a structured pipeline for exactly this: a failure is classified (fact, function, security, judgment, process, efficiency), assigned to the agent that could have caught it earliest and most cheaply — not the one that introduced it — then converted into a lesson file, a regression check, and, on recurrence, a hard rule. Repeat failures are treated as routing failures, not agent failures.

**Structured knowledge curation.** Knowledge enters agents through contracts, not conversation: `factsheet.json` carries per-fact source tiers (primary / research / practitioner), dates, and a fixed confidence vocabulary; a persistent source ledger records which sources have proven unreliable and why. Lessons follow one format — one lesson per file, one-line summary, why it mattered, the defect that produced it.

**Anti-vanity instrumentation.** The metrics are deliberately about impact rather than output volume: escaped defects, catch-stage distribution (are failures being caught earlier over time?), correction rate, repeat-defect rate, cycles-to-green. Metrics are segmented by model, so a regression after a model swap is distinguishable from a regression caused by a brain edit.

**Known limits of this pattern.** Memory here is flat files loaded whole — deliberately simple, and it will not survive a knowledge base large enough to need retrieval. There is no chunking, tagging, or ranking layer, and no retrieval-quality evaluation (no golden query sets, no ranking metrics). This harness solves the *governance* problem — what enters the brain, who edits it, what proves it helped — which sits upstream of the retrieval problem. Teams operating at retrieval scale should treat it as the policy layer above their RAG stack, not a replacement for one.

---

## What it's good for

Artifacts whose value depends on being verifiably right: research-backed analysis, technical explainers with checkable math, live-data dashboards and monitors, production tools, and work products where a wrong number is expensive. It's also recursive — the harness is a reasonable way to build skills, plugins, and other agent workflows.

**What it's the wrong tool for:** creative work with no factual surface, exploratory spikes (use T0 and don't feel bad), and anything where you can't yet write a spec. If you can't specify it, brainstorm first.

## Model portability

Contracts, gates, and brains are model-agnostic. Model-specific prompting lives in thin adapters (`adapters/`), and each run declares a build mode: `one-shot` for models that build end-to-end reliably, `staged` for models that do better with per-stage verification. Swapping models changes the adapter, not the harness.

## Status

Version 0.2. Built and operated by one person; the protocol is complete and the gate scripts are tested, but the improvement metrics need several projects of data before they mean anything, and the Red-team thresholds ship **uncalibrated** by design — see [QUICKSTART.md](QUICKSTART.md#calibrate-the-rubric) for the calibration step. Treat published thresholds as a starting point to replace with your own, not a benchmark.

## Documentation

- [QUICKSTART.md](QUICKSTART.md) — set up and run your first build
- [docs/PROTOCOL.md](docs/PROTOCOL.md) — the full specification: defect routing, I/O contracts, gating
- [docs/KNOWLEDGE-GOVERNANCE.md](docs/KNOWLEDGE-GOVERNANCE.md) — the agent-brain governance pattern in depth
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to contribute, including why lessons must be earned

## License

Apache License 2.0. See [LICENSE](LICENSE).
