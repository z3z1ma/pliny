Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Pricing Exceptions Page

## Purpose And Scope

This specification covers the existing pricing exceptions review page.

## Behavior

The page lists pricing exception requests and displays the account name,
exception reason, status, requested discount, ARR impact, and renewal date for
each visible request.

No active specification defines a risk summary, churn-risk calculation, risk
threshold, risk label taxonomy, recommendation logic, or which signals should be
shown in a summary panel.

## Acceptance Criteria

- Existing list rendering remains unchanged unless a new ratified feature
  explicitly changes it.
- New risk-summary behavior requires a separate behavioral contract before
  implementation.

## Constraints

Do not infer churn risk from ARR impact, renewal date, status, or exception
reason without an accepted product definition.
