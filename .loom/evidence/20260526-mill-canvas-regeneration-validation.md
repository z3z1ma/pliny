# Mill Canvas Regeneration Validation

ID: evidence:20260526-mill-canvas-regeneration-validation
Type: Evidence Dossier
Status: recorded
Created: 2026-05-26
Updated: 2026-05-26
Observed: 2026-05-26

## Summary

Validation observations for `ticket:20260526-mill-canvas-regeneration` after
implementing backend edit/reselect regeneration, stale subtree removal events,
frontend edit/reselect affordances, and regression coverage.

## Observations

- Observation: `uv run pytest tests/ -v` completed with all tests passing.
  Procedure/source: run from `loom-mill/` after the regeneration implementation.
  Actual result: `125 passed, 1 warning in 37.73s`. The warning was an existing
  subprocess cleanup warning from `tests/test_workstation_engine.py`.

- Observation: `npm run build` completed successfully for the frontend.
  Procedure/source: run from `loom-mill/frontend/` after the Svelte changes.
  Actual result: Vite reported `✓ built in 2.53s`. Build output also reported
  pre-existing Svelte deprecation/a11y warnings in chat components and a Svelvet
  Rollup sourcemap/comment warning.

- Observation: `git diff --check` completed with no output.
  Procedure/source: run from repository root after fixing the only whitespace issue
  introduced in `InputNode.svelte`.
  Actual result: no whitespace errors reported.

## Artifacts

- Command output remained in the current session transcript; no raw log artifact was
  written because the summaries above are sufficient for the validation claim.

## What This Shows

- `ticket:20260526-mill-canvas-regeneration#ACC-001` - supports - backend tests
  cover recursive stale marking and edit endpoint invalidation event emission.
- `ticket:20260526-mill-canvas-regeneration#ACC-002` - supports - backend tests
  cover stale subtree removal and replacement child creation under the edited node.
- `ticket:20260526-mill-canvas-regeneration#ACC-003` - supports - backend tests
  cover reselecting a dead option, killing the old selected subtree, activating the
  new option, and generating a new child when needed.
- `ticket:20260526-mill-canvas-regeneration#ACC-004` - partially supports - engine
  tests cover the max-depth guard preventing regeneration work when depth is zero;
  the implemented regeneration path performs one bounded invocation per endpoint
  call with `max_depth=3` and does not recursively re-enter itself.
- `ticket:20260526-mill-canvas-regeneration#ACC-005` - partially supports - edit and
  reselect endpoints now serialize session mutations with a per-session async lock;
  broad concurrent HTTP stress was not run.

## What This Does Not Show

- No Playwright browser run was performed for stale styling, fade-out/animation, or
  visual layout behavior.
- The frontend build proves compilation, not runtime WebSocket ordering in a browser.
- The pytest suite uses deterministic `printf` harness output, not a live LLM
  harness.
- The current ticket remains `active`; separate audit/review is still needed before
  closure.

## Related Records

- `ticket:20260526-mill-canvas-regeneration` - consuming ticket for this validation.
- `spec:mill-shaping-canvas` - REQ-012 reactive downstream regeneration behavior.
