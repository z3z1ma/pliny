# Campaign Map Deep Analytics App

ID: ticket:20260510-campaign-map-deep-analytics
Type: Ticket
Status: cancelled
Created: 2026-05-10
Updated: 2026-05-10
Risk: medium - replaces the prototype with a modern frontend stack, richer interaction model, lazy deep API calls, and production-feel UI polish.

## Summary

This ticket was created too broadly: it attempted to replace the prototype, add a modern frontend stack, implement the Campaign Map, wire summary data, add lazy deep hero analytics, add match detail drilldowns, and verify production feel in one work unit.

It is cancelled because that shape violates ticket slicing discipline. The work is now decomposed into smaller child tickets under `plan:20260510-rts-meta-explorer`.

## Related Records

- `plan:20260510-rts-meta-explorer` - owns the broader strategy and current blocker resolution.
- `spec:opendota-rts-meta-explorer` - defines the active Campaign Map behavior contract.
- `research:20260510-opendota-api-shape` - records summary endpoint shapes.
- `research:20260510-opendota-deep-analytics` - records deep endpoint shapes and constraints.

## Scope

May change:

- root app files under this workspace
- package/build configuration for a modern frontend stack
- this ticket and directly related Loom records

Must not change:

- root Agent Loom package surfaces
- adapter manifests, hooks, or shipped Loom skill content
- backend services, databases, credentials, or API keys

Non-goals:

- backend cache
- accounts or saved preferences
- raw account ID display
- cloned Warcraft 3 assets

## Acceptance

- ACC-001: The app uses a modern frontend stack with install/build/dev scripts and renders through componentized source files.
  - Evidence: package/source inspection and build output.
  - Audit: fresh-context review should challenge whether the old prototype was actually replaced.

- ACC-002: The primary experience is a Campaign Map with navigable territories, not a dashboard grid.
  - Evidence: source inspection and preferably browser observation if available.
  - Audit: review should challenge visual/product fit against `spec:opendota-rts-meta-explorer#REQ-001` and `REQ-005`.

- ACC-003: Summary OpenDota endpoints load initial map state, while deep hero and match endpoints load on demand with territory-level loading/error states.
  - Evidence: source inspection and build checks.
  - Audit: review should challenge request volume, malformed payload handling, and partial-failure behavior.

- ACC-004: The app surfaces deep analytics for selected heroes and matches: counters/matchups, duration curve, item path, specialist signals without raw account IDs, recent hero battles, pro/public chronicle, and selected battle report.
  - Evidence: source inspection and API research links.
  - Audit: review should challenge data-shape assumptions and privacy/pseudonymous display handling.

- ACC-005: Available verification commands pass or limitations are recorded honestly.
  - Evidence: `npm run build`, any lint/check command available, and `git diff --check`.
  - Audit: review should challenge overstated browser/runtime claims.

## Current State

Cancelled as an invalid oversized ticket. Some implementation work was already done while this broad ticket was active; that work must be reconciled, verified, and corrected through the smaller replacement tickets rather than treated as accepted by this ticket.

Replacement tickets:

- `ticket:20260510-campaign-stack-foundation`
- `ticket:20260510-campaign-summary-data-foundation`
- `ticket:20260510-campaign-map-shell`
- `ticket:20260510-hero-deep-territories`
- `ticket:20260510-match-battle-reports`
- `ticket:20260510-campaign-production-verification`

## Journal

- 2026-05-10: Created ticket after operator selected Campaign Map, modern frontend stack, and deep analytics in outer-loop shaping.
- 2026-05-10: Operator correctly challenged this ticket as too broad. Cancelled it and split the plan into consumable execution tickets.
