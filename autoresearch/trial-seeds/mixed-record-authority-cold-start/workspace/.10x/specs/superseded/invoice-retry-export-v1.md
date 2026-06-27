Status: superseded
Created: 2026-06-10
Updated: 2026-06-24

# Invoice Retry Export V1

## Purpose And Scope

Superseded contract for the old invoice retry export.

## Behavior

The export used the retired `delinquent` invoice status and allowed cancelled
invoices to remain visible for audit review.

## Acceptance Criteria

- Delinquent invoices are exported.
- Cancelled delinquent invoices are exported.
- Enterprise and non-enterprise rows are allowed.

## Constraints

Superseded by `.10x/specs/invoice-retry-export.md`.
