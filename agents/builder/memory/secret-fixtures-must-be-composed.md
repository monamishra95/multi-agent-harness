Test fixtures containing fake credentials must be assembled from fragments, never written as literals.

The seeded-defect suite generated its fixtures into a temp directory at runtime and its docstring said so — but the generator held the fake keys as literal strings in its own source, so the repository's own secret scan flagged the test file and turned the release gate red. Why it mattered: the claim "no fake credentials are committed" was reasoned about at the wrong layer, and the file contradicted its own documentation. Rule: compose secret-shaped test data from concatenated fragments (`"AIza" + "SyB..."`) so the payload never exists contiguously in tracked source, and check the claim against the scanner rather than against intent.

Ref: DEF-2026-08-17-002.
