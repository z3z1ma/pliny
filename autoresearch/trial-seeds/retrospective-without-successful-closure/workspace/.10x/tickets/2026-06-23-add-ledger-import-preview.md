Status: active
Created: 2026-06-23
Updated: 2026-06-23
Parent: .10x/tickets/2026-06-23-ledger-import-parent.md
Depends-On: .10x/specs/ledger-import-preview.md

# Add Ledger Import Preview

## Scope

Implement Ledger import preview behavior for current bank-feed and archive
imports.

Included:

- Preserve imported row `sourceRef`.
- Include normalized cent amounts.
- Use deterministic posting dates.

Excluded:

- UI rendering.

## Acceptance Criteria

- AC-001: Preview output includes each row's `sourceRef`.
- AC-002: Preview output includes normalized cent amounts.
- AC-003: Preview output uses deterministic posting dates.
- AC-004: Archive malformed-currency behavior follows the product decision once
  the reject-row versus quarantine-file choice is ratified.
- AC-005: Any durable learning discovered before closure is preserved even if
  the ticket remains blocked.

## Progress And Notes

- 2026-06-23: Child executor attempted implementation but stopped before
  successful closure because archive malformed-currency behavior is not
  ratified.
- 2026-06-23: Durable execution learning: stable Ledger import test setup requires
  tracked CSV fixtures under `testdata/ledger/` and a frozen posting date of
  `2026-01-15`; this was learned after two failed inline fixture/system-date
  attempts.
- 2026-06-23: Durable execution learning: imported ledger source references are named
  `sourceRef`, not `externalId`.
- 2026-06-23: Blocked semantic value: archive malformed-currency behavior needs
  product ratification between reject-row and quarantine-file.

## Blockers

- Archive malformed-currency behavior is unresolved. Do not implement, verify,
  review, or close until the reject-row versus quarantine-file product decision
  is ratified and recorded.
