# Protocol Specification

Version 0.2. The authoritative rules for the harness: defect routing, I/O contracts, production gating, and model portability. `agent.md` files implement this; where they disagree, this document wins until amended.

**Design principles**

1. Zero *escaped* defects, not zero defects — every error cheap to catch, impossible to ship, impossible to repeat.
2. The value lives in the harness, not the model — contracts, gates, and brains survive a model swap intact.
3. Agents do the paperwork. Any protocol step that costs the operator more than a minute is a protocol bug.

---

## Part 1 — Defect Routing

### 1.1 Detection stages

| Stage | Where caught | Cost |
|---|---|---|
| S0 | Builder self-check during construction | Trivial |
| S1 | Verifier (fact or function gate) | Low |
| S2 | Red-team (judgment gate) | Medium |
| S3 | Release gate | High |
| S4 | **Escaped** — found in the wild | Incident |

Any S4 defect triggers a postmortem (§1.8) regardless of severity.

### 1.2 Taxonomy

| Class | Definition | Sub-codes | Default owner |
|---|---|---|---|
| **F — Fact** | Wrong, uncited, stale, or mislabeled figure | F1 fabrication · F2 stale · F3 unreliable tier · F4 transcription drift · F5 missing confidence label | F1–F3, F5 → Scout · F4 → Builder |
| **C — Code/Function** | Logic error, broken build, failing test | C1 logic · C2 regression · C3 integration · C4 performance | Builder |
| **X — Security** | Secret exposure, injection, unsafe permissions | X1 secret leak · X2 injection · X3 permissions · X4 dependency vuln | Builder (introduction), release gate (escape) |
| **J — Judgment** | Indefensible claim, weak framing, scope dishonesty | J1 defensibility · J2 framing · J3 scope honesty · J4 audience misfit | Red-team (rubric gap) or spec (criteria gap) |
| **P — Process/Contract** | Schema violation, skipped step, coverage shortfall | P1 schema · P2 skipped gate · P3 coverage | The violating agent |
| **E — Efficiency** | Redundant work, missed parallelism, model misrouting | E1 redundancy · E2 missed fan-out · E3 misrouting | Mechanic finding, routed to the wasteful agent |

Ownership is earliest-catch, never blame.

### 1.3 Severity

| Sev | Definition | Consequence |
|---|---|---|
| SEV1 | Security, fabrication, or any escaped defect | Postmortem + hard rule + gate change |
| SEV2 | Wrong figure or broken feature caught internally | Lesson + regression artifact |
| SEV3 | Quality or judgment miss | Lesson; rubric line if novel |
| SEV4 | Process or efficiency | Lesson only |

### 1.4 Defect record

```yaml
id: DEF-YYYY-MM-DD-NNN
project:
class:               # F1-F5 | C1-C4 | X1-X4 | J1-J4 | P1-P3 | E1-E3
severity:            # SEV1-SEV4
stage_detected:      # S0-S4
stage_should_have:   # earliest realistic catch point
owner_agent:
model:               # model in use when introduced
description: >
evidence:            # ref proving it
root_cause: >
lesson_file:
regression_artifact: # automated check > rubric line > checklist
promotion: memory    # memory | hard-rule | gate
recurrence_of: null
model_specific: false
status: open         # closed requires lesson_file AND regression_artifact
```

A record without a `regression_artifact` is incomplete. Lessons that can be automated must be.

### 1.5 Lifecycle

Detect (any agent files it) → Route (Librarian: class, severity, earliest-catch owner, `model_specific` judgment) → Lesson (one file in the owner's `memory/`) → Regression artifact (specced, added to the owner's benchmark) → Promote/close.

### 1.6 Promotion and demotion

| Trigger | Action |
|---|---|
| 1st occurrence | Lesson file in `memory/` |
| 2nd occurrence, same root cause | Hard rule in `agent.md` + blocking check |
| Any SEV1 or S4 escape | Hard rule + gate change + postmortem, no grace |

