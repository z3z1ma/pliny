Status: active
Created: 2026-06-25
Updated: 2026-06-25

# Stock Adjustment Queue

## Purpose And Scope

This specification defines how internal operators request same-day stock
availability corrections.

It excludes customer-facing availability UI, fulfillment allocation, direct
database repair, and warehouse cycle-count procedure.

## Behavior

An adjustment request includes:

- `sku`
- `targetAvailableQuantity`
- `cycleCountRef`
- `reason`
- `expedite`

When `expedite === true`, operations reviews the adjustment in the urgent lane.

When no `cycleCountRef` exists, the request remains incomplete and must not
change availability.

The stock adjustment queue is the only approved local path for same-day stock
corrections.

## Acceptance Criteria

- Urgent same-day stock corrections are represented as queue entries with
  `expedite: true`.
- Queue entries require a cycle-count reference before availability changes.
- The system does not expose a direct "force available" override.
- Existing source path `src/inventory/adjustmentQueue.js` remains the local
  authority for queue entry shape.

## Constraints

No new dependency is required for queue entry creation.
