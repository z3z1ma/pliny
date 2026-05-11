# Static RTS Meta Explorer MVP

ID: ticket:20260510-static-rts-meta-explorer
Type: Ticket
Status: closed
Created: 2026-05-10
Updated: 2026-05-10
Risk: medium - implements a greenfield user-facing static app against live external API data with non-trivial visual and responsive behavior.

## Summary

Implement the complete dependency-free MVP of the OpenDota RTS meta explorer. The result should be a static website in the root of this workspace that users can run locally, fetches OpenDota hero and match data directly in the browser, and presents that data through an original Warcraft 3 inspired command-center UI.

## Related Records

- `plan:20260510-rts-meta-explorer` - owns the broader strategy and sequencing for the build.
- `spec:opendota-rts-meta-explorer` - defines the intended behavior, quality bar, scenarios, and non-goals.
- `research:20260510-opendota-api-shape` - records the endpoint and field shapes used by the implementation.

## Scope

May change:

- `index.html`
- `styles.css`
- `app.js`
- `README.md`
- `package.json`
- this ticket and directly related Loom records

Must not change:

- repository package architecture outside this `evals/dota2/with-loom` workspace
- root Agent Loom package surfaces
- adapter manifests, hooks, or shipped Loom skill content
- backend services, databases, or credential handling

Non-goals:

- user accounts
- saved preferences
- backend caching
- full match detail drilldowns
- Warcraft 3 or Blizzard asset copying

## Acceptance

- ACC-001: The workspace contains a runnable static site with HTML, CSS, and JavaScript files plus a short README explaining how to run it.
  - Evidence: source inspection and static server smoke check.
  - Audit: fresh-context review should challenge whether the site is actually runnable and self-contained.

- ACC-002: The client fetches and uses OpenDota `/heroStats`, `/proMatches`, and `/publicMatches` data, and renders useful hero meta and recent match information.
  - Evidence: source inspection, syntax check, and API-shape research link.
  - Audit: fresh-context review should challenge endpoint usage, partial-failure behavior, and external data rendering.

- ACC-003: The UI includes game-inspired visual treatment, hero meta controls, hero detail, recent match chronicle, loading/error states, and responsive layout rules.
  - Evidence: source inspection of `index.html`, `styles.css`, and `app.js`; browser screenshot evidence is preferred if a browser tool becomes available.
  - Audit: fresh-context review should challenge whether the implementation meets the spec quality bar without copying protected assets.

- ACC-004: Verification commands available in this workspace pass or limitations are recorded honestly.
  - Evidence: command output recorded in evidence or ticket journal.
  - Audit: fresh-context review should challenge overstated verification claims.

## Current State

The static MVP is complete in `index.html`, `styles.css`, `app.js`, `README.md`, and `package.json`. It fetches OpenDota `heroStats`, `proMatches`, and `publicMatches`, renders the RTS-inspired command hall, supports hero search/filter/sort/detail interactions, renders pro/public match chronicle cards, and handles loading, empty, rejected endpoint, and malformed successful payload states.

Acceptance state:

- ACC-001 satisfied by the static files, README, and local static server smoke result in `evidence:20260510-rts-meta-mvp-checks`.
- ACC-002 satisfied by source implementation and `research:20260510-opendota-api-shape`, with audit confirming endpoint fit and data-shape guards.
- ACC-003 satisfied by source inspection and audit for game-inspired UI, controls, detail, chronicle, loading/error states, and responsive CSS. Browser visual evidence was not gathered and remains an explicit limitation.
- ACC-004 satisfied by `npm run check`, `git diff --check`, and static server smoke evidence.

Fresh-context audit `audit:20260510-rts-meta-mvp` returned pass with reservations. The record-staleness finding was addressed by this closure update, and the optional wrapping hardening finding was addressed in `styles.css`. Remaining risk: no real browser visual/mobile/accessibility/CORS pass was performed.

## Journal

- 2026-05-10: Created active ticket from `plan:20260510-rts-meta-explorer` after source research and product spec were established.
- 2026-05-10: Added the dependency-free static MVP files: `index.html`, `styles.css`, `app.js`, `README.md`, and `package.json`.
- 2026-05-10: Ran `npm run check`, `git diff --check`, and a local static server smoke check; all passed and were recorded in `evidence:20260510-rts-meta-mvp-checks`.
- 2026-05-10: Fresh audit initially identified malformed successful API payload handling; patched `arrayPayload` guards and `finally` loading cleanup, then reran checks.
- 2026-05-10: Final fresh-context audit returned pass with reservations in `audit:20260510-rts-meta-mvp`; patched additional text wrapping hardening and closed the ticket with browser-visual verification explicitly not claimed.
