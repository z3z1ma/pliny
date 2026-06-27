Status: active
Created: 2026-06-23
Updated: 2026-06-23

# Checkout Payment Provider

## Context

Checkout retry work needs to know which payment provider owns retry outcomes.
Two options were considered: keep retry status tied to Stripe webhooks, or add a
new internal retry state machine immediately.

## Decision

Use Stripe webhook outcomes as the source of truth for checkout retry status in
the next implementation slice.

## Alternatives Considered

- Internal retry state machine now: rejected because no current requirement
  needs provider-independent retry orchestration.
- Manual support-only retry tracking: rejected because customers need visible
  checkout recovery state.

## Consequences

The retry UI should display Stripe-backed retry state and avoid inventing a
provider abstraction. If a second provider is added later, that requires a new
decision and migration plan.
