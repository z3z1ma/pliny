Status: done
Created: 2026-06-10
Updated: 2026-06-10
Parent: None
Depends-On: .10x/specs/superseded/invoice-retry-export-v1.md

# Include Cancelled Invoice Retries

## Scope

Prototype cancelled-invoice visibility in the old retry export.

## Acceptance Criteria

- Delinquent cancelled invoices appear in the CSV.
- Delinquent active invoices appear in the CSV.
- Header remains `invoice_id,account_id,amount_cents`.

## Progress And Notes

- 2026-06-10: Prototype completed against the superseded V1 spec.

## Blockers

None at closure. This ticket is historical and terminal.
