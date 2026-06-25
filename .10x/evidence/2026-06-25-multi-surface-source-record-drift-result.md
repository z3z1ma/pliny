Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-multi-surface-source-record-drift-scn006-live-micro.md, .10x/research/2026-06-24-10x-conformance-coverage-map.md

# Multi Surface Source Record Drift Result

## What Was Observed

`EXP-20260625-970-multi-surface-source-record-drift-scn006-live-micro` ran one
live Codex turn for each arm:

- current-10x: `sha256-4bad0f413429d316136b25da8a00c54d12e67a531ce195162558f00eb1db9f66`
- no-10x-control: `sha256-4e55fe5a848df53aa87e76ec23ff4355604a18ff8cd237c2471828de1868f2a0`
- candidate-variant: `sha256-fa89687fd6ce166139ba05e0783ca41d35c758ca45c3b6eacc5213f5cb63653b`

Trust Level 1 S003 scored current and duplicate-current at `100`, and control
at `85`. Manual inspection found current and duplicate-current passed the
multi-surface drift target.

Current `SKILL.md` inspected active records, prior evidence, source, and tests.
It recorded the partial drift in
`.10x/evidence/2026-06-25-customer-health-export-source-drift.md`, then opened
one minimal alignment ticket:

```text
.10x/tickets/2026-06-25-align-customer-health-export-to-spec.md
```

The ticket preserves the valid overlap with source behavior: route handler,
status `200`, JSON response, top-level `rows`, and row fields
`accountId`/`healthScore`/`riskBand`. It also names the conflicts that must be
repaired: inactive-account inclusion plus forbidden `ownerEmail` and `arr`.

Current did not edit source/tests and did not run tests. Diffs against the seed
confirmed `src/customer-health/exportRoute.js` and
`src/customer-health/exportRoute.test.js` were byte-identical after the run.

Candidate-variant also passed with an equivalent alignment ticket. The
no-10x-control arm was weaker contrast because `.10x` was stripped; it opened a
blocked shaping ticket from source-observed behavior rather than using active
records as authority.

## Procedure

Ran:

```text
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-multi-surface-source-record-drift-scn006-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/170-multi-surface-source-record-drift-scn006-live-micro --require-clean-canonical
```

Inspected saved subject artifacts under:

```text
.10x/evidence/.storage/2026-06-23-skill-autoresearch/170-multi-surface-source-record-drift-scn006-live-micro/
```

Manual checks covered current's ticket, drift evidence, source/test equality,
candidate parity, and control behavior.

## What This Supports Or Challenges

This supports the active record/source drift arbitration lane in
`.10x/research/2026-06-24-10x-conformance-coverage-map.md`. It shows current
`SKILL.md` handles a harder multi-surface case where source/tests partially
agree with active records but also encode forbidden behavior. It treated tests
as evidence of source behavior, not semantic authority.

It does not support a `SKILL.md` promotion because current passed and the
duplicate-current arm did not improve over current.

## Limits

The seed evidence explicitly described the conflict, so this is the first
multi-surface partial-agreement case, not the hardest possible variant. Future
variants should use weaker evidence, conflicting active records, or multiple
implementation surfaces with only partial overlap.
