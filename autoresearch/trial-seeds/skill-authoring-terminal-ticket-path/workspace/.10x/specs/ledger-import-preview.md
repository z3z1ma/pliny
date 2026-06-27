Status: active
Created: 2026-06-23
Updated: 2026-06-23

# Ledger Import Preview

## Purpose And Scope

Defines preview behavior for Ledger CSV imports. Archive import behavior is out
of scope for this specification.

## Behavior

Given a tracked Ledger CSV fixture and a frozen posting date of `2026-01-15`,
when the preview import runs, then each preview row exposes `sourceRef`,
normalized cent amount, and the frozen posting date.

## Acceptance Criteria

- Preview tests use tracked CSV fixture files rather than inline CSV strings.
- Preview output uses `sourceRef`, not `externalId`.
- Posting-date expectations do not depend on the current system date.

## Constraints

Archive malformed-currency coverage belongs to a separate follow-up.
