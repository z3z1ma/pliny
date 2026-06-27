Status: superseded
Created: 2026-06-10
Updated: 2026-06-24

# Invoice Retry Window V1

## Context

The old retry queue used a two-attempt review window and treated cancelled
invoices as audit-visible.

## Decision

Use the retired `delinquent` status and include invoices with
`retryAttemptCount <= 2`, including cancelled invoices.

## Alternatives Considered

Overdue-only export: rejected at the time because the current invoice source had
not migrated yet.

## Consequences

This decision is superseded. Do not use it as current authority.
