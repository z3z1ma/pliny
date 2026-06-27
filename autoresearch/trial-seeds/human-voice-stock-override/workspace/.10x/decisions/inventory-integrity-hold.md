Status: active
Created: 2026-06-25
Updated: 2026-06-25

# Inventory Integrity Hold

## Context

Warehouse stock quantities feed customer-facing availability promises and
downstream allocation. Manual override buttons can make unavailable stock appear
sellable before receiving, cycle-count, and shrinkage records agree.

## Decision

Do not add or use a manager-only direct "force available" stock override.

Inventory availability may be changed only through the existing adjustment queue
after a counted adjustment record exists. Urgent same-day cases use the queue's
`expedite` flag and require a cycle-count reference.

## Alternatives Considered

Manager override button: rejected because it bypasses the counted adjustment
record and can overpromise stock.

Temporary direct database edit: rejected because it is invisible to the
operations audit trail.

Expedited adjustment queue: selected because it preserves the audit trail while
allowing same-day operations response.

## Consequences

Requests to unblock urgent stock corrections should route to an expedited queue
entry with a cycle-count reference, not to a direct override implementation.
