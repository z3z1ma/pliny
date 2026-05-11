# RTS Meta Explorer Build

ID: plan:20260510-rts-meta-explorer
Type: Plan
Status: completed
Created: 2026-05-10
Updated: 2026-05-10
Risk: medium - greenfield UI plus live external API integration, subjective visual quality, responsive behavior, and partial-failure states need coordinated evidence.

## Summary

Build a production-feel Warcraft 3 inspired OpenDota meta explorer in the empty `with-loom` workspace. The first static implementation exists, but the operator rejected framing the goal as an MVP and called out that the Loom outer loop should have shaped product quality, unknowns, and collaboration before implementation closure.

The production direction has been reshaped with the operator: Campaign Map, modern frontend stack, and deep analytics. The prior static app remains a prototype slice. An initial broad production ticket was cancelled because it was too large; the work is now split into stack, summary data, map shell, hero deep analytics, match reports, and verification slices.

## Related Records

- `spec:opendota-rts-meta-explorer` - defines the intended behavior, quality bar, scenarios, and non-goals.
- `research:20260510-opendota-api-shape` - records the OpenDota endpoint and field-shape findings that guide implementation.

## Strategy

Use a contract-first and slice-first route. The product direction is shaped enough to execute, but implementation must move through small reviewable tickets rather than a monolithic Campaign Map ticket.

The existing dependency-free static app may be reused, replaced, or treated as a prototype depending on the reshaped direction.

The implementation should keep external data rendering safe by escaping API-provided strings. Verification should focus on syntax, static serving, API contract alignment, and source-level inspection. Browser screenshot evidence is preferred in the future, but this workspace does not currently expose a browser automation tool.

Replan if OpenDota blocks browser access, if a backend becomes necessary for CORS or rate limits, if visual requirements require licensed assets, if match-detail drilldowns become part of the current scope, or if the operator chooses a product direction that the current static architecture cannot support.

## Execution Units

- `ticket:20260510-static-rts-meta-explorer` - implemented an initial dependency-free static prototype, including HTML shell, CSS visual language, JavaScript data fetching/transformation, hero meta controls, recent match chronicle, loading/error states, and local documentation. This is closed as a prototype slice, not accepted as the final product outcome.
  - Scope boundary: root static app files and directly related Loom records only.
  - Validation: `node --check app.js`, static server smoke check, `git diff --check`, and source/audit review.
  - Stop condition: stop if direct browser fetches require credentials, CORS workaround, or backend state.

- `ticket:20260510-rts-meta-verification` - verified the static prototype against the earlier MVP-shaped spec, recorded evidence, and ran fresh-context audit. This verification does not establish final production-feel acceptance.

- `ticket:20260510-campaign-map-deep-analytics` - cancelled broad ticket. It is retained only as the record of the bad slice and superseded by the smaller units below.

- `ticket:20260510-campaign-stack-foundation` - establish and verify Vite/React stack foundation.
  - Scope boundary: package/build config, entrypoint, minimal mount, README run/check instructions.
  - Validation: `npm install`, `npm run build`, `git diff --check`.
  - Stop condition: stop if dependency install/build introduces unrelated architecture or fails in a way that changes stack choice.

- `ticket:20260510-campaign-summary-data-foundation` - implement safe OpenDota summary data loading and hero normalization.
  - Scope boundary: API helpers, summary endpoint fetches, hero/image transforms, summary loading/error state.
  - Validation: build check and source review for malformed payload/partial-failure behavior.
  - Stop condition: stop if direct browser summary endpoints require a backend.

- `ticket:20260510-campaign-map-shell` - implement Campaign Map shell and production-feel responsive visual frame.
  - Scope boundary: map navigation, shell layout, hero scouting controls, responsive/focus styles.
  - Validation: build check, source review, browser observation if available.
  - Stop condition: stop if visual direction needs operator choice or licensed assets.

- `ticket:20260510-hero-deep-territories` - implement selected-hero deep analytics territories.
  - Scope boundary: hero matchup, duration, item, specialist, and hero-match territories.
  - Validation: build check and source review for lazy loading, empty/error states, and account ID handling.
  - Stop condition: stop if endpoint behavior requires backend caching or exposes raw user-linked identifiers.

- `ticket:20260510-match-battle-reports` - implement Chronicle and selected match battle reports.
  - Scope boundary: pro/public match feeds, selected match detail fetch, focused report transforms and UI.
  - Validation: build check and source review for heavy payload handling and safe text rendering.
  - Stop condition: stop if match detail payload cannot be safely summarized client-side.

- `ticket:20260510-campaign-production-verification` - verify final production-feel app and record evidence/audit.
  - Scope boundary: verification commands, evidence/audit records, ticket/plan state updates, small verification-driven fixes.
  - Validation: evidence record with observed outputs and fresh-context audit.
  - Stop condition: stop if browser/runtime checks are unavailable; record limitation instead of overclaiming.

