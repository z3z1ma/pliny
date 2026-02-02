---
name: workspace-diff-ops-contract-testing
description: Use when changing workspace diff/read/ops code (diff_ops/repo_ops/poly_ops/workspace_read) to keep outputs deterministic, path-stable, and covered by focused tests.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-02T23:14:24.598Z"
  updated_at: "2026-02-02T23:14:24.598Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
## When to use

- You changed any of:
  - `src/agent_loom/workspace/diff_ops.py`
  - `src/agent_loom/workspace/repo_ops.py`
  - `src/agent_loom/workspace/poly_ops.py`
  - `src/agent_loom/dashboard/workspace_read.py`
- You touched logic that emits diffs, file lists, repo state summaries, or any data that could vary by machine.

## Goal

Keep workspace diff/read outputs deterministic, agent-legible, and regression-tested.

## Checklist

1. Deterministic ordering
   - Explicitly sort lists derived from the filesystem, git, dicts/sets.
   - Prefer stable keys (path, name, type) and document the ordering in tests.

2. Path stability
   - Prefer repo-root-relative paths in emitted data.
   - Avoid absolute paths and machine-specific prefixes.
   - Normalize separators and casing only if required by the repo contract.

3. Output shape is a contract
   - Keep keys/fields stable.
   - Avoid embedding timestamps, random IDs, or nondeterministic hashes.

4. Add/extend focused tests
   - Assert invariants (required fields, ordering rules, normalization) rather than entire payload dumps.
   - Add targeted fixtures that cover edge cases:
     - empty repo / no changes
     - rename vs delete
     - binary files
     - ignored/untracked files

5. Verification gate
   - `uv run basedpyright`
   - `uv run ruff check .`
   - `uv run pytest <smallest relevant module(s)>`

## Common failure modes

- Output order changes due to nondeterministic iteration.
- Absolute paths leaking into results (breaks determinism and agent parsing).
- Tests asserting full payloads that include volatile details.
- Git plumbing returning platform-specific results without normalization.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
