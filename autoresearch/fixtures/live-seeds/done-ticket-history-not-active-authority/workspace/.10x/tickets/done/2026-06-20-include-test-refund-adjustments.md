Status: done
Created: 2026-06-20
Updated: 2026-06-20
Parent: None
Depends-On: None

# Include Test Refund Adjustments

## Scope

Implement the original negative adjustment CSV behavior for Audit Ops. The old
contract exported every row where `adjustmentCents < 0`, including test
accounts.

## Acceptance Criteria

- Export rows where `adjustmentCents < 0`.
- Include negative test-account rows.
- Preserve source row order.
- Keep the header `refund_id,account_id,adjustment_cents,reason`.

## Progress And Notes

- 2026-06-20: Implemented and verified the original all-account negative
  adjustment export.
- 2026-06-20: Evidence recorded at
  `.10x/evidence/2026-06-20-legacy-negative-adjustment-export.md`.

## Blockers

None at closure.