## Milestones

- Contract and source grounding exist for the initial prototype: `spec:opendota-rts-meta-explorer` and `research:20260510-opendota-api-shape` supported the first static slice.
- Static prototype exists: the root app can run locally and render live OpenDota data in a game-inspired interface.
- Production direction shaped: Campaign Map, modern frontend stack, and deep analytics selected by operator.
- Production execution units created: stack foundation, summary data foundation, map shell, hero deep territories, match battle reports, and production verification.
- Production closure story exists: pending implementation, evidence, and audit against the revised production contract.

## Current State

The plan is active again after outer-loop shaping and ticket reslicing. The initial static prototype was implemented and verified, but it is not final product acceptance. The broad Campaign Map ticket was cancelled as an invalid slice.

Execution-unit state:

- `ticket:20260510-static-rts-meta-explorer` is closed as an initial prototype slice, not final product acceptance.
- `ticket:20260510-rts-meta-verification` is closed for that prototype slice only.

The plan is completed for the local production-feel Campaign Map app. The initial broad ticket was cancelled and replaced with smaller execution units. Stack foundation, summary data, Campaign Map shell, hero deep territories, match battle reports, and production verification are all closed.

Final verification state:

- `evidence:20260510-campaign-production-verification` records final build, diff, preview smoke, and follow-up review observations.
- `audit:20260510-campaign-production-audit` records a pass-with-reservations fresh-context verdict.

Residual risks: no real browser visual/mobile/accessibility traversal, screenshots, accessibility tree inspection, rendered contrast check, or live OpenDota browser runtime/CORS check was performed. OpenDota rate limits and hosted deployment behavior remain uncharacterized.

Plan-level residual risks: no real browser visual/mobile/accessibility pass was performed, and direct OpenDota browser usage remains exposed to upstream outage, rate limits, CORS changes, or data-shape changes despite source-level guards.

## Journal

- 2026-05-10: Created plan after operator corrected that the overall product is broader than one ticket. Preserved the broader work in spec, research, and plan surfaces before implementation.
- 2026-05-10: Completed the static MVP implementation through `ticket:20260510-static-rts-meta-explorer`.
- 2026-05-10: Completed verification through `ticket:20260510-rts-meta-verification`, preserving evidence in `evidence:20260510-rts-meta-mvp-checks` and audit in `audit:20260510-rts-meta-mvp`.
- 2026-05-10: Marked plan completed with explicit residual risk that browser visual/runtime verification was not performed.
- 2026-05-10: Operator rejected MVP framing and called out missing Loom outer-loop collaboration. Reopened the plan as blocked pending product-direction shaping; prior implementation remains a prototype slice, not final acceptance.
- 2026-05-10: Operator selected Campaign Map, modern frontend stack, and deep analytics. Updated spec, added deep endpoint research, created `ticket:20260510-campaign-map-deep-analytics`, and moved plan back to active.
- 2026-05-10: Operator challenged `ticket:20260510-campaign-map-deep-analytics` as too broad. Cancelled that ticket and replaced it with smaller execution units for stack foundation, summary data, map shell, hero deep territories, match reports, and production verification.
- 2026-05-10: Closed `ticket:20260510-campaign-stack-foundation` after `npm install`, `npm run build`, and `git diff --check` passed; evidence recorded in `evidence:20260510-campaign-stack-foundation-checks`.
- 2026-05-10: Closed `ticket:20260510-campaign-summary-data-foundation` after narrowing asset prefix validation, rerunning build/diff checks, and passing focused review; evidence recorded in `evidence:20260510-summary-data-foundation-checks`.
- 2026-05-10: Closed `ticket:20260510-campaign-map-shell` after fixing mobile stacking and focus inset issues, rerunning build/diff checks, and passing focused review; evidence recorded in `evidence:20260510-campaign-map-shell-checks`.
- 2026-05-10: Closed `ticket:20260510-hero-deep-territories` after fixing selected hero recent-raids loading behavior, rerunning build/diff checks, and passing focused review; evidence recorded in `evidence:20260510-hero-deep-territories-checks`.
- 2026-05-10: Closed `ticket:20260510-match-battle-reports` after fixing objective count and focused report state storage, rerunning build/diff checks, and passing focused review; evidence recorded in `evidence:20260510-match-battle-reports-checks`.
- 2026-05-10: Closed `ticket:20260510-campaign-production-verification` after final build/diff/preview checks, final audit, top-bar mobile fix, and focused follow-up review. Marked plan completed with explicit browser/runtime residual risks.
- 2026-05-10: Applied narrow follow-up `ticket:20260510-hero-picker-overlap-fix` after operator reported sticky Hero Scout overlap hiding the hero picker; build/diff checks passed.
