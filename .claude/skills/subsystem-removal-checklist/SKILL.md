---
name: subsystem-removal-checklist
description: Procedural checklist for safely removing a major module/package without leaving broken imports, stale docs, or drifting contracts.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-09T04:04:39.675559Z"
  source_episode_ids: "3a49e37b2714b270438b82f96000a53a401f9d577d6a7ca6976af7f4eb510cdb"
  source_instinct_ids: "cli-ux-change-needs-tests,keep-openapi-and-ui-in-sync,post-refactor-quality-gates,remove-orphans-after-large-deletions,subsystem-removal-sweep"
  tags: "docs,maintenance,refactor,tests,uv"
  updated_at: "2026-02-09T04:04:39.675559Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
# Subsystem Removal Checklist

Use this when deleting or deprecating a substantial subsystem (package/module tree).

## Steps

1. Identify the public surface
- Find entrypoints, CLI commands, and any `__init__.py` exports that reference the subsystem.

2. Remove code and update imports
- Delete the subtree.
- Update all import sites and re-home any still-needed utilities.
- Fix `__init__.py` re-exports so the package surface stays accurate.

3. Update docs and examples
- Remove/replace references in README/docs.
- Update any CLI usage examples and expected outputs.

4. Update API contracts (if applicable)
- If endpoints or payloads changed, update `docs/openapi.yaml` in the same change.
- Ensure any dashboard/server consumers are updated to match.

5. Update and/or rewrite tests
- Remove tests for deleted behavior.
- Add/adjust tests to validate replacement behavior and CLI UX.

6. Run gates
- `uv run ruff check .`
- `uv run basedpyright`
- `uv run pytest`

## Done Criteria
- No remaining references to deleted modules.
- Docs and OpenAPI reflect current behavior.
- All gates pass.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
