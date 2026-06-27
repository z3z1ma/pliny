Status: active
Created: 2026-06-22
Updated: 2026-06-22

# No Automatic Payment Retry Without Policy Ratification

## Context

The billing team needs better visibility into failed invoice recovery, but
customer payment retries can charge cards, trigger notifications, affect account
state, and create audit obligations. Product has not yet ratified retry count,
retry timing, charge authorization, notification recipients, dunning ownership,
idempotency behavior, or escalation semantics.

## Decision

Payment recovery work remains manual and report-only until billing operations
ratifies automatic retry semantics.

## Alternatives Considered

- Three retries over seven days: common SaaS behavior, but not authorized for
  this product and may violate account-specific payment agreements.
- Immediate retry on failure: simple, but risks duplicate charges and noisy
  customer notifications.
- Collector-owned manual queue: slower, but safe while policy semantics remain
  unresolved.

## Consequences

Agents may improve the manual failed-invoice queue, but they must not implement
automatic charge retries, notification sends, lifecycle transitions, or tests
that encode retry policy until those semantics are record-backed or
user-ratified.
