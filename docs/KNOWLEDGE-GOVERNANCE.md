# Agent Knowledge Governance

The pattern this harness implements, described independently of the build workflow it grew out of.

Most teams operating AI agents in production converge on the same three questions once the demo stops being the point:

1. What should the agent know *deterministically*, and what should it be allowed to reason about?
2. When an agent run fails, how do you find the actual gap — and who fixes it?
3. Who is allowed to change what the agent knows, and how do you prove the change helped rather than hurt?

This document is one set of answers. They're opinionated and they're small; the value is that they're enforceable.

---

## 1. Deterministic context vs. model reasoning

An agent's knowledge is not one undifferentiated pile. This harness splits it in two, and the split is a design decision made explicitly rather than emerging by accident.

**Hard rules** live in `agent.md`. They are binding, loaded every run, and never negotiable. A hard rule is knowledge where being wrong is unacceptable and judgment adds nothing: *commercial figures require a primary source*, *keys never enter client bundles*, *never average conflicting figures*. There is no reasoning path where violating one of these is correct, so no reasoning is invited.

**Lessons** live in `memory/`, one per file. They are advisory context the model reasons *with*: what went wrong before, why it mattered, what to watch for. A lesson informs judgment rather than replacing it.

The same line runs through verification. Every gate is an automated check where a check is possible (secret scans, golden tests, coverage lints) and an agent judgment only where it isn't (defensibility, scope honesty, audience fit). The design principle: *automated where possible, judged where not, never a vibe.*

**How to decide which side something belongs on.** Ask what happens when the model reasons about it and gets it wrong. If the answer is "an incident" — legal language, pricing, safety constraints, brand-mandated wording, regulated disclosures — it's deterministic: retrieve it verbatim, don't paraphrase it, don't let it be summarized. If the answer is "a slightly worse output," it's reasoning territory, and forcing determinism there produces the brittle, over-specified prompt files that degrade as models improve.

The failure modes are symmetric and both common: too much determinism makes agents rigid and expensive to maintain; too little makes them confidently wrong about things that had a right answer sitting in a document.

---

## 2. Diagnosing failed runs

A failure is a *defect*, and defects get classified, routed, and closed — the same discipline software teams apply to bugs, applied to agent knowledge.

**Classification.** Six classes: Fact (fabricated, stale, wrong-tier source, unlabeled confidence), Code/Function, Security, Judgment, Process/Contract, Efficiency. Severity runs SEV1 (security, fabrication, or any escaped defect) to SEV4 (process friction).

**Detection stage.** Where was it caught — during construction, at verification, at adversarial review, at release, or in the wild? Cost rises at every stage; the whole system exists to shift detection left, and the distribution across stages is a tracked metric.

**Routing by earliest catch, not by blame.** The central question for every defect is: *which agent could have caught this earliest, at the lowest cost?* A stale figure surfaced by the verifier still routes to the researcher, because a freshness rule there prevents recurrence more cheaply than a check downstream. Blame-based routing produces defensive agents and no learning; earliest-catch routing produces prevention.

**Closure requires an artifact.** A defect record isn't closed until it has both a lesson file and a regression artifact — preferably an automated check, otherwise a rubric line, otherwise a checklist item. A lesson that stays prose is a lesson waiting to be forgotten. Lessons that *can* be automated *must* be.

**Promotion and demotion.** First occurrence writes a lesson. Second occurrence of the same root cause promotes it to a hard rule with a blocking check. Any security issue, fabrication, or escaped defect skips the grace period entirely. In the other direction, rules that haven't fired in five projects or ninety days are reviewed for deletion — brains must stay small enough to load whole, and pruning is as much a part of governance as adding.

**Distinguishing gap types.** When a run fails, the useful question is *which* gap: the agent lacked the knowledge (knowledge gap), had it but didn't surface it (retrieval gap), surfaced it but reasoned badly (reasoning gap), or the knowledge itself was wrong (source gap). These route differently — to curation, to retrieval configuration, to the model or rules layer, and to the source ledger respectively. Conflating them is the most common reason teams "fix" an agent repeatedly without the failure rate moving.

---

## 3. Curating knowledge from across an organization

Knowledge enters agents through contracts, not conversation.

**Sourced, tiered facts.** Research output is a structured `factsheet.json`, not prose. Every fact carries its source URL, a source tier (0 primary — vendor documentation, filings, official statements; 1 research — papers, proceedings, lab publications; 2 practitioner — forums, engineering blogs, newsletters), the date it was true, the date it was retrieved, and a confidence value from a fixed four-word vocabulary. Different claim types require different tiers: commercial figures require tier 0, technical claims tier 1 or better, and tier 2 is never a figure's only source.

**Unknowns are first-class.** What isn't known is recorded explicitly rather than quietly filled with something plausible. An agent that reports "this number isn't published anywhere" is more useful than one that produces a confident estimate, and the harness treats an empty unknowns list on a substantial research task as suspicious.

**A source reliability ledger.** Sources that proved unreliable are recorded, with the evidence and the incident that demoted them. The ledger is consulted before every research run and updated only through the defect pipeline, so distrust is earned and traceable rather than accumulated as folklore.

**Provenance survives into the artifact.** Every claim rendered in an output maps back to a fact or a shown derivation, at 100% coverage. This is what makes "where did this number come from?" answerable months later, by someone who wasn't there.

---

## 4. Change control for agent brains

**One editor.** Exactly one agent (Librarian) may modify any brain, memory, adapter, or rubric. Everything else proposes. Multiple mutators with no attribution means a degradation nobody can trace.

**Benchmarks gate edits.** Each agent carries a regression benchmark grown from its own past defects — never invented upfront, because pre-written benchmarks test imagined failure modes rather than real ones. Once an agent has a few earned cases, any brain edit re-runs them first, and an edit that degrades the benchmark is reverted. Without this, "self-improving" and "self-degrading" are indistinguishable from the inside.

**Versioned and attributable.** Every artifact carries the hash of the producing agent's brain plus the model that ran it, so quality changes can be attributed to a brain edit, a model swap, or neither. Improvement metrics are segmented by model for the same reason.

**Measured, not asserted.** The metrics are deliberately about impact rather than volume: escaped defects, catch-stage distribution, correction rate, repeat-defect rate, cycles-to-green, review scores. The one that matters most is the repeat-defect rate — it's the direct measure of whether routing works. If the curves are flat after several projects, the loop isn't learning, and the routing step is the first suspect rather than the agents.

---

## Limits

Memory here is flat files loaded whole. That is deliberate and it does not scale: past a few dozen lessons per agent, this needs chunking, tagging, and retrieval, and this harness has none of that — no ranking, no embeddings, no retrieval-quality evaluation, no golden query sets or ranking metrics.

What it does provide is the layer above: what is allowed into the knowledge base, at what evidentiary standard, who may change it, and what proves a change helped. Those questions don't go away when a retrieval system arrives — they get harder, because a larger knowledge base makes unvalidated content easier to hide. Teams at retrieval scale should read this as the policy layer over their RAG stack, not a substitute for one.
