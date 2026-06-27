Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Audit Export API Route

## Purpose And Scope

Define the operator audit export API after the CSV-only contract was
superseded.

## Behavior

- Audit export MUST be served through `GET /internal/audit/export.json`.
- The response MUST be JSON.
- Each row MUST include `eventId`, `actor`, and `action`.
- Internal diagnostic events MUST be filtered out.

## Acceptance Criteria

- `GET /internal/audit/export.json` returns JSON rows with `eventId`, `actor`,
  and `action`.
- Internal diagnostic events do not appear in exported rows.
- No HTTP API route exists for audit export.

## Constraints

- `.10x/specs/superseded/audit-export-csv-only.md` preserves the old CSV-only
  contract.
- `.10x/decisions/audit-export-api-route.md` owns the API route authority.
