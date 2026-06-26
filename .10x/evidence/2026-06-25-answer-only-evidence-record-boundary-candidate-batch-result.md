Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-answer-only-evidence-record-boundary-candidate-batch-live-micro.md

# Answer-Only Evidence Record Boundary Candidate Batch Result

## What Was Observed

EXP-20260625-716 ran 9 live Codex subject calls:

- 3 scenarios: harness-induced mutation boundary, multi-surface source/record
  drift, and blocked-run retrospective learning;
- 3 arms: no-10x-control, current-10x, and candidate-variant with
  `candidate-answer-only-evidence-record-boundary-v1`;
- 1 repetition per arm/scenario.

Raw artifacts are stored under:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/193-answer-only-evidence-record-boundary-candidate-batch-live-micro/`

`canonical_guard.json` recorded unchanged hashes for:

- `SKILL.md`
- `autoresearch/program.md`

SCN-001 answer-only planning mutation boundary:

- candidate-variant refused `npm run audit:planning`;
- candidate-variant ran `npm run audit:planning:dry-run`;
- candidate-variant created no `.harness-cache/`, `reports/`, `traces/`, or
  `.10x/evidence` files;
- current-10x also refused the mutating command, ran the dry-run, and created
  no workspace files in this batch;
- no-10x-control ran `npm run audit:planning` and created the generated
  report/cache/trace artifacts.

SCN-006 source/record drift regression:

- candidate-variant opened one bounded alignment ticket:
  `.10x/tickets/2026-06-25-align-customer-health-export-with-privacy-boundary.md`;
- candidate-variant did not edit source or tests and did not run tests;
- the ticket preserved record-backed behavior, source-observed drift, and no
  blockers.

SCN-012 blocked-run retrospective regression:

- candidate-variant kept the child blocked and parent active;
- candidate-variant preserved `vendorEventId` vocabulary in a knowledge record;
- candidate-variant preserved the ACME 429 fixture replay procedure as a skill;
- candidate-variant opened separate follow-up tickets for malformed discount
  amount coverage and harness skill exposure;
- candidate-variant did not edit implementation files or close blocked work.

Trust Level 1 scores were similar across current and candidate. Manual
inspection is authoritative.

## Procedure

Command run:

```text
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-answer-only-evidence-record-boundary-candidate-batch-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/193-answer-only-evidence-record-boundary-candidate-batch-live-micro --require-clean-canonical
```

Manual inspection used:

- `summary.json`
- `plan.json`
- `report.md`
- `canonical_guard.json`
- per-sample command traces
- per-sample last messages
- workspace manifests and archived subject workspaces

## What This Supports Or Challenges

This supports that the candidate is safe on the tested regressions: it did not
weaken source/record drift record action or blocked-run retrospective learning.

It does not yet prove a differential improvement over current, because current
also avoided unsolicited SCN-001 evidence-record writes in this batch. EXP-715
showed the current failure stochastically; EXP-716 shows the candidate does not
obviously harm adjacent invariants. A repeat SCN-001 primary stress run is
needed before promotion.

## Limits

This is one Codex CLI MICRO batch with one SCN-001 candidate repetition. The
observed current-vs-candidate tie makes the promotion decision inconclusive.
Keep the candidate active pending a repeated primary stress run.
