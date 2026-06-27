Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Payout Retry Policy Authority

## Context

The payout failure queue has enough technical context to identify provider
transport failures, idempotency keys, account risk tier, and failed amount. It
does not establish business authority for automatic money movement after a
failure.

Automatic payout retry or auto-release can duplicate transfers, move money for
high-risk accounts, violate finance review requirements, or notify the wrong
owner when provider state is ambiguous.

## Decision

Automatic payout retry eligibility, auto-release eligibility, amount thresholds,
retry counts, risk-tier exclusions, notification recipients, and operational
owner must be explicitly ratified by Finance/Ops policy before implementation.

Until that policy is ratified, the product may surface failed payouts for manual
review and may preserve provider/idempotency facts, but it must not choose
automatic release behavior.

## Alternatives Considered

- Use standard SaaS retry defaults: rejected because money movement and risk
  review are domain policy, not generic implementation details.
- Auto-release low-risk failures below a guessed amount threshold: rejected
  because the threshold and low-risk definition are unratified business rules.
- Retry every provider transport failure three times: rejected because retry
  count, cadence, and escalation behavior require policy authority.

## Consequences

Implementation may prepare manual-review context and technical validation, but
executable tickets, tests, and code must not encode automatic retry or release
semantics until the policy is ratified.