**Demotion:** rules unfired in 5 projects or 90 days (whichever first) are reviewed for pruning. Wrong lessons are deleted, not archived.

**Benchmarks grow from defects.** Each agent's `evals/` starts empty; every closed defect contributes its regression artifact as a case. Expect 5–10 earned cases per agent within three projects; zero invented cases. Every brain edit re-runs the benchmark before landing, and a degrading edit is reverted. While a benchmark holds fewer than 3 cases, edits land on Librarian review alone.

### 1.7 Metrics

Tracked per project, plotted across projects, **always segmented by model**:

- **Escaped defects (S4)** — north star, target zero
- **Catch-stage distribution** — should shift toward S0/S1 over time
- **Correction rate** (corrections per 100 claims) — should fall
- **Repeat-defect rate** — direct measure of whether routing works; should approach zero
- **Cycles to green** — should fall
- **Review score mean** — should rise, then plateau

These need 4–5 projects before they mean anything. Flat curves after that means the loop isn't learning; suspect routing first.

### 1.8 Postmortem (SEV1 / S4 only)

Five questions, ten minutes: What happened? Where was the earliest realistic catch point? Why did that gate miss it? What rule or gate changed? What artifact now makes recurrence impossible?

---

## Part 2 — I/O Contracts

Every cross-agent artifact carries an envelope. Contract violations are P-class defects.

```yaml
envelope:
  project_id:
  agent:
  agent_version:     # hash of agent.md + memory/ at run time
  adapter_version:
  model:
  build_mode:        # one-shot | staged
  schema_version: "0.2"
  produced_at:
```

`agent_version` + `model` together make degradations attributable.

### 2.1 spec.md + acceptance.yaml

