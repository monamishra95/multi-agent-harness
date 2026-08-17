API keys never enter client bundles — the starter template you build from may already violate this; check before trusting it.

A project began from an official starter template that inlined an API key into the browser bundle through a build-time variable substitution. It was caught and moved to a server-side function reading the key from the environment at request time — but only because someone looked. Why it mattered: one deploy away from a harvested key and an unbounded bill, and on a public-facing project, a visible demonstration of the exact judgment lapse a reviewer probes for. The lesson generalizes past keys: inherited scaffolding carries inherited defects, and "it came with the template" is not a security review.

Ref: DEF-2026-07-19-XXX (sample — genericized from a real incident)
