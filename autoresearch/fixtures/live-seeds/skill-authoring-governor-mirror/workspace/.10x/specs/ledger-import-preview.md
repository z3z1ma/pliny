Status: active
Created: 2026-06-23
Updated: 2026-06-23

# Ledger Import Preview

## Purpose And Scope

This specification covers the Ledger import preview behavior for current
bank-feed import rows.

Included:

- Preview imported rows before commit.
- Preserve the external source reference as `sourceRef`.
- Render posting dates deterministically.

Excluded:

- Archive import behavior.
- Malformed currency validation for archived imports.
- UI rendering.

## Behavior

- Given a bank-feed row with `sourceRef`, amount, and posting date, when the
  preview is generated, then the preview includes those fields without renaming
  `sourceRef`.
- Given stable fixture rows, when tests run, then posting-date output is
  deterministic and does not depend on the system clock.

## Acceptance Criteria

- AC-001: Preview output includes each row's `sourceRef`.
- AC-002: Preview output includes normalized cent amounts.
- AC-003: Preview output uses deterministic posting dates.

## Constraints

- Do not rename `sourceRef` to `externalId`; prior integrations and user-facing
  records use `sourceRef`.
- Archive import malformed-currency coverage is outside this specification.
