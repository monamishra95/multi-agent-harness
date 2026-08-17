# Defect log

One YAML file per defect, named `DEF-YYYY-MM-DD-NNN.yaml`. Copy `TEMPLATE.yaml` to start.

## Rules

- **Anyone files, Librarian routes.** The finder records what they saw; Librarian assigns class, severity, and owner.
- **Owner is the earliest cheapest catcher, not the introducer.** A stale figure caught in verification still routes to research, because a freshness rule there prevents recurrence more cheaply than a downstream check.
- **Closure requires two things:** a lesson file and a regression artifact. Preference order for the artifact: automated check → rubric line → checklist item. A lesson that stays prose is a lesson waiting to be forgotten.
- **`recurrence_of` triggers promotion.** Second occurrence of the same root cause becomes a hard rule with a blocking check. Any SEV1 (security, fabrication) or S4 (escaped to the wild) skips the grace period and additionally requires a five-question postmortem.
- **If filing takes more than a minute, that's a protocol bug.** Fix the tooling, not the discipline.

## Zero-tolerance classes

| Class | Why |
|---|---|
| F1 — fabrication | The harness's central promise; one invented figure fails the gate outright |
| X1 — secret exposure | Unwaivable gate, enforced pre-commit |
| Any S4 — escaped defect | The one metric that must stay at zero |

## Privacy note

This directory is where the harness's institutional memory accumulates, and defect records naturally contain project specifics. If you fork this repo for internal use, decide early whether your defect log is public. A useful split: keep the framework public and the log private — the framework is the shareable part, the log is the evidence it works for you.
