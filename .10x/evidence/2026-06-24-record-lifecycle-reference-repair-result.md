Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-record-graph-supersession-reference-repair-scn004-live-micro.md, autoresearch/candidates/2026-06-24-record-lifecycle-reference-repair.md

# Record Lifecycle Reference Repair Result Evidence

## What Was Observed

`EXP-20260624-908-record-graph-supersession-reference-repair-scn004-live-micro`
ran twice.

The initial run wrote artifacts under:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/108-record-graph-supersession-reference-repair-scn004-live-micro/`

Its `candidate-variant` arm was confounded because Codex returned a temporary
usage-limit failure before executing the turn. Manual inspection of the
`current-10x` arm still found strong selective record-reference repair.

The clean rerun wrote artifacts under:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/108b-record-graph-supersession-reference-repair-scn004-live-micro-rerun/`

The clean rerun scored:

- no-10x-control: `S002=60`
- current-10x: `S002=45`
- candidate-variant: `S002=45`

Manual inspection found:

- `current-10x` created a new active auto-approval decision at
  `.10x/decisions/finchpay-instant-payout-auto-approval-policy.md`.
- `current-10x` moved the prior manual-review decision to
  `.10x/decisions/superseded/finchpay-instant-payout-review-policy.md`.
- `current-10x` updated active spec/ticket links to the active decision,
  repointed historical review/evidence metadata to superseded records, and
  preserved historical research path mentions.
- `candidate-variant` also repaired live links and preserved historical path
  mentions.
- `candidate-variant` additionally cancelled the old shaping ticket and opened
  `.10x/tickets/2026-06-24-implement-finchpay-auto-approval-policy.md`, which
  was not needed for the requested record-graph repair.
- Both current and candidate left source files unchanged and did not run tests.

## Procedure

Commands:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-record-graph-supersession-reference-repair-scn004-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/108-record-graph-supersession-reference-repair-scn004-live-micro --require-clean-canonical
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-record-graph-supersession-reference-repair-scn004-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/108b-record-graph-supersession-reference-repair-scn004-live-micro-rerun --require-clean-canonical
```

Inspected:

- `report.md`
- subject final messages
- archived subject `.10x` file lists
- `rg` output over archived subject `.10x` records
- archived decision, spec, evidence, review, and ticket records
- archived subject source files using `diff -u` against the seed source

## What This Supports Or Challenges

Supports discarding
`candidate-record-lifecycle-reference-repair-v1` as null to slightly worse
versus current canonical `SKILL.md`.

## Limits

The clean rerun used one repetition. The scenario covers one decision
supersession with historical path mentions; it does not cover deletion or record
renaming more generally.
