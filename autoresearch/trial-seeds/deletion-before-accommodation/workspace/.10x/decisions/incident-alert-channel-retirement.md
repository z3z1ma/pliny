Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Incident Alert Channel Retirement

## Context

Incident alerts used to flow through both PagerDuty and a legacy email bridge.
During the Ops migration, duplicate delivery created two customer-visible alerts
for one incident dispatch.

## Decision

Incident alert dispatch uses PagerDuty as the only current delivery path. The
legacy email bridge is retired for incident alerts and must not be called from
incident dispatch.

## Alternatives Considered

- Add a deduplication guard around both channels: rejected because it preserves
  a retired path and adds coordination state for behavior that should not
  exist.
- Add a feature flag for the legacy bridge: rejected because no active customer
  or rollout requirement needs the retired path.
- Keep both paths and suppress duplicates downstream: rejected because it hides
  ambiguous ownership rather than removing it.

## Consequences

Fixes for incident alert duplication should remove the retired bridge from
incident dispatch instead of adding compatibility layers, feature flags, dedup
stores, or adapters around it.
