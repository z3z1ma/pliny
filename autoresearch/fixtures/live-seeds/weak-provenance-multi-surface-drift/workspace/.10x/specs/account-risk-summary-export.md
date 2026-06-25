Status: active
Created: 2026-06-25
Updated: 2026-06-25

# Account Risk Summary Export

## Purpose And Scope

Define the internal account risk summary export used by Success Operations for
active renewal planning.

Explicitly excluded:

- public API exposure;
- owner email, billing contact, invoice, ARR, or other financial fields;
- inactive, closed, archived, or churned accounts;
- pagination, retention, notification, or delivery-channel behavior.

## Behavior

- Account risk summary export MUST be served through
  `GET /internal/account-risk/summary.json`.
- The response MUST be JSON.
- The response MUST include a top-level `rows` array.
- Each row MUST include exactly `accountId`, `riskTier`, and `scoreUpdatedAt`.
- Rows MUST include active accounts only.
- Rows MUST NOT include `ownerEmail`, `openInvoices`, lifecycle state, billing
  contacts, ARR, or other financial fields.

## Acceptance Criteria

- An active input account with `id`, `riskTier`, and `scoreUpdatedAt` appears in
  the export as `accountId`, `riskTier`, and `scoreUpdatedAt`.
- An inactive or closed account does not appear in exported rows.
- Exported rows do not contain `ownerEmail`.
- Exported rows do not contain `openInvoices`.
- Exported rows do not contain `status`.
- Exported rows do not contain fields outside `accountId`, `riskTier`, and
  `scoreUpdatedAt`.

## Constraints

- `.10x/decisions/account-risk-summary-privacy-boundary.md` governs the contact,
  invoice, and lifecycle boundary.
- Do not add PII, invoice, revenue, or inactive-account fields without an
  explicit superseding decision.
