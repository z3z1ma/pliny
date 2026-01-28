---
name: ticket-feature-checklist
description: Use when adding/expanding ticket runtime (src/agent_loom/ticket/*): keep CLI behavior coherent with core/store, with LSP+ruff+targeted tests via uv.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-31T02:21:31.200Z"
  updated_at: "2026-01-31T02:21:31.200Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
## When to use

- You changed `src/agent_loom/ticket/cli.py`, `src/agent_loom/ticket/core.py`, or `src/agent_loom/ticket/store.py`.
- You changed ticket file format / serialization (`src/agent_loom/ticket/frontmatter.py`).
- You added/changed ticket state fields, storage shape, or CLI behavior.

## Goal

Keep ticket behavior consistent across CLI, core logic, and persistence; keep invariants testable.

## Checklist

1. Surface area audit
   - Identify the behavior you changed: CLI parsing/output, core semantics, persistence shape, adapters/API.
   - Confirm the CLI maps cleanly to core operations (no duplicate business logic in CLI).

2. Persistence + format invariants
   - If store schema/format changed, define upgrade/migration expectations.
   - Ensure read/write paths are symmetric.
   - If frontmatter/serialization changed, add a round-trip test (load -> write -> reload) to lock the format.
   - Ensure errors are actionable (what file, what field, what expected shape).

3. Deterministic output
   - Keep CLI output stable and parseable where possible.
   - Use explicit ordering for fields/lists; do not rely on dict/set iteration.

4. UX contract tests
   - If output formatting/UX changed, add/update a focused contract test in `tests/test_ticket_ux.py`.

5. LSP first
   - Run `lsp_diagnostics` on touched files.
   - Fix errors/warnings before lint/tests.

6. Lint
   - Run `uv run ruff check .`.

7. Targeted tests
   - Add/adjust focused tests for the changed behavior (CLI + core + store + format).
   - Start with `uv run pytest tests/test_ticket_ux.py` when UX/output is involved.
   - Otherwise run the smallest relevant subset first, then expand if needed.

## Common failure modes

- CLI behavior changes but core/store invariants are not covered by tests.
- Store changes land without clear handling of existing on-disk data.
- Frontmatter/file-format changes land without a round-trip regression test.
- Output becomes order-dependent (dict/set iteration) and breaks snapshots or tooling.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
