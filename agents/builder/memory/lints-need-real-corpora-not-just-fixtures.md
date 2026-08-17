Run a new check against a real repo before trusting its output — synthetic fixtures prove it fires, real corpora prove it's usable.

The citation lint passed its seeded-defect fixtures cleanly, then returned 33 flags on its first real repository, roughly a third of them CSS declarations and HTML attributes (`width: 100%`, `data-tflops="312"`). Layout numbers are not claims. The genuine findings — uncited hardware specifications in documentation tables — were buried under noise. Why it mattered: a check whose output has to be manually filtered gets ignored within two runs, and an ignored check is functionally identical to no check while still costing time. Rule: exercise a new check against at least one real project before shipping it, and treat false-positive rate as a first-class pass condition alongside detection rate.

Ref: DEF-2026-08-17-003.
