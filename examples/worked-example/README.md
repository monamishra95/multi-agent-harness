# Worked example — vendor pricing comparison

A realistic build contract, showing the level of specificity the harness expects before a build starts.

- [`spec.md`](spec.md) — intent, goals, non-goals, audience, tier, build mode, plus explicit research constraints
- [`acceptance.yaml`](acceptance.yaml) — seven machine-verifiable criteria, zero manual

## Why this example

Pricing comparison is deliberately mundane and deliberately fact-dense: it's the kind of artifact where being wrong is embarrassing and being verifiable is the entire value. That makes it a good demonstration of what the harness is *for*, and a poor demonstration of what it isn't for (nothing here is creative or exploratory).

## What to notice

**The intent explains a decision, not a deliverable.** "They need a single page so the pricing debate argues about strategy instead of whose recollection is right" tells the agents what a good outcome looks like. "Build a pricing comparison page" would not.

**Non-goals do real work.** Excluding a recommendation and excluding analyst figures both narrow the build in ways that prevent predictable failures — scope creep into strategy, and untraceable numbers.

**Criteria are observable, not evaluative.** Compare AC-3 ("vendors with no published enterprise price display 'not published' rather than any number") with a criterion like "the page is accurate." The first can fail a build; the second can only start an argument.

**Unknowns are specified in advance.** The spec tells Scout what to do when a price isn't published, before the situation arises. Most fabrication happens in exactly that gap.

## Running it

This example ships as a contract only — there's no built artifact, because the useful part is the contract. To try it end to end, copy both files into an empty project, install the harness, and run `/build`. Expect Scout to return several `unknowns`; enterprise pricing is frequently quote-based, and an agent that reports that honestly is behaving correctly.
