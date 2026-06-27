Status: active
Created: 2026-06-25
Updated: 2026-06-25

# Customer Health Export Privacy Boundary

## Context

Customer Success needs an internal customer health export for renewal planning.
The initial implementation can support an internal JSON route, but the export
contains account health data and must avoid exposing owner contact details or
revenue fields until Privacy and Finance approve those surfaces.

## Decision

Customer health export is served through
`GET /internal/customer-health/export.json` and returns JSON rows for active
accounts only. Each row contains exactly `accountId`, `healthScore`, and
`riskBand`.

The export must not include `ownerEmail`, `arr`, billing contact data, or other
personally identifying or revenue fields unless a future decision supersedes
this one.

## Alternatives Considered

- Include owner email for Customer Success convenience: rejected because the
  export is shared broadly and owner contact data needs a privacy review.
- Include ARR for prioritization: rejected because Finance has not ratified
  revenue data exposure in this workflow.
- Export inactive accounts as well: rejected because the first production
  workflow is active-renewal planning.

## Consequences

The route can be productionized only after source and tests align to the active
privacy boundary. Future PII or revenue fields require a new decision that
explicitly supersedes this one.
