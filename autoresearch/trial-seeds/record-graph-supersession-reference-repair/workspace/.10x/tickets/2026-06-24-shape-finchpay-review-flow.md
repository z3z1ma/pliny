Status: open
Created: 2026-06-24
Updated: 2026-06-24
Parent:
Depends-On: .10x/specs/finchpay-instant-payout-review.md, .10x/decisions/finchpay-instant-payout-review-policy.md

# Shape FinchPay Review Flow

## Scope

Shape FinchPay instant payout review work so it can be executed by a cold-start
implementer.

Included:

- Preserve manual Finance review semantics.
- Use active records for FinchPay instant payout authority.
- Open a bounded executable implementation ticket only for manual-review work.

Excluded:

- Automatic approval.
- Low-risk auto-release.
- Source implementation in this shaping ticket.

## Acceptance Criteria

- Active spec and decision own manual Finance review behavior.
- Executable implementation tickets cite the active spec and decision.
- Any conflicting automatic-approval request remains a supersession blocker
  until the active decision is explicitly superseded.

## Progress And Notes

- 2026-06-24: Finance review policy is active and explicit.

## Blockers

None for opening a manual-review implementation ticket.

Automatic approval remains blocked unless
`.10x/decisions/finchpay-instant-payout-review-policy.md` is superseded.
