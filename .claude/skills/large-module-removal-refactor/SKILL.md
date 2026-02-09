---
name: large-module-removal-refactor
description: Procedure for safely deleting a large module/package and converging code, docs, and tests without leaving dead paths.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-09T04:23:39.443272Z"
  source_episode_ids: "e73f6556efab5a08fe44febbe2ba7d245b558f059154ad39c13d6adedb7d42b2"
  source_instinct_ids: "large-change-update-cli-ux-tests,prefer-uv-gates-before-tests,refactor-delete-module-chase-imports"
  tags: "python,quality,refactor,testing"
  updated_at: "2026-02-09T04:23:39.443272Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
# Skill: Large Module Removal Refactor

## When to use
- You are deleting or fully replacing a Python module/package (especially one referenced by CLI, docs, or tests).

## Goal
- No dangling imports, no dead entrypoints, tests updated, and quality gates pass.

## Procedure
1. Identify the removal boundary
- Name the module/package being removed and its public entrypoints (CLI commands, exported functions, docs references).

2. Remove code and immediately chase fallout
- Delete/move the module.
- Search the repo for:
  - old module path (e.g. `agent_loom.workspace.poly`)
  - key symbols/types that were commonly imported
  - CLI subcommand strings

3. Update routing + wiring
- If the removed code was reachable from CLI, update the corresponding CLI command handlers.
- If it affected a service/API surface, update `docs/openapi.yaml` accordingly.

4. Update tests and docs in the same sweep
- Update unit tests and CLI UX tests that reflect output/behavior.
- Update any READMEs under the affected package (e.g. `src/agent_loom/workspace/README.md`).

5. Run quality gates (in order)
- `uv run basedpyright`
- `uv run ruff check .`
- `uv run pytest`

## Done checklist
- `uv run basedpyright` is clean
- `uv run ruff check .` is clean
- `uv run pytest` passes
- No references to removed module remain in code/docs/tests
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
