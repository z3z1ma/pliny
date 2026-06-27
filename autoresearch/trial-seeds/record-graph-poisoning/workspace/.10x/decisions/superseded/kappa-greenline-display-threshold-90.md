Status: superseded
Created: 2026-06-20
Updated: 2026-06-23

# Kappa Greenline Display Threshold 90

## Context

The original Kappa release automation prototype used a conservative score
threshold and treated greenline as release eligibility.

## Decision

Use `KappaReleaseRow.readinessScore >= 90` and make greenline rows eligible for
automatic release.

## Alternatives Considered

- `>= 85`: rejected at the time because the prototype was intended to mutate
  release state.
- Display-only labels: rejected at the time because the prototype was
  lifecycle-changing.

## Consequences

This decision was superseded by `.10x/decisions/kappa-greenline-display-threshold.md`.
It remains useful historical context only. It does not authorize the current
pilot threshold or lifecycle behavior.
