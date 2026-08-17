# Lesson format — illustrative samples

These are **examples of the format**, not lessons pre-loaded into any agent. Agent memories ship empty and fill only from your own defects (see [CONTRIBUTING.md](../../CONTRIBUTING.md)).

Each sample below is derived from a real incident, genericized. Read them to learn the shape: one lesson per file, a one-line summary first, then what happened and why it mattered, then the defect reference.

## What makes a good lesson

- **Specific enough to act on.** "Be careful with pricing" is useless; "pricing figures older than 30 days are not `confirmed` — re-fetch before any build" is a rule.
- **Carries the why.** The incident is what makes the rule stick and what lets a future reader judge whether it still applies.
- **Names the cost.** What did this failure nearly cause, or actually cause? That's the difference between a lesson and a preference.
- **Deletable.** If it turns out to be wrong, delete it. Wrong lessons are worse than no lessons because they're loaded every run.

## What makes a bad lesson

- Restating something the code, spec, or documentation already says.
- General best practice with no incident behind it (open an issue instead).
- Anything so broad it will never fail to apply — those become noise that dilutes the rules that matter.
