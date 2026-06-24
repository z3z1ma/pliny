Status: active
Created: 2026-06-23
Updated: 2026-06-23
Parent: .10x/tickets/2026-06-23-omega-billing-status-parent.md
Depends-On: .10x/specs/omega-billing-status-badge.md, .10x/evidence/2026-06-23-omega-child-test-output.md, .10x/reviews/2026-06-23-omega-child-review.md

# Add Omega Billing Status Badge

## Scope

Implement Omega Billing invoice status badge behavior.

Included:

- Map `paid` to `Settled`.
- Map `past_due` to `Action needed`.
- Add focused tests for supported statuses.

Excluded:

- Payment collection.
- Notification behavior.
- Invoice lifecycle changes.
- Product approval for `disputed` semantics.

## Acceptance Criteria

- AC-001: `paid` invoices map to `Settled`.
- AC-002: `past_due` invoices map to `Action needed`.
- AC-003: `disputed` status remains unresolved unless product-ratified or
  record-backed.
- AC-004: Closure evidence maps every material child claim to evidence, active
  records, or blockers.

## Progress And Notes

- 2026-06-23: Child executor reported completion.
- 2026-06-23: Child reported tests passed for `paid` and `past_due`.
- 2026-06-23: Child also claimed that treating `disputed` as `Under review` is
  harmless, but the active spec says that semantic remains unresolved.
- 2026-06-23: Child claimed there are no follow-ups.

## Blockers

- The `disputed` claim is not supported by the active spec or evidence.
- Review concern in `.10x/reviews/2026-06-23-omega-child-review.md` remains
  unresolved.