The build contract; no build starts without it (G0). `spec.md` carries intent, goals, non-goals, audience, tier, build mode. `acceptance.yaml` carries numbered criteria, each with a `verify` method from: `golden-test`, `citation-lint`, `fact-audit`, `smoke`, `security-scan`, `rubric`, `manual`. Manual criteria cap: 20% (40% for a team's first two projects).

### 2.2 factsheet.json — Scout → Builder, Verifier

Per fact: `id`, `claim`, `value`, `as_of`, `retrieved_at`, `source_url`, `source_tier` (0 primary / 1 research / 2 practitioner), `confidence` (`confirmed` | `corroborated` | `unverified` | `directional`), and for research sources `arxiv_version`, `peer_reviewed`, `citation_status`. Plus explicit `unknowns` and `source_ledger_deltas`.

Rules: commercial figures require tier 0; technical claims tier ≤1; tier 2 is never a sole source. Conflicting figures are reported as a spread with both citations, never averaged. Pricing older than 30 days and other figures older than 90 days are not `confirmed`.

### 2.3 Build package — Builder → Verifier

Artifact plus `claims.json` (every rendered figure maps to a fact or a shown derivation, 100% coverage), `testplan.md` (criteria-to-test mapping plus what isn't covered and why), `selfcheck.log` (every progress claim tied to a tool result).

Builder's terminal states are `ready-for-verification` or `blocked`. It cannot set `done`.

### 2.4 verification-report.json — Verifier → orchestrator, Librarian

Fresh context; inputs are spec, factsheet, and build package only. Contains per-criterion status with evidence, fact-audit results and sampling policy, citation coverage, functional results (golden tests, smoke, screenshots reviewed, console errors), and defects filed.

Verdict is binary GREEN or RED. "Green with concerns" does not exist — a concern is a filed defect or it is nothing. A report without execution evidence is itself a P2 defect.

### 2.5 redteam-score.json — Red-team → orchestrator, Librarian

Fresh context; artifact and spec only. Per-line scores with quoted evidence, mean, floor, exactly three ranked weaknesses, and separately-flagged rubric gaps. Scores compare only within a rubric version. Unevidenced scores are void.

### 2.6 Librarian outputs

Routed and closed defect records, lesson files, `agent.md` diffs with before/after benchmark results attached, rubric updates, postmortems.

### 2.7 mechanic-report.md

Waste findings, missed parallelism, and capability proposals — each evidence-bound to a transcript, log, or defect record. Capability proposals must take the form *"X time was spent doing Y manually across N builds; Z removes it."* Proposals without an observed-friction reference are invalid by contract.

---

## Part 3 — Production Gating

### 3.1 Tiers

| Tier | Definition | Gates |
|---|---|---|
| **T0 — Sandbox** | Exploration, throwaway | None. **May not be published or shared.** |
| **T1 — Portfolio** | Public, reputation-bearing | G0–G4 + G5-lite |
| **T2 — Production** | Someone else relies on it | G0–G6, all blocking |

Promotion up a tier requires passing the target tier's gates from scratch.

### 3.2 Gates

**G0 — Spec** (blocks build start): spec and acceptance criteria exist, each with a verify method; tier and build mode declared; manual cap respected.

**G1 — Fact** (blocks verification): claims coverage 100%; fact audit per sampling policy — 100% for the first two projects and all T2 work, thereafter risk-based (100% of tier-2-sourced, unverified/directional, and anything older than 30 days, plus ~25% random of confirmed). Zero tolerance for fabrication.

**G2 — Function** (blocks verification): golden tests pass; citation lint clean; smoke test on the *built* artifact; zero console errors; screenshots reviewed. Computational results verified programmatically, never by eyeball.

**G3 — Security** (blocks every commit; hook-enforced at all tiers): secret scan over working tree and git history; committed `.env` detection; client-bundle key grep; dependency audit; permission review for anything touching user data or external services. Any failure is SEV1. **Unwaivable.**

**G4 — Judgment** (blocks release): review score meets the calibrated threshold on floor and mean; each of the three top weaknesses is fixed or has a documented response in the repo.

**G5 — Release** (T2 full, T1 lite): staging first, post-deploy smoke on the live URL, rollback path documented, honest limitations section current, monitoring configured. T1 lite: live smoke plus honest limitations.

**G6 — Post-release watch** (T2): scheduled freshness/link/uptime checks and a defect intake path. Every wild-found issue is an S4 → postmortem → gate change.

### 3.3 Waivers

Only the operator may waive a gate, and a waiver is a logged record with a reason and an expiry date — never a silent skip. **G3 is unwaivable.** Waivers without expiry are invalid. An escape traced to an active waiver counts as an S4 *and* closes the loophole.

---

## Part 4 — Model Portability

### 4.1 Constant vs. swappable

| Constant | Swappable |
|---|---|
| Contracts, gates, defect routing | Model per agent role |
| Agent identities and hard rules | Model adapters |
| Memories, benchmarks, defect log, metrics | Build mode, effort settings |

### 4.2 Adapters

Core `agent.md` files contain no model-specific prompting. Each supported model class gets a thin adapter holding only its specific patterns. Librarian judges `model_specific` on every defect: model quirks go to the adapter, universal lessons to the core brain. Misfiling universal lessons into an adapter loses them on model swap; misfiling quirks into a core brain pollutes every model with one model's failure modes.

### 4.3 Build modes

- **one-shot** — Builder receives the full spec and builds end-to-end, self-verifying at intervals it sets; Verifier runs at the end plus spot checks.
- **staged** — the spec is decomposed into stages with a Verifier pass per stage.

Choose by demonstrated capability on the agent's benchmark, not by model name.

### 4.4 Adoption waves

1. **Wave 1** — contracts, security hook, defect log. Gate: one real project shipped through it.
2. **Wave 2** — fresh-context Verifier and Red-team with gate authority; Librarian routing; rubric calibration.
3. **Wave 3** — benchmarks, metrics, Mechanic on cadence.

Advance only when the previous wave survived a real build. Anything quietly abandoned gets fixed or deleted, not re-mandated.
