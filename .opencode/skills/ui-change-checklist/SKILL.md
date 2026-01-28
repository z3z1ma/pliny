---
name: ui-change-checklist
description: Use when modifying src/agent_loom/ui/*.py to keep UI output stable, lint-clean, and covered by targeted tests.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-31T03:03:39.463Z"
  updated_at: "2026-01-31T03:03:39.463Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
## When to use

- You changed `src/agent_loom/ui/*.py` (for example `src/agent_loom/ui/ticket_ui.py`).

## Goal

Keep UI behavior stable and easy to verify.

## Checklist

1. Deterministic output
   - Avoid timestamps, random IDs, and nondeterministic ordering.
   - Prefer stable formatting (explicit ordering, explicit widths if relevant).

2. LSP first
   - Run `lsp_diagnostics` on touched UI files.
   - Fix errors/warnings before lint/tests.

3. Lint
   - Run `uv run ruff check .` and resolve findings.

4. Targeted tests
   - Run the smallest relevant subset first (ex: `uv run pytest tests/test_ui_*.py`).
   - If no obvious subset exists, run `uv run pytest`.

## Common failure modes

- Small formatting tweaks break downstream parsing/snapshots.
- Output ordering changes due to dict/set iteration.
- Lint fixes deferred until later and snowball across unrelated files.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
