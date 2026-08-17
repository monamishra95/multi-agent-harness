# Contract schemas (spec Part 2)

Authoritative definitions live in `../docs/PROTOCOL.md` Part 2. This directory holds copy-paste templates:

| File | Producer → Consumer | Spec section |
|---|---|---|
| `envelope.yaml` | every agent → everyone | §2 preamble |
| `acceptance.yaml` | the operator/orchestrator → all | §2.1 |
| `factsheet.json` | Scout → Builder, Verifier | §2.2 |
| `claims.json` | Builder → Verifier | §2.3 |
| `verification-report.json` | Verifier → orchestrator, Librarian | §2.4 |
| `redteam-score.json` | Red-team → orchestrator, Librarian | §2.5 |

Contract violations are P-class defects. Schema changes bump `schema_version` and are Librarian-gated.
