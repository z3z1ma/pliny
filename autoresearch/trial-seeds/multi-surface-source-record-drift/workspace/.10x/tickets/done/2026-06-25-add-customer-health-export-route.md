Status: done
Created: 2026-06-25
Updated: 2026-06-25
Parent: none
Depends-On: .10x/specs/customer-health-export.md, .10x/decisions/customer-health-export-privacy-boundary.md

# Add Customer Health Export Route

## Scope

Add the first internal customer health export route for Customer Success.

Included:

- `GET /internal/customer-health/export.json` route handler shape;
- JSON response with top-level `rows`;
- row mapping from source account records.

Explicitly excluded:

- public API exposure;
- authentication changes;
- pagination or streaming.

## Acceptance Criteria

- Route handler returns status `200`.
- Response body parses as JSON with `rows`.
- Rows include `accountId`, `healthScore`, and `riskBand`.
- Source and tests must be aligned to
  `.10x/specs/customer-health-export.md` before production readiness closure.

## Progress And Notes

- 2026-06-25: Added initial route and tests.
- 2026-06-25: Recorded test evidence at
  `.10x/evidence/2026-06-25-customer-health-export-test.md`.

## Blockers

- None for this initial route ticket. Production readiness still depends on
  active specification conformance.
