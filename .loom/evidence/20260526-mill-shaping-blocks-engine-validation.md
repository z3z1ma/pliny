# Mill Shaping Blocks Engine Validation

ID: evidence:20260526-mill-shaping-blocks-engine-validation
Type: Evidence Dossier
Status: recorded
Created: 2026-05-26
Updated: 2026-05-26
Observed: 2026-05-26

## Summary

Validation observations for `ticket:20260526-mill-shaping-blocks`, covering the new
decision parser, shaping engine advance loop, API route, backend regression suite,
and frontend production build.

## Observations

- Observation: The focused shaping engine test file passed.
  - Procedure/source: Ran `uv run --extra dev python -m pytest tests/test_shaping_engine.py -x` from `loom-mill/`.
  - Actual result: `10 passed in 0.20s`.
- Observation: The full backend test suite passed.
  - Procedure/source: Ran `uv run --extra dev python -m pytest tests/ -x` from `loom-mill/`.
  - Actual result: `85 passed in 30.67s` after the final API orchestrator cache fix.
- Observation: The frontend production build completed.
  - Procedure/source: Ran `npm --prefix loom-mill/frontend run build` from the repository root.
  - Actual result: Vite reported `✓ built in 1.85s`; existing Svelte deprecation/a11y warnings and chunk-size warning were emitted.
- Observation: Whitespace checking for the files touched by this ticket passed.
  - Procedure/source: Ran `git diff --check --` scoped to the ticket record, new shaping engine/parser/prompt/test files, and touched backend API/harness/app files.
  - Actual result: No output.
- Observation: Repository-wide whitespace checking reported unrelated pre-existing frontend whitespace issues.
  - Procedure/source: Ran `git diff --check` from the repository root.
  - Actual result: Reported trailing whitespace in `loom-mill/frontend/src/lib/design/GraphSidebar.svelte` lines 3 and 150, which were not touched by this ticket.

## Artifacts

- Command outputs are in the current session transcript; no raw artifact files were written for these concise checks.

## What This Shows

- `ticket:20260526-mill-shaping-blocks#ACC-001` - partially supports - the engine can produce typed blocks from mock harness decisions, including question, observation, and proposal blocks.
- `ticket:20260526-mill-shaping-blocks#ACC-003` - partially supports - tests cover operator feedback after a proposal transitioning the session to refining before continuing.
- `ticket:20260526-mill-shaping-blocks#ACC-004` - supports the parser/block path - tests cover `AGENT_PROPOSAL` creation with Markdown record content.
- `ticket:20260526-mill-shaping-blocks#ACC-005` - supports - malformed harness output is parsed as an observation rather than crashing.
- `ticket:20260526-mill-shaping-blocks#ACC-006` - supports - full backend tests passed.

## What This Does Not Show

- Does not prove live model/harness quality with an actual opencode/Claude decision invocation; tests use deterministic mock harness output.
- Does not prove complete Loom record Markdown quality for every proposal a model may generate; it verifies the transport and block creation path.
- Does not include a separate adversarial audit verdict; the ticket remains active/review-ready rather than closed.
- Does not address unrelated frontend Svelte warnings or GraphSidebar whitespace issues already present in the worktree.

## Related Records

- `ticket:20260526-mill-shaping-blocks` - consuming ticket for this validation story.
- `spec:mill-shaping-sessions` - intended behavior for shaping sessions.
