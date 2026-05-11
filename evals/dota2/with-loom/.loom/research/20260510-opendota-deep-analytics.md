# OpenDota Deep Analytics Endpoints

ID: research:20260510-opendota-deep-analytics
Type: Research
Status: completed
Created: 2026-05-10
Updated: 2026-05-10

## Summary

The Campaign Map production pass can support deep analytics with on-demand OpenDota endpoints for selected heroes and matches. Hero matchup, duration, item popularity, hero-match, and hero-player aggregate endpoints are light enough to load for one selected hero. Full match details are heavier and should be fetched only when the user selects a match, then summarized into focused battle reports.

## Question

Which OpenDota deep endpoints can support a Campaign Map experience with hero counter, timing, item, specialist, recent performance, and match-detail territories?

## Scope

Covered:

- `/api/heroes/1/matchups`
- `/api/heroes/1/durations`
- `/api/heroes/1/players`
- `/api/heroes/1/itemPopularity`
- `/api/heroes/1/matches`
- `/api/matches/8806354486`

Excluded:

- Team, league, and player profile pages.
- Authentication, API-key behavior, and rate-limit characterization.
- Backend cache design.

## Method And Sources

- Fetched each endpoint live on 2026-05-10.
- Large `/heroes/1/players` and `/matches/8806354486` outputs were summarized by fresh explore workers from saved tool-output artifacts.

## Findings

- `/heroes/{hero_id}/matchups` returns an array of `{ hero_id, games_played, wins }`. This supports counter and favorable matchup cards when joined to `heroStats` names/images.
- `/heroes/{hero_id}/durations` returns an array of `{ duration_bin, games_played, wins }`. This supports timing curves and early/mid/late game interpretation.
- `/heroes/{hero_id}/itemPopularity` returns grouped item ID maps for `start_game_items`, `early_game_items`, `mid_game_items`, and `late_game_items`. This supports item-path panels but item names/icons need constants or fallback labels.
- `/heroes/{hero_id}/matches` returns recent match rows with `match_id`, `start_time`, `duration`, `radiant_win`, `leagueid`, `league_name`, side, account ID, slot, kills, deaths, and assists. This supports recent hero performance cards.
- `/heroes/{hero_id}/players` returned 3,661 player aggregate records for Anti-Mage with `account_id`, `games_played`, and `wins`. This supports specialist rankings, but raw account IDs are pseudonymous user-linked data and should not be displayed directly.
- `/matches/{match_id}` returned a roughly 197 KB object with 56 top-level fields, 10 player objects, objectives, teamfights, advantage arrays, and picks/bans. This supports selected-match battle reports, but the app should avoid rendering or retaining the full payload in broad UI loops.

## Tradeoffs

- On-demand hero deep analytics:
  - Strength: richer map territories without upfront loading every hero endpoint.
  - Risk: selected hero changes can create multiple network requests and partial failures.

- Full match detail on click:
  - Strength: production-feel drilldown for recent battles.
  - Risk: heavier payload and more external text fields to handle safely.

- Item popularity without item constants:
  - Strength: can still show phases and item IDs as strategic artifacts.
  - Risk: lower polish than named item icons. A future pass should fetch or embed item constants.

## Rejected Paths And Null Results

- Rejected preloading deep analytics for every hero because it would create many requests and a poor production experience.
- Rejected displaying raw `account_id` values in primary UI because they are public but user-linked and correlatable.
- Rejected rendering full match payload objects because the payload is large and contains many nested logs not needed for the map experience.

## Conclusions

- Deep analytics are feasible in a client-only modern frontend if the app loads them lazily and treats failures as territory-specific outages.
- The Campaign Map should have territories for counters, timing, item paths, specialist signals, recent hero battles, pro/public chronicle, and selected battle reports.
- The match detail territory should summarize draft, scoreboard, objectives, teamfights, and leaders instead of exposing raw payload structure.

## Recommendations

- Update `spec:opendota-rts-meta-explorer` with on-demand deep endpoint behavior and pseudonymous account ID handling.
- Implement the production-feel pass with a component-based frontend stack and route all deep endpoint failures to visible territory-level states.

## Open Questions

- Item names/icons require an additional constants source or fallback labels.
- Browser CORS and rate-limit behavior still need runtime evidence.

## Related Records

- `spec:opendota-rts-meta-explorer` - consumes these endpoint findings.
- `plan:20260510-rts-meta-explorer` - uses this research to unblock the next implementation ticket.
