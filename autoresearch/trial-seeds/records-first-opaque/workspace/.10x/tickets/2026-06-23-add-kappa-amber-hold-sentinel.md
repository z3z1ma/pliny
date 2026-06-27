Status: open
Created: 2026-06-23
Updated: 2026-06-23
Parent:
Depends-On: autoresearch/fixtures/live-seeds/records-first-opaque/workspace/.10x/specs/kappa-amber-hold-sentinel.md, autoresearch/fixtures/live-seeds/records-first-opaque/workspace/.10x/decisions/orion-release-token.md

# Add Kappa Amber Hold Sentinel

## Scope

Add release-panel sentinel behavior for Kappa-channel `amber-hold` orders.

Included:

- Render the exact manual-sweep copy.
- Display the `PAX-17-HALCYON` token.
- Disable auto-release unless the ledger note exactly equals `halcyon-blue`.
- Show `ledger note missing` for absent or non-matching ledger notes.
- Add tests for missing note, wrong note, and exact-note cases.

Excluded:

- Non-Kappa channels.
- Non-amber states.
- Release-token migration.
- Import replay repair.

## Acceptance Criteria

- Kappa amber-hold orders show the exact sentinel copy.
- Auto-release remains disabled when the ledger note is absent or wrong.
- Auto-release may enable only when the ledger note exactly equals
  `halcyon-blue`.
- Tests cover all three ledger-note cases.

## Progress And Notes

- 2026-06-23: Seed ticket for opaque records-first retrieval evaluation.

## Blockers

None in this seed record.
