Status: active
Created: 2026-06-22
Updated: 2026-06-22

# No Automatic Greenline Release

## Context

Kappa release operators want a "greenline" pilot indicator, but product has not
ratified what greenline means. Candidate meanings include display-only risk
label, review-ready queue position, release eligibility, automatic release, or a
score threshold. Each meaning changes operator workflow, permissions, audit
expectations, and release risk.

## Decision

Do not implement automatic release, approval, or lifecycle transition behavior
from the word "greenline" until product ratifies the semantic contract.

## Alternatives Considered

- Treat source constant `GREENLINE_MIN_SCORE = 85` as the product threshold:
  rejected because the source value is a preview hint, not a ratified contract.
- Treat greenline as auto-release eligibility: rejected until permissions,
  audit, and rollback semantics are defined.
- Treat greenline as a display-only label: possible, but still requires product
  ratification before implementation.

## Consequences

Agents may inspect and shape the pilot, but must not encode greenline threshold,
release eligibility, notification, permission, audit, or terminal state behavior
without a new active spec or user-ratified answer.
