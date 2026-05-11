# OpenDota RTS Meta Explorer

ID: spec:opendota-rts-meta-explorer
Type: Spec
Status: active
Created: 2026-05-10
Updated: 2026-05-10

## Summary

This spec defines the intended behavior for a Warcraft 3 inspired, Dota-focused web experience backed by the public OpenDota API. The product should feel like entering an RTS command hall while still helping users explore current hero meta signals and recent match activity.

The spec is active for the next implementation pass. The operator selected a Campaign Map direction, a modern frontend stack, and deep analytics. The existing static app is a prototype slice, not the accepted final shape.

## Requirements

- REQ-001: The site MUST present a distinctive video-game command-center experience rather than a generic analytics dashboard.

- REQ-002: The site MUST use the public OpenDota API as its live data source for hero statistics and recent match activity, without requiring API keys or secret values.

- REQ-003: The hero meta view MUST let users inspect heroes by search, role, bracket, and sorting mode, and MUST surface picks, wins, win rate, and pro ban or pro heat where the API provides those values.

- REQ-004: The site MUST make recent matches understandable through readable pro and public match cards, including team names or hero lineups when available, score or winner information, duration, rank context when available, and links back to OpenDota match pages.

- REQ-005: The Campaign Map experience MUST organize exploration into distinct territories that reveal different data lenses, including meta overview, hero matchup/counter data, timing curves, item paths, recent hero performances, pro/public battles, and selected match detail when available.

- REQ-006: The site MUST fetch deeper OpenDota analytics on demand rather than loading every heavy endpoint upfront.

- REQ-007: The experience MUST handle loading, partial API failure, malformed successful payloads, heavy endpoint failures, and empty results without leaving the user in a broken or blank interface.

- REQ-008: The interface MUST be responsive enough for desktop and mobile exploration, with readable contrast, semantic landmarks, labels for controls, and keyboard-usable interactive elements.

- REQ-009: The site MUST avoid copying Warcraft 3 copyrighted assets. The allowed inspiration is original layout, color, texture, typography, and command-panel interaction language.

- REQ-010: The implementation SHOULD use a modern frontend stack for component structure, state management, production build output, and maintainable deep analytics interactions.

- REQ-011: User-linked OpenDota account identifiers from hero player analytics MUST not be displayed as raw account IDs in the primary UI.

## Scenarios

- SCN-001: Given a first-time visitor opens the page, when OpenDota requests complete successfully, then the visitor sees a campaign map with named territories and an active data panel rather than a conventional dashboard.
  - Exercises: REQ-001, REQ-002, REQ-005

- SCN-002: Given the hero meta data loaded, when the visitor changes bracket, search, role, or sort controls, then the hero cards and selected hero detail update without a page reload.
  - Exercises: REQ-003, REQ-008

- SCN-003: Given OpenDota hero statistics fail but match endpoints return data, when the page renders, then it explains the hero-data problem and still surfaces any available match chronicle data.
  - Exercises: REQ-007

- SCN-004: Given a narrow mobile viewport, when the visitor scrolls through the experience, then panels stack, text remains readable, controls remain usable, and hero/match cards do not require horizontal scrolling.
  - Exercises: REQ-008

- SCN-005: Given a hero is selected from the meta board, when the detail panel renders, then it shows portrait, role identity, win/pick signals, recent trend bars when provided, and a short interpretation in the command-center voice.
  - Exercises: REQ-001, REQ-003

- SCN-006: Given a hero is selected, when deeper analytics finish loading, then the map can show strongest counters, best matchups, duration performance, item popularity, recent hero matches, and anonymized top specialist signals.
  - Exercises: REQ-005, REQ-006, REQ-011

- SCN-007: Given a recent match card is selected, when match detail finishes loading, then the app shows a focused battle report with draft, scoreboard, objectives, teamfight count, and performance leaders without rendering the entire heavy match payload.
  - Exercises: REQ-004, REQ-006, REQ-007

## Interface Contract

- Data source: `https://api.opendota.com/api` public endpoints.
- In-scope summary endpoints: `/heroStats`, `/proMatches`, and `/publicMatches`.
- In-scope deep endpoints loaded on demand: `/heroes/{hero_id}/matchups`, `/heroes/{hero_id}/durations`, `/heroes/{hero_id}/players`, `/heroes/{hero_id}/itemPopularity`, `/heroes/{hero_id}/matches`, and `/matches/{match_id}`.
- Image source: hero `img` and `icon` paths from OpenDota hero stats are converted to Steam CDN URLs only when the paths match expected Dota image prefixes.
- External data rendered into HTML MUST be escaped because API values such as team or league names are untrusted text.

## Quality Bar

- Visual direction: carved stone, dark wood, brass/gold trim, rune-glow accents, campaign-map territories, fog-of-war panels, command-board overlays, parchment data cards, and high-drama hero portrait treatment.
- Interaction direction: controls should read like territories, routes, quests, scouting reports, battle chronicles, and draft council commands rather than ordinary admin widgets.
- Non-example: a plain Bootstrap dashboard with tables and charts only.

## Boundaries And Non-Goals

- The current production-feel pass does not create a backend, database, daemon, account system, or API proxy.
- The current production-feel pass does not store secrets or require an OpenDota API key.
- The current production-feel pass does not claim professional-grade predictions; computed meta scores are presentation heuristics derived from public API fields.
- The current production-feel pass does not clone Warcraft 3 UI assets or include Blizzard-owned imagery.
- The current production-feel pass does not render full raw match details; match detail drilldowns must select a focused subset from the heavy payload.

## Evidence Plan

- For REQ-002 and REQ-003, use source inspection plus runtime/API-shape observations showing the client fetches and transforms `/heroStats`.
- For REQ-004, use source inspection and runtime/API-shape observations showing `/proMatches`, `/publicMatches`, and selected match detail data are rendered safely.
- For REQ-005, use source inspection and browser observation when available to show map territories, navigation, and territory-specific content.
- For REQ-006 and REQ-007, use source inspection and focused tests or manual checks when available to show lazy loading, malformed payload handling, endpoint-specific errors, and empty states.
- For REQ-008, use CSS/source inspection and browser viewport checks when available.
- For REQ-011, use source inspection to show `account_id` values are not displayed in primary specialist UI.

## Open Questions

- Who is the primary user: casual Dota viewer, ranked player improving hero choices, esports analyst, or someone exploring Dota as a game world?
- Whether production quality requires a backend cache/API normalization layer after this client-only modern frontend pass.
- What evidence must exist before claiming production quality: browser screenshots, responsive checks, accessibility checks, live API runtime checks, performance budgets, or fresh design audit?
- Whether future versions should include match-detail drilldowns, player/account lookup, or league/team pages.
- Whether future versions should persist user preferences locally.
- Whether future versions should add a backend cache to reduce OpenDota rate-limit exposure.
