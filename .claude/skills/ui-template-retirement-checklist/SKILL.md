---
name: ui-template-retirement-checklist
description: Use when deleting/retiring UI modules or server template variants (e.g. removing src/agent_loom/ui/* or dashboard_v*.html) to prevent dangling references and keep contracts tested.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-02T21:02:44.841Z"
  updated_at: "2026-02-02T21:02:44.841Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
## When to use

- You delete/retire UI modules under `src/agent_loom/ui/`.
- You delete/retire server template variants under `src/agent_loom/server/templates/` (for example `dashboard_v*.html`).

## Goal

Remove legacy surfaces cleanly: no dangling references, and contracts stay deterministic.

## Checklist

1. Reference sweep
   - Search for imports/loads/paths referencing removed files.
   - Search for docs/README/usage text referencing removed commands/templates.

2. Runtime wiring sweep
   - Check server routes/templates selection logic for references to retired templates.
   - Check any CLI/UI registries that might import the removed modules.

3. Contract tests
   - For server HTML: update/add invariants in `tests/test_server_api_contract.py` (anchors/sections + ordering).
   - For CLI changes caused by removals: update/add the relevant CLI UX contract test module.

4. Verification gate
   - `uv run basedpyright`
   - `uv run ruff check .`
   - `uv run pytest <targeted modules>`

## Common failure modes

- Orphaned import in `__init__.py` or a registry module.
- Server route still selecting a deleted template.
- Contract tests asserting legacy sections/variants instead of stable invariants.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
