---
name: basedpyright-ruff-pytest-gate
description: Use when validating Python changes in this repo: typecheck via uv+basedpyright, then ruff, then targeted pytest (no lsp_diagnostics).
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-01T02:50:11.293Z"
  updated_at: "2026-02-01T02:50:11.293Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
## When to use

- You changed Python code and need the repo-standard verification loop.
- A checklist/instinct suggests `lsp_diagnostics`.

## Gate sequence (do this order)

1. Typecheck
   - `uv run basedpyright`
   - Fix all findings before proceeding.

2. Lint
   - `uv run ruff check .`

3. Targeted tests
   - Run the smallest relevant suite, for example:
     - `uv run pytest tests/test_ticket_ux.py`
     - `uv run pytest tests/test_team_cli_ux.py`
     - `uv run pytest tests/test_team_prompts.py`
     - `uv run pytest tests/test_team_disband.py`

## Notes

- Always prefer `uv run ...` for all Python tooling.
- Do not use `lsp_diagnostics` in this repository.
- If your change affects user-visible text/ordering, prefer a focused UX contract test module (for example `tests/test_ticket_ux.py`).
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
