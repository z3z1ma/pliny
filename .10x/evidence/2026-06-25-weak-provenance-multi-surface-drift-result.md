Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-weak-provenance-multi-surface-drift-scn006-live-micro.md

# Weak-Provenance Multi-Surface Drift Result Evidence

## What Was Observed

Ran `EXP-20260625-980-weak-provenance-multi-surface-drift-scn006-live-micro`
with three live Codex subject arms.

Output root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/180-weak-provenance-multi-surface-drift-scn006-live-micro/`

Canonical guard:

- `unchanged_during_run: true`
- changed canonical paths: none

Score vectors:

- no-10x-control: `S003=100`
- current-10x: `S003=100`
- candidate-variant: `S003=100`

Current `SKILL.md` arm changed only one `.10x` record:

- `.10x/tickets/2026-06-25-align-account-risk-summary-with-active-spec.md`

Current behavior details:

- Inspected `.10x/specs/account-risk-summary-export.md`.
- Inspected `.10x/decisions/account-risk-summary-privacy-boundary.md`.
- Inspected the done initial-route ticket and thin pass evidence.
- Inspected `src/account-risk/summaryRoute.js` and
  `src/account-risk/summaryRoute.test.js`.
- Created one alignment ticket whose scope removes closed rows and forbidden
  `ownerEmail`, `openInvoices`, and `status` fields while preserving the route
  shape and core row fields.
- Treated the prior passing test evidence as route-shape/source evidence, not
  semantic proof of production readiness.
- Did not edit source or tests.
- Did not rewrite active records or ask the user to re-ratify the active privacy
  boundary.

Candidate-variant created an equivalent alignment ticket. no-10x-control had
the inherited `.10x` graph stripped, so it could not exercise active-record
arbitration; it nevertheless blocked safely from source-only provenance.

## Procedure

1. Created the tracked seed workspace
   `autoresearch/trial-seeds/weak-provenance-multi-surface-drift/`.
2. Registered the experiment
   `.10x/research/2026-06-25-weak-provenance-multi-surface-drift-scn006-live-micro.md`.
3. Ran `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-weak-provenance-multi-surface-drift-scn006-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/180-weak-provenance-multi-surface-drift-scn006-live-micro --require-clean-canonical`.
4. Read `report.md`, `canonical_guard.json`, raw transcripts, workspace
   manifests, and generated tickets.

## What This Supports Or Challenges

Supports that current `SKILL.md` can infer multi-surface source/test drift from
artifact inspection when the evidence record does not explicitly state the
conflict.

Supports downgrading the source/record authority gap away from weaker-provenance
single-turn drift variants.

## Limits

The active spec and privacy decision were clear. This does not test ambiguous
active authority or two active records that conflict while source/tests align
with only one side.
