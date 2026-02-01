---
name: loom-core-docs-hygiene
description: Use when changing AGENTS.md, LOOM_PROJECT.md, or LOOM_ROADMAP.md so the constitution/direction stays stable and agent-legible.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-01T18:34:49.248Z"
  updated_at: "2026-02-01T18:34:49.248Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
## When to use

- You need to edit `AGENTS.md`, `LOOM_PROJECT.md`, or `LOOM_ROADMAP.md`.
- You are tempted to delete or rewrite large sections of the repo's constitution/direction.

## Goal

Keep core docs stable, agent-legible, and safe to evolve.

## Checklist

1. Identify what is "contract"
   - `LOOM_PROJECT.md`: constitution (principles and non-negotiables).
   - `LOOM_ROADMAP.md`: direction (near-term focus and decision compass).
   - `AGENTS.md`: operational guidance + AI-managed blocks.

2. Respect AI-managed fences
   - Do not hand-edit inside `BEGIN/END` AI-managed fences.
   - Prefer `docs.blocks.upsert[]` entries in a CompoundSpec v2 to change managed content.

3. Make changes additive and minimal
   - Prefer adding or refining bullets over deleting large sections.
   - If removing text, replace it with a clearer, shorter invariant.

4. Keep the always-on context small
   - Only add principles that are durable across features.
   - Avoid implementation details and one-off incidents.

5. Enforce the repo path rule
   - Use repo-root-relative paths (e.g. `src/agent_loom/cli.py`).
   - Do not include absolute paths.

6. Keep it safe
   - Never include secrets, tokens, or local machine identifiers.
   - Avoid timestamps or other nondeterministic text in "contract" blocks.

7. Sync after doc changes
   - Set `docs.sync: true` in the CompoundSpec v2 so derived indexes stay consistent.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
