# Contributing

Contributions welcome. This project has one unusual constraint, and it's the important one.

## Lessons must be earned

Agent memories (`agents/*/memory/`) ship empty and stay that way until real failures fill them. **A pull request adding a lesson must reference a defect record with evidence** — what happened, where it was caught, what would have caught it earlier.

This is not bureaucracy. An open memory system without this rule fills with plausible-sounding advice nobody validated, agent brains grow past the point where they can be loaded whole, and the harness degrades into the over-prescriptive prompt file it was built to replace. The value of a lesson is the incident behind it.

If you have a strong intuition with no incident behind it yet, open an issue instead. It becomes a lesson the first time it costs someone something.

The same applies to hard rules in `agent.md`: those are promoted from lessons after a second occurrence of the same root cause, not written directly.

## What's most useful

- **Gate checks.** New checks in `checks/` — dependency auditing, license scanning, accessibility linting, retrieval-quality evaluation. Each should be runnable standalone and return a clear pass/fail.
- **Model adapters.** `adapters/` currently covers two model classes. Adapters for other models — including non-Anthropic ones — are valuable and self-contained.
- **Schema improvements.** Contract changes bump `schema_version` and need a migration note.
- **Documentation.** Especially worked examples from real projects, with the boring parts left in.

## What to avoid

- Adding agents. Six is deliberate. A seventh needs a defect class no existing agent could own.
- Loosening the fresh-context rule for Verifier or Red-team. If that becomes optional, the harness's central quality claim is gone.
- Making G3 waivable.
- Speculative features for hypothetical scale. This harness is opinionated about doing the simplest thing that works.

## Pull request checklist

- [ ] Gate scripts still pass on this repo: `python checks/run_gates.py . --release`
- [ ] Any figure added to documentation carries a source or an explicit hedge
- [ ] New checks include an example of both a passing and a failing input
- [ ] Lessons/rules reference the defect record that produced them
- [ ] No placeholder text, junk files, or secrets (CI enforces this, but check first)

## Development

The harness gates itself in CI — the same scripts it ships run against this repository on every push. If you change a check, expect it to be applied to your own change.

```bash
python checks/run_gates.py . --release
python checks/lint_citation.py . --strict   # optional: treat the screen as blocking
```

## Code of conduct

Be direct, be kind, assume competence. Critique work rather than people. Disagreement with a maintainer decision is fine; relitigating a closed decision without new evidence is not.

## License

By contributing, you agree your contributions are licensed under the Apache License 2.0.
