# Match Battle Reports

ID: ticket:20260510-match-battle-reports
Type: Ticket
Status: closed
Created: 2026-05-10
Updated: 2026-05-10
Risk: medium - fetches heavy match detail payloads and must summarize them safely without rendering raw nested logs or unescaped external text.
Depends On: ticket:20260510-campaign-map-shell

## Summary

Implement the Chronicle and Battle Report territories: recent pro/public match cards, selected hero recent raids linking into battle reports, and on-demand `/matches/{match_id}` detail summaries with draft/scoreboard/objective/leader views.

## Related Records

- `plan:20260510-rts-meta-explorer` - sequences this after shell and summary data.
- `spec:opendota-rts-meta-explorer` - defines recent match and selected battle report behavior.
- `research:20260510-opendota-deep-analytics` - records match detail payload size and safe summary guidance.

## Scope

May change:

- match-related transforms in `src/analytics.js`
- match/chronicle components in `src/main.jsx`
- match/chronicle styles in `src/styles.css`

Must not change:

- hero deep territories except shared selected-match hooks
- backend services or credentials
- raw full match payload rendering

## Acceptance

- ACC-001: Pro and public match feeds render useful match cards from summary endpoints and selecting a match opens the Battle Report territory.
  - Evidence: source inspection and build check.
  - Audit: challenge summary endpoint assumptions and external text safety.

- ACC-002: Match detail fetches are on-demand and produce focused battle reports from selected fields only.
  - Evidence: source inspection and API research links.
  - Audit: challenge heavy payload handling and raw nested-log exposure.

- ACC-003: Battle reports include score, teams, duration, league, teamfight/objective counts, scoreboard, and leaders when payload fields are available.
  - Evidence: source inspection.
  - Audit: challenge fallback/empty behavior.

## Current State

Closed. Chronicle feeds and selected match battle reports are implemented and source-reviewed: pro/public match cards, selected match navigation, on-demand detail fetch, focused report transform, total objective count, scoreboard, and leaders. Evidence is recorded in `evidence:20260510-match-battle-reports-checks`.

Acceptance state:

- ACC-001 satisfied by source review: pro/public feeds render match cards and selecting a match opens Battle Report territory.
- ACC-002 satisfied after fix: match detail is fetched on demand and transformed into a focused report before being stored in React state.
- ACC-003 satisfied after fix: Battle Report displays total objective count rather than sliced preview count, plus score, teams, duration, league, teamfights, scoreboard, and leaders.

This ticket does not claim live browser/API runtime verification.

## Journal

- 2026-05-10: Created from the split of cancelled `ticket:20260510-campaign-map-deep-analytics`.
- 2026-05-10: Set active after `ticket:20260510-hero-deep-territories` closed.
- 2026-05-10: Focused review found objective count truncation and full match payload state retention; fixed both in `src/analytics.js` and `src/main.jsx`.
- 2026-05-10: Reran `npm run build` and `git diff --check`; follow-up review passed. Evidence recorded in `evidence:20260510-match-battle-reports-checks`.
- 2026-05-10: Closed ticket; next plan move is `ticket:20260510-campaign-production-verification`.
