# Loom Mill Shaping Backend Audit Fixes

ID: ticket:20260526-mill-shaping-backend-audit-fixes
Type: Ticket
Status: review
Created: 2026-05-26
Updated: 2026-05-26
Risk: medium - fixes cross-cut shaping session runtime behavior, error handling, event delivery, and commit rollback
Priority: high - adversarial audit found blocking backend issues before shaping sessions can be trusted

## Summary

Fix the backend shaping session issues found by adversarial audit: keep proposal block payloads consistent with backend staging, return meaningful blocks and harness errors from `advance`, surface exploration blocks on the existing `shaping:block_added` channel, roll back failed git commits cleanly, and prove the full backend session lifecycle with an integration test.

Closure claim: Loom Mill shaping backend session lifecycle produces observable blocks, handles missing or failed harness paths without crashing, publishes exploration blocks through the frontend-consumed event channel, and commits or rolls back staged records predictably.

## Related Records

- `ticket:20260526-mill-shaping-harness` - introduced exploration orchestration and harness invocation behavior.
- `ticket:20260526-mill-shaping-blocks` - introduced engine advance and proposal block production.
- `ticket:20260526-mill-shaping-staging` - introduced staged record integration and commit materialization.

## Scope

May change:

- `loom-mill/src/loom_mill/shaping/engine.py`
- `loom-mill/src/loom_mill/shaping/orchestrator.py`
- `loom-mill/src/loom_mill/shaping/harness.py`
- `loom-mill/src/loom_mill/shaping/commit.py`
- `loom-mill/src/loom_mill/api/shaping.py`
- `loom-mill/tests/test_shaping_integration.py`

Must not change frontend files, start servers, bind ports, or widen into unrelated shaping UX fixes. Use echo or printf harness commands in tests. Every expected failure path should return a meaningful block or clear error rather than crashing unexpectedly.

## Acceptance

- ACC-001: Engine proposal blocks use the flat backend schema (`content.temp_id`, `content.surface`, `content.title`, `content.content`) and staging consumes that schema correctly.
  - Evidence: Source inspection and tests covering proposal staging or lifecycle behavior.
  - Audit: Verify no backend wraps proposals under `content.proposal`.

- ACC-002: `advance` returns produced blocks, including exploration start blocks, and converts harness-missing or harness-crash failures into meaningful returned blocks instead of HTTP 500s.
  - Evidence: Focused or integration tests through the API endpoint.
  - Audit: Verify exceptions do not bypass the user-visible block path for expected harness failures.

- ACC-003: Orchestrator publishes every added exploration/system block as `shaping:block_added` in addition to any specialized exploration event.
  - Evidence: Source inspection or tests over store events.
  - Audit: Verify frontend can rely on the existing block channel.

- ACC-004: Commit flow cleans the git index and deletes written files if `git add` or `git commit` fails, returning a clear error.
  - Evidence: Tests or source inspection of rollback path.
  - Audit: Verify no partial files or staged index entries remain from failed commit attempts.

- ACC-005: Full shaping lifecycle integration test covers create, advance with echo harness, operator input, second advance, manual staging, commit, and records written to disk.
  - Evidence: `uv run --extra dev python -m pytest tests/test_shaping_integration.py -x`.
  - Audit: Verify the test uses a simple echo/printf harness and does not start servers.

- ACC-006: Requested verification passes or failures are reported honestly: full backend tests, focused integration test, and frontend production build.
  - Evidence: Command output from the requested commands.
  - Audit: Separate audit would add useful trust before closure; leave ticket in review after implementation if no audit is run.

## Evidence

- `evidence:20260526-mill-shaping-backend-audit-fixes-validation` - focused shaping tests, full backend tests, focused integration test, frontend build, and whitespace-check limitation.

## Current State

Implementation is complete and ready for review/audit. Backend changes were made only in the shaping engine/API/orchestrator/harness/commit paths and shaping tests. Requested verification passed for the full backend suite, focused shaping integration test, and frontend build. Repository-wide `git diff --check` is blocked by unrelated frontend trailing whitespace outside this ticket's backend write scope.

## Journal

- 2026-05-26: Created ticket from the operator-provided adversarial audit findings and marked active for current-session implementation. Non-goals include frontend edits and server startup.
- 2026-05-26: Implemented backend audit fixes and moved to review. Evidence recorded in `evidence:20260526-mill-shaping-backend-audit-fixes-validation`; separate adversarial audit still recommended before closure because this ticket directly follows audit findings.
