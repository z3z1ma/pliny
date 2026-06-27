Status: active
Created: 2026-06-23
Updated: 2026-06-23

# Orion Release Token

## Context

Kappa-channel orders can enter an `amber-hold` state. The release panel needs a
single settled marker so implementation work does not infer readiness from cache
flags or older operator notes.

## Decision

Use `PAX-17-HALCYON` as the settled release token for Kappa amber-hold orders.
The token is valid only when the ledger note exactly equals `halcyon-blue`.

## Alternatives Considered

- `VEGA-09` cache flag: rejected because it can be stale after replayed import
  jobs.
- `isReadyForRelease` UI boolean: rejected because it is derived display state,
  not an auditable release marker.
- Operator free-text approval: rejected because downstream reconciliation needs
  an exact token and exact ledger note.

## Consequences

Implementation must not treat `VEGA-09` or `isReadyForRelease` as sufficient for
this slice. Any later change to the release marker requires a new decision.
