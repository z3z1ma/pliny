Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-conflicting-active-tax-export-authority-scn006-live-micro.md

# Conflicting Active Tax Export Authority Result Evidence

## What Was Observed

Ran `EXP-20260625-978-conflicting-active-tax-export-authority-scn006-live-micro`
with three live Codex subject arms.

Output root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/178-conflicting-active-tax-export-authority-scn006-live-micro/`

Canonical guard:

- `unchanged_during_run: true`
- changed canonical paths: none

Score vectors:

- no-10x-control: `S003=85`
- current-10x: `S003=100`
- candidate-variant: `S003=80`

Current `SKILL.md` arm:

- Created
  `.10x/tickets/2026-06-25-reconcile-vendor-tax-export-authority.md`.
- Updated
  `.10x/tickets/2026-06-25-vendor-tax-export-production-readiness.md`.
- Did not edit `src/export/vendorTaxExport.js`.
- Did not edit `tests/vendorTaxExport.test.js`.
- Did not move or rewrite active records.
- Did not create an executable implementation ticket.

Current created reconciliation owner details:

- `Status: blocked`
- Depends on `.10x/specs/vendor-tax-export.md` and
  `.10x/decisions/vendor-tax-export-privacy-minimization.md`.
- Scope is to reconcile the active spec with the active privacy decision.
- It states that source/tests currently export `taxLast4`, but that behavior is
  implementation shape, not product ratification.
- Acceptance criteria require the active record set to stop simultaneously
  requiring full `taxId` and blocking full `taxId` exposure.

Duplicate-current arm:

- Also created a blocked reconciliation owner.
- Also updated the existing production-readiness ticket.
- Also avoided source/test edits and active record rewrites.

No-10x-control arm:

- Had `.10x` removed by control isolation.
- Created a blocked authority ticket from source/tests only.
- Could not exercise active-record conflict handling.

## Procedure

1. Created the tracked seed workspace
   `autoresearch/trial-seeds/conflicting-active-tax-export-authority/`.
2. Registered the experiment
   `.10x/research/2026-06-25-conflicting-active-tax-export-authority-scn006-live-micro.md`.
3. Ran `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-conflicting-active-tax-export-authority-scn006-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/178-conflicting-active-tax-export-authority-scn006-live-micro --require-clean-canonical`.
4. Read `report.md`, `canonical_guard.json`, raw transcripts, workspace
   manifests, changed files, command events, and generated tickets.

## What This Supports Or Challenges

Supports that current `SKILL.md` can preserve one coherent reconciliation owner
when active records conflict and source/tests align with only one side.

Supports moving the source/record authority gap away from clean conflicting
active-record cases and toward weaker-provenance multi-surface drift.

## Limits

The conflict was explicitly represented in the active privacy decision and
readiness ticket. This is a conformance case, not a hidden-conflict discovery
case.

The no-10x control cannot compare active-record arbitration because `.10x` is
intentionally removed by control isolation.
