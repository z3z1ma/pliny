Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: .10x/tickets/2026-06-23-ledger-import-parent.md
Depends-On: .10x/specs/ledger-import-preview.md

# Add Ledger Import Preview

## Scope

Implement and verify the Ledger import preview fixture behavior described by
`.10x/specs/ledger-import-preview.md`.

## Acceptance Criteria

- Preview import tests replay tracked CSV fixtures.
- Expected posting date is frozen.
- Preview output uses `sourceRef`.

## Progress And Notes

- 2026-06-23: Child executor reported completion.
- 2026-06-23: Evidence and review passed for the child scope.
- 2026-06-23: During execution, repeated fixture replay friction surfaced as a
  reusable operational procedure.

## Blockers

None.
