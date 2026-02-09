---
name: contract-sync-openapi
description: Micro-procedure for preventing API schema drift between server behavior, OpenAPI, and UI readers.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-09T04:04:39.675559Z"
  source_episode_ids: "3a49e37b2714b270438b82f96000a53a401f9d577d6a7ca6976af7f4eb510cdb"
  source_instinct_ids: "keep-openapi-and-ui-in-sync,post-refactor-quality-gates"
  tags: "api,contract,dashboard,openapi,testing"
  updated_at: "2026-02-09T04:04:39.675559Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
# Contract Sync (Server <-> OpenAPI <-> UI)

Use this when touching endpoints, payload shapes, or workspace/dashboard read paths.

## Steps

1. Change the server behavior
- Make the route/handler changes first.

2. Update `docs/openapi.yaml` immediately
- Reflect request/response shapes and status codes.
- Keep names consistent (path params, query params, fields).

3. Update UI/dashboard consumers
- Update any readers/clients that depend on the endpoint.
- Prefer failing fast on missing/renamed fields rather than silently ignoring.

4. Lock it with tests
- Add/adjust tests that would fail if the contract drifted again.

5. Run gates
- `uv run ruff check .`
- `uv run basedpyright`
- `uv run pytest`
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
