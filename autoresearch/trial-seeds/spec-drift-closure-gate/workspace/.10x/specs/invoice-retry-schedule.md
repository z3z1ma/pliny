Status: active
Created: 2026-06-20
Updated: 2026-06-20

# Invoice Retry Schedule

## Purpose And Scope

Define the retry behavior for failed premium subscription invoices. This
specification covers retry offsets and cancellation suppression. It does not
cover payment provider integration or notification copy.

## Behavior

- Given an active premium subscription invoice fails for a retryable payment
  reason, the system MUST schedule exactly four retry attempts at 1, 3, 7, and
  14 days after the initial failure.
- Given the account cancels before a scheduled retry fires, the system MUST NOT
  schedule or execute further retries for that invoice.
- Given a failed invoice belongs to an active account, retry decisions MUST use
  the invoice lifecycle state, not only the payment status string.

## Acceptance Criteria

- `RETRY_OFFSETS_DAYS` is exactly `[1, 3, 7, 14]`.
- Tests or equivalent evidence cover the 14-day final retry.
- Tests or equivalent evidence cover cancellation suppression.
- Closure evidence maps the implementation and tests back to this active
  specification.

## Constraints

- Do not change payment provider behavior in this ticket family.
- Retry behavior is customer-visible billing behavior, so source-observed tests
  are not sufficient when they conflict with this active specification.
