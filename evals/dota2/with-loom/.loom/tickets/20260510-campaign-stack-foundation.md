# Campaign Stack Foundation

ID: ticket:20260510-campaign-stack-foundation
Type: Ticket
Status: closed
Created: 2026-05-10
Updated: 2026-05-10
Risk: medium - changes the app toolchain from a static script to a Vite/React stack and introduces dependency/build behavior.
Priority: high - other production slices depend on the stack running and building.

## Summary

Establish the modern frontend foundation for the Campaign Map app. This slice owns only the Vite/React scaffold, entrypoint, package scripts, and build viability. It does not own campaign UI completeness or OpenDota feature depth.

## Related Records

- `plan:20260510-rts-meta-explorer` - owns the production Campaign Map decomposition.
- `spec:opendota-rts-meta-explorer` - requires a modern frontend stack for maintainable deep analytics interactions.

## Scope

May change:

- `package.json`
- package lockfile if dependency installation creates one
- `vite.config.js`
- `index.html`
- `src/main.jsx` only enough to prove React mounts
- `README.md` run/check instructions

Must not change:

- OpenDota data model beyond minimal placeholder wiring
- visual campaign polish beyond mount-safe shell
- deep analytics behavior
- backend services or credentials

## Acceptance

- ACC-001: `npm install` can install the declared frontend dependencies without adding unrelated packages.
  - Evidence: install command result or existing lockfile inspection.
  - Audit: challenge whether dependency churn is scoped.

- ACC-002: `npm run build` succeeds and produces a Vite production build.
  - Evidence: build command output.
  - Audit: challenge whether the stack is actually buildable.

- ACC-003: `npm start`/`npm run dev` instructions in `README.md` match package scripts.
  - Evidence: package/README inspection.
  - Audit: challenge whether a future agent can run the app from the record.

## Current State

Closed. The Vite/React stack foundation is in place with `package.json`, `package-lock.json`, `vite.config.js`, `index.html`, `src/`, and `.gitignore`. `npm install`, `npm run build`, and `git diff --check` passed and are recorded in `evidence:20260510-campaign-stack-foundation-checks`.

Acceptance state:

- ACC-001 satisfied by `npm install` evidence and `package-lock.json` creation.
- ACC-002 satisfied by `npm run build` evidence.
- ACC-003 satisfied by package/README alignment for `npm install`, `npm start`, and `npm run check`.

This ticket does not claim product UI quality or runtime OpenDota behavior; those belong to later tickets.

## Journal

- 2026-05-10: Created from the split of cancelled `ticket:20260510-campaign-map-deep-analytics`.
- 2026-05-10: Ran `npm install`, `npm run build`, and `git diff --check`; recorded results in `evidence:20260510-campaign-stack-foundation-checks`.
- 2026-05-10: Added `.gitignore` for generated `node_modules/` and `dist/`; kept `package-lock.json` as the reproducible dependency artifact.
- 2026-05-10: Closed ticket; next plan move is `ticket:20260510-campaign-summary-data-foundation`.
