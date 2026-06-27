Status: done
Created: 2026-06-25
Updated: 2026-06-25
Parent: none
Depends-On: .10x/specs/account-risk-summary-export.md, .10x/decisions/account-risk-summary-privacy-boundary.md

# Add Account Risk Summary Route

## Scope

Add the first internal account risk summary route for Success Operations.

Included:

- `GET /internal/account-risk/summary.json` route handler shape;
- JSON response with top-level `rows`;
- row mapping from source account records.

Explicitly excluded:

- public API exposure;
- authentication changes;
- pagination or streaming;
- production readiness sign-off.

## Acceptance Criteria

- Route handler returns status `200`.
- Response body parses as JSON with `rows`.
- Rows include account risk summary fields.
- Production readiness remains a separate step after active specification
  conformance is checked.

## Progress And Notes

- 2026-06-25: Added initial route and tests.
- 2026-06-25: Recorded pass evidence at
  `.10x/evidence/2026-06-25-account-risk-summary-test.md`.
- 2026-06-25: The initial ticket is complete for route shape only. Production
  readiness still needs a records/source/test conformance pass.

## Blockers

- None for this initial route-shape ticket.
