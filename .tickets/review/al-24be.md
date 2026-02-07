---
"id": "al-24be"
"status": "review"
"deps":
- "al-0e62"
"links": []
"created": "2026-02-07T06:00:20Z"
"type": "task"
"priority": 2
"assignee": "z3z1ma"
"parent": "al-1f81"
"tags":
- "workspace"
- "cleanup"
- "gc"
- "ttl"
- "lifecycle"
"external": {}
---
# Workspace: unify cleanup/GC story (TTL, leases, metadata) across repo + poly

We have several cleanup-like mechanisms:
- Repo mode: `cleanup suggest/apply` uses TTL metadata.
- Repo/poly sandboxes: `sandbox gc` uses TTL.
- Poly mode: `worktree gc` uses mtime/older-than and can skip claimed groups via leases.

This is close to the value proposition, but it's split across commands and semantics.

## Design

Goals:
- One coherent lifecycle model:
  - TTL is always evaluated against the same timestamp field (prefer `last_used_at`).
  - Leases/claims are respected by default for poly group deletion.
  - Metadata is cleaned up when worktrees are removed.

Proposed changes:
- Factor a shared expiration helper used by:
  - repo cleanup
  - repo sandbox gc
  - poly sandbox gc
  - poly worktree gc (new TTL-based mode)
- Add poly cleanup parity:
  - `loom workspace poly cleanup suggest` (list expired groups/worktrees with reasons)
  - `loom workspace poly cleanup apply --id ... --yes` (remove + clean meta)
  - Optionally: `loom workspace poly worktree gc --ttl` as shorthand.
- Ensure group deletion cleans:
  - `.loom/.../worktree meta`
  - `.loom/leases` entries if present (or mark stale)

Risk management:
- All destructive operations require `--yes`.
- Add contract tests for the new behavior.

Non-goals:
- No automatic background cleanup.

## Acceptance Criteria

- TTL cleanup semantics are consistent across repo + poly and share one implementation.
- Poly mode has an explicit TTL-driven cleanup pathway (suggest/apply or gc flag).
- Tests cover: (a) TTL expiry deletes unclaimed groups, (b) claimed groups are skipped, (c) metadata is removed.

## Notes

**2026-02-07T07:11:52Z**

Starting: unify TTL cleanup semantics across repo + poly (TTL vs last_used_at), respect leases for poly group deletion, ensure metadata cleanup on removal, and add explicit poly TTL cleanup commands (suggest/apply) with deterministic output + tests.

**2026-02-07T07:19:29Z**

Done: unified TTL expiration semantics via workspace.lifecycle.meta_is_expired across repo cleanup + poly sandbox gc + new poly TTL cleanup. Added poly TTL cleanup commands:  (apply requires --yes; skips claimed groups by default). Ensured metadata + stale lease cleanup when group becomes empty (poly worktree rm + poly worktree gc) and when repo worktrees are removed (repo worktree rm/rm-path + repo cleanup apply). Added regression test: tests/test_workspace_poly_cleanup_ttl.py (expires g1/g2, claims g1, asserts cleanup removes only unclaimed g2 + deletes meta). Verified: uv run basedpyright; uv run ruff check .; uv run pytest tests/test_workspace_*.py.

**2026-02-07T07:19:52Z**

Detail: added poly TTL cleanup commands: loom workspace poly cleanup suggest; loom workspace poly cleanup apply --id <group> --yes [--force].
