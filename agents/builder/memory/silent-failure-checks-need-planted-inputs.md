A check that has never been shown a defect it should catch is unproven — plant one before trusting it.

The citation lint's regex required a word boundary after its unit group, so "47%" never matched (a "%" followed by a space is non-word to non-word — not a boundary). Every percentage in every document passed silently, and the check cheerfully reported "clean." It had been validated only against inputs that happened to use word-character units like `ms` and `TFLOPS`. Why it mattered: a check that reports clean while missing an entire class of defect is worse than no check, because it manufactures confidence. Rule: every check ships with a planted input it must catch and a legitimate input it must not flag, both in the seeded-defect suite and both running in CI.

Ref: DEF-2026-08-17-001.
