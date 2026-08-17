# Tests

## `seeded_defects.py`

Plants known defects in a throwaway project and measures whether the gates catch them. This is how the harness tests its central claim — that the gates block bad work — instead of asserting it.

```bash
python tests/seeded_defects.py       # scorecard
python tests/seeded_defects.py -v    # plus each check's raw output
```

**Six planted defects**, one per class the automated checks cover: a Google API key in client source, a private key block, a hardcoded credential, committed build artifacts, template placeholder text in a shipped README, and an uncited figure in prose.

**Two controls** that must *not* fire: a placeholder credential in `.env.example` (the sanctioned convention) and a figure carrying a visible source link. False positives matter as much as misses — a check that cries wolf trains its operator to ignore it, which is worse than having no check.

Fixtures are generated at runtime in a temp directory and deleted afterward. Secret-shaped payloads are assembled from fragments so they never exist contiguously in tracked source (see `defects/DEF-2026-08-17-002.yaml` for why that lesson was earned rather than assumed).

## What this test found on its first run

Two real defects in the harness itself, both now logged in `defects/`:

- **DEF-2026-08-17-001** — the citation lint silently missed *every* percentage, because its regex required a word boundary after `%`. It had been reporting "clean" on documents containing uncited figures.
- **DEF-2026-08-17-002** — the test's own fixtures tripped the repository's secret scan, turning the release gate red.

That's the honest argument for this file: the first thing it did was prove one of the shipped checks didn't work.

## What this test does not cover

Three gates need an agent, not a script, and a green run here says nothing about them:

- **G1 fact audit** — whether a figure is *true* requires re-fetching a primary source.
- **G4 judgment** — whether a claim is defensible under hostile review.
- **Fresh context** — whether Verifier and Red-team actually ran uncontaminated by the build reasoning.

A green run means the automated gates work. It does not mean the harness works; that requires running a real project end to end through the loop.

## Adding a case

Append a tuple to `CASES`: `(id, defect_class, description, {path: content}, check_script, extra_args, should_detect)`. When a defect escapes in real use, add the case that would have caught it — that's the regression artifact the defect-routing protocol requires before a record can be closed.
