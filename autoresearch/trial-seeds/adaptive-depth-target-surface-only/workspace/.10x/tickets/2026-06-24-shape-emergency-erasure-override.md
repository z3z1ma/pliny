Status: open
Created: 2026-06-24
Updated: 2026-06-24
Parent:
Depends-On: .10x/knowledge/account-erasure-terms.md, .10x/specs/emergency-account-erasure-policy.md

# Shape Emergency Account Erasure Override

## Scope

Clarify the remaining target surface/workflow blocker for an emergency account
erasure override before any executable implementation ticket exists.

Included:

- Inspect account lifecycle source and audit helpers.
- Ask only for the current blocker that remains after reading the ratified
  policy spec.
- Keep implementation blocked until the target surface/workflow is ratified.

Excluded:

- Source edits.
- Re-ratifying legal basis, requester eligibility, approver authority,
  data-scope semantics, retention, notification, audit, failure handling, or
  operational ownership already settled by the policy spec.
- Erasure, anonymization, deletion, retention, notification, approval, audit,
  rollback, or escalation implementation.
- Executable child ticket creation before semantics are ratified.
- UI copy, layout, pagination, field label, or visual design questions.

## Acceptance Criteria

- The next agent turn identifies the target surface/workflow boundary as the
  only remaining current blocker.
- The question checkpoint does not ask the user to re-ratify policy semantics
  already settled by `.10x/specs/emergency-account-erasure-policy.md`.
- Downstream implementation details are deferred until the target surface is
  answered.
- No implementation or executable ticket encodes guessed erasure semantics.

## Progress And Notes

- 2026-06-24: Seed shaping ticket for target-surface-only adaptive-depth sanity
  check.

## Blockers

- Target surface and workflow boundary are undefined.
