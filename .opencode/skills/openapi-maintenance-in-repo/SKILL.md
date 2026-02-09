---
name: openapi-maintenance-in-repo
description: Keep `docs/openapi.yaml` consistent, stable, and reviewable when endpoints or schemas change.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-09T04:23:39.443272Z"
  source_episode_ids: "e73f6556efab5a08fe44febbe2ba7d245b558f059154ad39c13d6adedb7d42b2"
  source_instinct_ids: "openapi-keep-spec-deterministic,prefer-uv-gates-before-tests"
  tags: "api,docs,openapi"
  updated_at: "2026-02-09T04:23:39.443272Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
# Skill: OpenAPI Maintenance In Repo

## When to use
- You edit API endpoints, response bodies, or schemas and need to update `docs/openapi.yaml`.

## Procedure
1. Make a minimal, coherent spec change
- Update paths and component schemas together.
- Prefer stable naming and avoid churn-only edits.

2. Keep the spec deterministic
- Avoid volatile fields (timestamps, generated markers) unless required.
- Keep ordering consistent to reduce diff noise.

3. Validate consistency with code expectations
- Confirm request/response shapes match handlers.
- Confirm schema references resolve (no missing `$ref`).

4. Update tests that assert API/contract behavior
- If tests cover API output or wiring, update them alongside the spec.

## Done checklist
- Spec diff is readable and intentional
- No stale references remain
- Quality gates pass: `uv run basedpyright`, `uv run ruff check .`, `uv run pytest`
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
