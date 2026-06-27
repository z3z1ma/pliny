Status: open
Created: 2026-06-25
Updated: 2026-06-25
Parent: .10x/tickets/2026-06-25-acme-status-label-parent.md
Depends-On: .10x/specs/acme-status-labels.md

# Add Paused Status Label

## Scope

Add display support for the `paused` account status label.

Included:

- Update `src/statusLabel.js` so `statusLabel("paused")` returns `Paused`.
- Update `src/statusLabel.test.js` to cover the paused status.

Excluded:

- Account lifecycle changes.
- Archived status changes.
- Unknown status behavior changes.

## Acceptance Criteria

- `statusLabel("paused")` returns `Paused`.
- Existing `active`, `archived`, and unknown status behavior still passes.
- `npm test` passes and evidence records the command output.

## Progress And Notes

- 2026-06-25: Ticket is executable and belongs to a child executor.

## Blockers

- None.
