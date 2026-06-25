Status: active
Created: 2026-06-25
Updated: 2026-06-25

# Payout Export CSV

## Purpose And Scope

Defines the completed payout CSV export behavior. The implementation ticket is
`.10x/tickets/2026-06-25-align-payout-export-csv.md`.

## Behavior

The payout export includes settled payout rows only, emits `payoutId`,
`accountId`, `settledAt`, `amountCents`, and `currency`, and excludes pending
or failed payouts.

## Acceptance Criteria

- Ticket `.10x/tickets/2026-06-25-align-payout-export-csv.md` is done.
- Evidence for `.10x/tickets/2026-06-25-align-payout-export-csv.md` proves
  pending and failed payouts are excluded.
- Review for `.10x/tickets/2026-06-25-align-payout-export-csv.md` has pass
  verdict and no unresolved export-shape concerns.

## Constraints

The record-maintenance task must not change CSV behavior.
