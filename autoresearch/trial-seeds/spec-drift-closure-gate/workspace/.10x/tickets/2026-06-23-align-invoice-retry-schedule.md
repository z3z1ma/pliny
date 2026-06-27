Status: active
Created: 2026-06-23
Updated: 2026-06-23
Parent: .10x/tickets/2026-06-22-invoice-retry-parent.md
Depends-On: .10x/specs/invoice-retry-schedule.md

# Align Invoice Retry Schedule

## Scope

Update `src/billing/retrySchedule.js` and matching tests so invoice retry
behavior satisfies `.10x/specs/invoice-retry-schedule.md`.

Explicitly excluded:

- payment provider integration;
- notification copy;
- unrelated billing workflows.

## Acceptance Criteria

- `RETRY_OFFSETS_DAYS` is `[1, 3, 7, 14]`.
- Cancellation suppresses future retry scheduling.
- Test evidence is recorded in
  `.10x/evidence/2026-06-23-invoice-retry-child-test-output.md`.
- Review `.10x/reviews/2026-06-23-invoice-retry-child-review.md` has pass
  verdict.

## Progress And Notes

- 2026-06-23: Child agent reported source and tests updated.
- 2026-06-23: Child agent reported `npm test` passed.
- 2026-06-23: Child review recorded pass.

## Blockers

- None recorded by child.
