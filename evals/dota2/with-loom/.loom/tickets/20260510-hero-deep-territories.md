# Hero Deep Analytics Territories

ID: ticket:20260510-hero-deep-territories
Type: Ticket
Status: closed
Created: 2026-05-10
Updated: 2026-05-10
Risk: medium - adds multiple lazy hero analytics endpoints and must avoid overfetching, raw account ID display, and brittle data-shape assumptions.
Depends On: ticket:20260510-campaign-map-shell

## Summary

Implement selected-hero deep analytics territories for the Campaign Map: Counterlands, Time Rift, Item Forge, Adept Tower, and selected hero recent raids. Deep endpoints must load lazily for the selected hero and fail independently without breaking the whole map.

## Related Records

- `plan:20260510-rts-meta-explorer` - sequences this after the shell exists.
- `spec:opendota-rts-meta-explorer` - defines on-demand deep analytics and account ID handling.
- `research:20260510-opendota-deep-analytics` - records endpoint shapes and caveats.

## Scope

May change:

- `src/api.js` deep endpoint helpers if needed
- `src/analytics.js` hero-deep transforms
- `src/main.jsx` hero territory components
- `src/styles.css` hero territory styles

Must not change:

- match detail drilldown beyond links/placeholders
- backend services or credentials
- raw account ID display in primary UI

## Acceptance

- ACC-001: Selecting a hero triggers lazy requests for matchup, duration, player aggregate, item popularity, and recent hero match endpoints without preloading every hero.
  - Evidence: source inspection and build check.
  - Audit: challenge request volume and dependency on selected hero state.

- ACC-002: Hero territories render matchup/counter rows, duration curve, item phases, anonymized specialist signals, and recent hero match cards when data is available.
  - Evidence: source inspection and API research links.
  - Audit: challenge data-shape assumptions and empty-state coverage.

- ACC-003: Raw OpenDota `account_id` values from `/heroes/{hero_id}/players` are not displayed in the primary UI.
  - Evidence: source inspection.
  - Audit: challenge pseudonymous data handling.

## Current State

Closed. Selected-hero deep analytics territories are implemented and source-reviewed: lazy hero-specific endpoint requests, matchup/counter rows, duration curve, item phases, anonymized specialist signals, selected hero recent raids, loading/error/empty states, and raw account ID avoidance. Evidence is recorded in `evidence:20260510-hero-deep-territories-checks`.

Acceptance state:

- ACC-001 satisfied by source review: deep hero requests are tied to selected hero state and do not preload every hero.
- ACC-002 satisfied after fix: hero territories render their data when available and selected hero recent raids now show loading instead of premature empty state.
- ACC-003 satisfied by source review: `/heroes/{hero_id}/players` data is transformed to anonymized `Adept NN` labels and raw `account_id` values are not displayed.

This ticket does not claim live browser/API runtime verification.

## Journal

- 2026-05-10: Created from the split of cancelled `ticket:20260510-campaign-map-deep-analytics`.
- 2026-05-10: Set active after `ticket:20260510-campaign-map-shell` closed.
- 2026-05-10: Focused review found selected hero recent raids showed empty state while loading; fixed by passing loading state into `RecentHeroMatches`.
- 2026-05-10: Reran `npm run build` and `git diff --check`; follow-up review passed. Evidence recorded in `evidence:20260510-hero-deep-territories-checks`.
- 2026-05-10: Closed ticket; next plan move is `ticket:20260510-match-battle-reports`.
