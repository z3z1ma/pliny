Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-external-artifact-status-dependent-repair-scn004-live-micro.md

# External Artifact Status Dependent Repair Result

## What Was Observed

`EXP-20260625-973-external-artifact-status-dependent-repair-scn004-live-micro`
ran three live Codex subject arms over the Atlas customer export external PRD
status-change fixture:

- no-10x-control:
  `sha256-26a7618aa973ff732d8c7c78622eecb30616e09b74386da0e0e6bfd18d8ab33f`
- current-10x:
  `sha256-bf009825242b2ffd5587eb15d1147bb65940c7b1ef3a3ad769e3b216f73db99b`
- candidate-variant duplicate current:
  `sha256-37ec28f917b7c1bfe4d7e4154a6533b55ca8f536c028b2495298cb9c500e2aa3`

The current-10x arm passed manual inspection:

- created one active revision B thin index at
  `.10x/specs/atlas-customer-export-prd.md`;
- moved revision A to
  `.10x/specs/superseded/atlas-customer-export-prd-rev-a.md`;
- preserved revision B provenance: source system, document id, canonical URL,
  observed status, revision, superseded revision, approval timestamp, export
  timestamp, local export path, and external-canonical statement;
- updated
  `.10x/tickets/2026-06-25-implement-atlas-customer-export.md`
  so active work depends on revision B and includes the `region` field;
- repointed
  `.10x/evidence/2026-06-25-atlas-customer-export-rev-a-evidence.md`
  to the superseded revision A spec path and preserved its limit that it does
  not prove revision B behavior;
- repointed
  `.10x/reviews/2026-06-25-atlas-customer-export-rev-a-review.md`
  to the superseded revision A spec path and preserved its revision-A-only
  verdict;
- left `src/export/atlasCustomerExport.js` unchanged versus the seed fixture;
- did not run tests or create implementation tickets.

The duplicate-current arm produced equivalent passing behavior.

The no-10x-control arm created active and superseded spec records, but because
control isolation removed the seeded `.10x` graph, it found no dependent
ticket/evidence/review records to repair.

Trust Level 1 heuristic scores were low for all arms: current S002=45,
duplicate-current S002=45, and no-10x-control S002=55. Manual inspection is
authoritative for this result.

## Procedure

1. Created the seed workspace under
   `autoresearch/trial-seeds/external-artifact-status-dependent-repair/`.
2. Registered
   `.10x/research/2026-06-25-external-artifact-status-dependent-repair-scn004-live-micro.md`.
3. Ran:
   `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-external-artifact-status-dependent-repair-scn004-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/173-external-artifact-status-dependent-repair-scn004-live-micro --require-clean-canonical`
4. Inspected the generated `report.md`, `summary.json`, `plan.json`, last
   messages, current/candidate subject records, and `diff -qr` source checks.

Raw artifacts:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/173-external-artifact-status-dependent-repair-scn004-live-micro/`

## What This Supports Or Challenges

This supports the conclusion that current `SKILL.md` handles exported external
artifact status/revision maintenance plus dependent-record repair. It extends
prior stale thin-index coverage by verifying that active tickets move to the
new canonical revision while old evidence and reviews remain historical.

## Limits

This still uses exported files, not a live Google Docs connector refresh. The
prompt explicitly named the desired active path and repair intent, so future
variants can reduce assistance.
