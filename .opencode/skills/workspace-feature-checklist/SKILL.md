---
name: workspace-feature-checklist
description: Use when adding/expanding workspace runtime (src/agent_loom/workspace/*): keep behavior deterministic, safe, and covered by targeted tests.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-01T07:19:01.983Z"
  updated_at: "2026-02-07T15:05:48.054314Z"
  version: "3"
---
<!-- BEGIN:compound:skill-managed -->
## When to use

- You changed workspace runtime code under `src/agent_loom/workspace/` (CLI, core, ops, models, state, guards).
- You added a new workspace command, behavior, or state transition.

## Goal

Ship workspace features with deterministic behavior, clear failure modes, and fast verification.

## Checklist

1. Determinism & ordering
   - Define explicit ordering for any list output or selection logic.
   - Add tie-break rules when sorting (avoid accidental nondeterminism).

2. Guardrails & errors
   - Ensure guard failures explain what to do next.
   - Avoid partial state updates on failure; keep operations atomic where possible.
   - If accepting TTL/duration inputs, validate strictly and make errors list supported units (`s|m|h|d|w`).

3. State & models
   - If you changed any on-disk representation or serialization, add a round-trip test.
   - If you moved/renamed persisted paths (dirs/files), keep reads backward-compatible or implement an idempotent best-effort migration (move old files); add a focused upgrade test.
   - Keep schema evolution simple; avoid implicit migrations unless required.

4. CLI contract (if CLI changed)
   - Use `tests/test_workspace_cli_ux.py` to lock required text/sections/ordering.

5. Verification gate
   - `uv run basedpyright`
   - `uv run ruff check .`
   - Run the smallest relevant pytest subset (and expand if failures suggest missing coverage).

## Notes

- Workspace features are agent-facing infrastructure: treat the CLI + state format as public API.
- Prefer stable, explicit behavior over clever inference.
- Prefer shared primitives from `src/agent_loom/core/` (fs escape/unescape, atomic IO, exec wrappers, concurrency helpers) over duplicating helpers under workspace.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
