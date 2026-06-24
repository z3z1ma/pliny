Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Server-Owned Billing Exports

## Context

Billing exception CSV exports are used by finance operations. Client-side CSV
assembly previously drifted from backend totals and produced inconsistent
column ordering.

## Decision

Billing exception CSV export formatting is server-owned. The UI may trigger a
download but must not assemble CSV rows or decide the export schema.

## Alternatives Considered

- Client-side export: faster to wire but duplicates schema and risks mismatched
  finance output.
- Shared client/server formatter: still exposes schema ownership to UI code and
  complicates deployment.

## Consequences

Implementation belongs in `src/features/billing/exportPricingExceptions.ts`.
Tests must verify server formatter output. UI changes are out of scope unless a
separate ticket explicitly owns the download trigger.
