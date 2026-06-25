Status: active
Created: 2026-06-25
Updated: 2026-06-25

# Customer Health Export

## Purpose And Scope

Define the internal customer health export used by Customer Success for active
renewal planning.

Explicitly excluded:

- public API exposure;
- owner email, billing contact, ARR, or revenue fields;
- inactive, archived, or churned accounts;
- pagination, retention, or notification behavior.

## Behavior

- Customer health export MUST be served through
  `GET /internal/customer-health/export.json`.
- The response MUST be JSON.
- The response MUST include a top-level `rows` array.
- Each row MUST include exactly `accountId`, `healthScore`, and `riskBand`.
- Rows MUST include active accounts only.
- Rows MUST NOT include `ownerEmail`, `arr`, billing contacts, or revenue data.

## Acceptance Criteria

- An active input account with `id`, `healthScore`, and `riskBand` appears in
  the export as `accountId`, `healthScore`, and `riskBand`.
- An inactive account does not appear in exported rows.
- Exported rows do not contain `ownerEmail`.
- Exported rows do not contain `arr`.
- Exported rows do not contain fields outside `accountId`, `healthScore`, and
  `riskBand`.

## Constraints

- `.10x/decisions/customer-health-export-privacy-boundary.md` governs the
  privacy and revenue-field boundary.
- Do not add PII or revenue fields without an explicit superseding decision.
