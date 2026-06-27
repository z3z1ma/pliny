Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Target: .10x/specs/audit-export.md
Verdict: fail

# Audit Export Record Repair Needed

## Target

`.10x/specs/audit-export.md`

## Findings

- significant: the active spec still says no HTTP API route may exist.
- significant: the active decision and source/tests now require
  `GET /internal/audit/export.json`.
- minor: historical notes that mention the old CSV-only spec should remain as
  history when the spec is moved or superseded.

## Verdict

Fail until the record graph is repaired.

## Residual Risk

Future agents may create source-revert work if the stale spec remains active.
