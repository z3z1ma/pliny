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
- 2026-06-25: User ratified refund auto-approval cap as $250 and low-risk
  predicate as exactly `riskTier === "low"`.
- 2026-06-25: User ratified privacy audit export retention as 90 days and
  closed-account policy as excluded.
- 2026-06-25: User ratified audit export fields as exactly `accountId`,
  `createdAt`, `status`, and `balanceCents`; email redaction by omission; and
  Data Platform ownership. Created executable audit child ticket
  `.10x/tickets/2026-06-25-implement-privacy-audit-export.md`.
- 2026-06-25: User ratified refund notification destination `#refund-ops`,
  Refund Ops ownership, and one retry after 30 minutes. Refund remains blocked
  because `normal risk escalation` is not defined by active records.

## Blockers

- Refund: failure/escalation behavior remains unresolved. The requested phrase
  `normal risk escalation` is not defined by active records and cannot be used
  as executable acceptance criteria.
- Audit: none. The audit implementation child ticket owns execution.
