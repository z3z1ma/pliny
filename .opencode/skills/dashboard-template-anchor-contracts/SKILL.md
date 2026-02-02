---
name: dashboard-template-anchor-contracts
description: Use when editing the dashboard HTML template(s) to keep stable data-* anchors, deterministic ordering, and server contract tests aligned.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-02T20:07:38.170Z"
  updated_at: "2026-02-02T20:07:38.170Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
## When to use

- You changed `src/agent_loom/dashboard/templates/dashboard.html`.
- You changed `src/agent_loom/server/templates/dashboard.html`.
- You added/removed/reordered sections in a dashboard template.

## Goal

Make the rendered dashboard easy for both humans and agents to parse, and lock it with a focused contract test.

## Checklist

1. Add or preserve stable anchors
   - Prefer stable `data-*` attributes for sections and repeated items.
   - Use obvious, low-churn anchors like:
     - `data-section="..."` for major sections
     - `data-item="..."` for repeated rows/cards
     - `data-field="..."` for key label/value pairs when adding new fields
   - Avoid relying on CSS classes or deep DOM structure as the contract.

2. Diff hygiene (avoid churn)
   - Minimize formatting-only changes (indentation/whitespace reflow) unless required.
   - Keep section ordering deliberate and stable.
   - Preserve existing `data-*` anchors when reshuffling layout.

3. Keep rendering deterministic
   - Explicitly sort any lists that come from dicts/sets.
   - Avoid timestamps/random IDs/machine-specific paths in HTML.

4. Update the contract test
   - Prefer adding/updating request-level invariants in `tests/test_server_api_contract.py`.
   - Assert presence of key sections/anchors and deterministic ordering.
   - Avoid full-HTML snapshots unless the full HTML is intentionally the contract.

5. Verification gate
   - `uv run basedpyright`
   - `uv run ruff check .`
   - `uv run pytest tests/test_server_api_contract.py`
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
