# Adapter: Claude Opus-class (adapter_version: opus-1.0)

Model-specific layer for Opus 4.8 and comparable models. Only differences from core behavior belong here.

## Defaults

- Build mode: `staged` — decompose the spec into stages; Verifier pass at every stage boundary, not just the end. Build one component at a time and confirm it before moving on; the sequential-prompt playbooks written for earlier model generations are the reference implementation of this mode, not a deprecated practice.
- Verification intervals: tighter. Builder self-checks after each component, not each milestone.
- Parallel subagents: dispatch works but supervise more closely; prefer fewer, better-scoped subagents over wide fan-outs.

## Steering

- Enumerate steps explicitly where the Fable adapter uses one line. Checklists over principles: "confirm output before moving to the next stage" is load-bearing here, not optional.
- Repeat hard constraints (ban-invention, citation requirements) at each stage boundary — instruction retention over long runs is weaker; a constraint stated once at the top will fade.
- Ask Builder to restate acceptance criteria for the current stage before building it; catches drift cheaply.
- Red-team and Verifier prompts should include 2–3 worked examples of the expected output format (Fable infers the format from the schema alone; Opus-class benefits from exemplars).

## Cautions

- One-shot full-spec builds produce shallower work on complex artifacts — resist the temptation even when the first stage goes well.
- Self-critique in the same context is weaker still than on Fable; fresh-context Verifier/Red-team separation is non-negotiable, never simulated with "now switch roles."
