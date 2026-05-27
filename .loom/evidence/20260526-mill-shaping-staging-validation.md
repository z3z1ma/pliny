# Mill Shaping Staging Validation

ID: evidence:20260526-mill-shaping-staging-validation
Type: Evidence Dossier
Status: recorded
Created: 2026-05-26
Updated: 2026-05-26
Observed: 2026-05-26

## Summary

Validation observations for `ticket:20260526-mill-shaping-staging`: focused staging
tests, full backend tests, frontend build, and whitespace checks for touched files.

## Observations

- Observation: Focused staging tests passed.
  Procedure/source: Ran `uv run --extra dev python -m pytest tests/test_shaping_staging.py -x` from `loom-mill/`.
  Actual result: `6 passed in 0.76s`.
- Observation: Full backend tests passed.
  Procedure/source: Ran `uv run --extra dev python -m pytest tests/ -x` from `loom-mill/`.
  Actual result: `91 passed in 29.74s`.
- Observation: Frontend production build completed.
  Procedure/source: Ran `npm --prefix loom-mill/frontend run build` from the repository root.
  Actual result: Vite build succeeded; existing Svelte deprecation/a11y warnings and chunk-size warning were reported.
- Observation: Repository-wide whitespace check found unrelated pre-existing whitespace.
  Procedure/source: Ran `git diff --check` from the repository root.
  Actual result: Failed on trailing whitespace in `loom-mill/frontend/src/lib/design/GraphSidebar.svelte` lines 3 and 150, which were dirty before this ticket's edits.
- Observation: Touched-file whitespace check passed.
  Procedure/source: Ran `git diff --check --` over this ticket's touched files.
  Actual result: No output.

## Artifacts

- Command outputs are preserved in the current session transcript; no raw artifact files were written.

## What This Shows

- `ticket:20260526-mill-shaping-staging#ACC-001` - supports - focused tests cover staging propose, update, accept, reject, API CRUD, and persistence after reload.
- `ticket:20260526-mill-shaping-staging#ACC-002` - supports - focused tests cover branch create, switch, propose on branch, merge, and absence of source-branch records after merge.
- `ticket:20260526-mill-shaping-staging#ACC-003` - supports - focused tests commit three cross-referencing records and verify committed files contain real IDs and no `temp:` strings.
- `ticket:20260526-mill-shaping-staging#ACC-004` - supports - focused tests initialize a temp git repo, run commit flow, and verify latest commit message includes `shape: 1 tickets, 1 specs, 1 plans`.
- `ticket:20260526-mill-shaping-staging#ACC-005` - supports - focused tests verify the durable knowledge record path exists after commit.
- `ticket:20260526-mill-shaping-staging#ACC-006` - supports - focused tests simulate an atomic write failure and verify no partial files remain.
- `ticket:20260526-mill-shaping-staging#ACC-007` - supports - full backend suite passed.

## What This Does Not Show

- This does not include a browser-level manual staging workflow check.
- This does not prove frontend warnings are harmless; they predate this backend ticket's scope.
- This does not audit the implementation independently; it records validation observations only.

## Related Records

- `ticket:20260526-mill-shaping-staging` - ticket validated by these observations.
- `spec:mill-shaping-sessions` - intended shaping-session behavior.
