Status: active
Created: 2026-06-25
Updated: 2026-06-25

# Account Risk Summary Privacy Boundary

## Context

Success Operations needs a compact internal account risk summary before the
renewal planning meeting. The export will be shared outside the core account
team, so contact details and financial exposure remain out of scope until Legal
and Finance ratify them.

## Decision

The account risk summary is served through
`GET /internal/account-risk/summary.json` and returns active customer accounts
only.

Each row contains exactly `accountId`, `riskTier`, and `scoreUpdatedAt`.

The summary must not include `ownerEmail`, `openInvoices`, ARR, billing contact
fields, lifecycle state, or inactive/closed accounts unless a future decision
explicitly supersedes this one.

## Alternatives Considered

- Include `ownerEmail` for Success convenience: rejected because broad internal
  sharing needs Legal review before account owner contact data is exposed.
- Include `openInvoices` to explain risk: rejected because Finance has not
  approved invoice exposure in this workflow.
- Include inactive and closed accounts for historical comparison: rejected
  because this production path is scoped to active renewal planning.

## Consequences

Production readiness depends on source and tests conforming to the active
privacy and lifecycle boundary. Future contact, invoice, revenue, or inactive
account exposure requires a superseding decision.
