# Red-team rubric — v1.0

Scale per line: **1** indefensible · **2** weak, obvious pushback lands · **3** adequate, survives casual review · **4** strong, survives hostile review with minor concessions · **5** airtight, the reviewer learns something.

Every score requires a quoted-evidence string from the artifact. Unevidenced scores are void.

| Line | Question |
|---|---|
| **R1 — Defensibility** | Does every claim survive hostile probing? Are hedges precise (estimate vs. confirmed vs. unknown)? One indefensible number caps this line at 2. |
| **R2 — Evidence discipline** | Are sources visible at the point of claim, not just in a README? Are estimates and synthetic data labeled where they're displayed? |
| **R3 — Demonstration over description** | Does the artifact *show* the capability, or narrate it? A working pipeline beats a diagram of one. |
| **R4 — Scope honesty** | Are limitations stated plainly, inside the artifact? Is anything overclaimed? Honest "unknown" and "N/A" score up, not down. |
| **R5 — Technical correctness** | Do the numbers, math, and architecture hold when recomputed or inspected? Is correctness verified programmatically or by eyeball? |
| **R6 — Audience fit** | Does it land for the declared audience? Does the strongest feature map to what that audience actually evaluates? |
| **R7 — Anticipated pushback** | Are the three weakest points already identified, with documented responses, before a reviewer finds them? |
| **R8 — Craft & hygiene** | Repo cleanliness, no secrets, no placeholder text shipped, tests present, deploy story real. |

## Gate G4 thresholds

**Uncalibrated. These must be set locally before they gate anything.**

| Tier | Floor | Mean |
|---|---|---|
| T1 | _(set locally)_ | _(set locally)_ |
| T2 | _(set locally)_ | _(set locally)_ |

### How to calibrate

1. Pick two or three artifacts you have already shipped and would defend publicly.
2. Score each against the lines above, with quoted evidence — no leniency for it being your own work.
3. Set the T1 mean **one notch below your best score**, and the T1 floor at the lowest line score you'd accept on anything public. For T2, raise the floor on R1 and R2 specifically, since fact defensibility is what production work fails on.
4. Record the calibration run — the artifacts, the scores, the reasoning — next to this file. Thresholds without provenance get relitigated every time someone dislikes a verdict.
5. Freeze after your second rubric revision. Scores compare only within a rubric version.

The gate's job is catching regressions against your demonstrated standard, not enforcing someone else's aspiration. Published thresholds from another team are a starting point to replace, never a benchmark to hit.

## Rubric changes

Versioned and Librarian-gated, exactly like agent brain edits. When Red-team finds a real problem the rubric has no line for, that's a **rubric gap** — reported separately from scores, and the mechanism by which this file improves. Bump the version on any line change; historical scores stay attached to the version that produced them.
