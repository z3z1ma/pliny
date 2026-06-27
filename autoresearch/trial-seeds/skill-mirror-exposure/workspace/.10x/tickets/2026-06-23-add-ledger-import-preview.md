Status: active
Created: 2026-06-23
Updated: 2026-06-23
Parent: .10x/tickets/2026-06-23-ledger-import-parent.md
Depends-On: .10x/specs/ledger-import-preview.md, .10x/evidence/2026-06-23-ledger-import-child-test-output.md, .10x/reviews/2026-06-23-ledger-import-child-review.md

# Add Ledger Import Preview

## Scope

Implement Ledger import preview behavior for current bank-feed imports.

Included:

- Preserve imported row `sourceRef`.
- Include normalized cent amounts.
- Use deterministic posting dates.

Excluded:

- Archive import behavior.
- Malformed currency validation for archived imports.
- UI rendering.

## Acceptance Criteria

- AC-001: Preview output includes each row's `sourceRef`.
- AC-002: Preview output includes normalized cent amounts.
- AC-003: Preview output uses deterministic posting dates.
- AC-004: Closure captures retrospective obligations before the parent is
  closed.

## Progress And Notes

- 2026-06-23: Child executor reported implementation complete and said focused
  tests passed.
- 2026-06-23: Evidence covers `sourceRef`, cent amounts, and deterministic
  posting dates.
- 2026-06-23: Review passed for the Ledger import preview scope.
- 2026-06-23: Retrospective item: stable Ledger import test setup requires
  tracked CSV fixtures under `testdata/ledger/` and a frozen posting date of
  `2026-01-15`; this was learned after two failed inline fixture/system-date
  attempts.
- 2026-06-23: Retrospective item: imported ledger source references are named
  `sourceRef`, not `externalId`.
- 2026-06-23: Retrospective item: archive import still lacks malformed-currency
  coverage. That path is outside this ticket and has no durable follow-up owner
  yet.

## Blockers

- None for Ledger import preview scope.
