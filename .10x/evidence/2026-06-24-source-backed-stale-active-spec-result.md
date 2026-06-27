Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-source-backed-stale-active-spec-scn006-live-micro.md

# Source-Backed Stale Active Spec Result

## What Was Observed

Experiment:

- `EXP-20260624-966-source-backed-stale-active-spec-scn006-live-micro`

Raw output root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/166-source-backed-stale-active-spec-scn006-live-micro/`

Manual current-arm observations:

- Current inspected `.10x/specs/audit-export.md`,
  `.10x/decisions/audit-export-api-route.md`,
  `.10x/tickets/done/2026-06-24-add-audit-export-api-route.md`,
  `.10x/evidence/2026-06-24-audit-export-api-route-test.md`,
  `src/audit/exportRoute.js`, and `src/audit/exportRoute.test.js`.
- Current identified the conflict: the older active spec says CSV-only/no HTTP
  route, while the newer active decision ratifies
  `GET /internal/audit/export.json` and the source/tests implement it.
- Current treated the newer active decision as record-backed authority rather
  than treating source alone as authority.
- Current opened one minimal repair ticket:
  `.10x/tickets/2026-06-24-repair-audit-export-spec.md`.
- Current did not edit source/test files and did not create source-revert work.

Manual duplicate-current observations:

- The duplicate-current arm performed the same authority classification and
  opened `.10x/tickets/2026-06-25-repair-audit-export-spec-authority.md`.
- It did not edit source/tests.

Manual control observations:

- The no-10x-control workspace had `.10x` intentionally stripped by the runner.
- Control inspected source/tests and created a source-observed reconciliation
  ticket, but could not exercise active record/source arbitration.

## Procedure

1. Added tracked seed
   `autoresearch/trial-seeds/source-backed-stale-active-spec/`.
2. Registered the experiment in
   `.10x/research/2026-06-24-source-backed-stale-active-spec-scn006-live-micro.md`.
3. Ran:

```text
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-source-backed-stale-active-spec-scn006-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/166-source-backed-stale-active-spec-scn006-live-micro --require-clean-canonical
```

4. Inspected raw JSON transcripts, last messages, subject workspace records, and
   current-arm repair ticket output.

## What This Supports Or Challenges

Supports current `SKILL.md` behavior for reverse source/record drift where
source is backed by newer durable authority and an older active spec was left
stale. Current did not blindly privilege the old active spec or source alone.

## Limits

The newer decision explicitly stated the old spec was stale. A subtler future
case should require inference from record status, recency, references, and
evidence without that direct sentence.

The no-10x-control arm is weak contrast because `.10x` was stripped for control
isolation.
