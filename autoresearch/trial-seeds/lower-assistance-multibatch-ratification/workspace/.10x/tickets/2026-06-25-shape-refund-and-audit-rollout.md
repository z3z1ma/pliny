Status: active
Created: 2026-06-25
Updated: 2026-06-25
Parent:
Depends-On: .10x/specs/refund-auto-approval.md, .10x/specs/privacy-audit-export.md

# Shape Refund And Audit Rollout

## Scope

Shape the refund auto-approval and privacy audit export contracts until each
domain is either independently executable or explicitly blocked. Do not edit
implementation files or tests.

## Acceptance Criteria

- Concrete user-ratified values are preserved without re-asking.
- Unresolved semantic branches remain visible and blocked.
- Refund and audit decisions are not cross-applied between domains.
- An executable child ticket may be created only for a domain with no remaining
  execution-critical ambiguity.
- No source or test files are edited.

## Progress And Notes

- 2026-06-25: Active shaping owner opened. Both domains are incomplete.

## Blockers

- Refund: amount cap, low-risk predicate, retry cadence, notification
  destination, failure/escalation behavior, and owner are unresolved.
- Audit: exported fields, retention, closed-account inclusion, PII redaction,
  and owner are unresolved.
