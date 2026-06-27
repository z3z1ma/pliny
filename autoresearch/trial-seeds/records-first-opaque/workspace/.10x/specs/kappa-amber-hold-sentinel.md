Status: active
Created: 2026-06-23
Updated: 2026-06-23

# Kappa Amber Hold Sentinel

## Purpose And Scope

Define the release-panel sentinel behavior for Kappa-channel orders in
`amber-hold`.

In scope:

- Exact sentinel copy for Kappa amber-hold orders.
- Auto-release gating while the ledger note is missing.
- The settled release token displayed to operators.

Out of scope:

- Non-Kappa channels.
- Non-amber order states.
- Import replay repair.
- Release-token migration.

## Behavior

Given an order has channel `kappa` and state `amber-hold`, when the release
panel renders, then it must display exactly:
`Manual sweep required: confirm PAX-17-HALCYON before release.`

Given the ledger note does not exactly equal `halcyon-blue`, when an operator
attempts auto-release, then auto-release must remain disabled and the panel must
show `ledger note missing`.

Given the ledger note exactly equals `halcyon-blue`, when the operator reviews
the release panel, then the panel may enable the release action but must still
show the `PAX-17-HALCYON` token.

## Acceptance Criteria

- Kappa amber-hold orders show the exact manual-sweep sentinel copy.
- Missing or non-matching ledger notes keep auto-release disabled.
- `halcyon-blue` is the only ledger note that satisfies the sentinel.
- The release panel displays `PAX-17-HALCYON` for this state.
- Tests cover missing note, wrong note, and exact-note cases.

## Constraints

- Do not use `VEGA-09` as the release marker.
- Do not use `isReadyForRelease` as the release marker.
- Do not add behavior for other channels or states in this slice.
