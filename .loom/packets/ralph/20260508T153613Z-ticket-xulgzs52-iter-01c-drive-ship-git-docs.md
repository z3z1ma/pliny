---
id: packet:ralph:20260508T153613Z-ticket-xulgzs52-iter-01c-drive-ship-git-docs
kind: packet
packet_kind: ralph
status: consumed
target: ticket:xulgzs52
iteration: 1
slice: drive-ship-git-docs
style: reference-first
verification_posture: observation-first
created_at: 2026-05-08T15:36:13Z
updated_at: 2026-05-08T15:40:41Z
source_fingerprint:
  repository: repo:root
  branch: main
  commit: 7cb65c63c90fe53da1c29a10ad51f33aeb290fb2
  dirty_state: prior core edits and Loom records exist; child must edit only declared playbook files
execution_context:
  harness: opencode task worker
  worktree: /Users/alexanderbutler/code_projects/personal/agent-loom
  isolation: shared checkout with non-overlapping file write scope
child_write_scope:
  - loom-playbooks/skills/loom-docs-sync/SKILL.md
  - loom-playbooks/skills/loom-docs-sync/references/documentation-sync.md
  - loom-playbooks/skills/loom-drive/SKILL.md
  - loom-playbooks/skills/loom-drive/references/continuity-contract.md
  - loom-playbooks/skills/loom-drive/references/tranche-decision-protocol.md
  - loom-playbooks/skills/loom-git/SKILL.md
  - loom-playbooks/skills/loom-git/references/parallel-ralph-with-git.md
  - loom-playbooks/skills/loom-ship/SKILL.md
links:
  ticket:
    - ticket:xulgzs52
  spec:
    - spec:point-of-use-ergonomics-and-mechanical-simplicity
---

# Mission

Remove Markdown pipe tables from scoped drive, ship, Git, and docs-sync playbook
files.

# Rules

- Preserve row content by default.
- Delete rows only if plainly duplicate or stale, and report the rationale.
- Preserve drive coordination boundaries, Git support truth boundary, ship
  packaging boundary, and docs-sync owner-routing semantics.
- Do not edit `.loom`, `loom-core`, root docs, examples, package scripts, or files
  outside `child_write_scope`.

# Validation

Before return, run a targeted table search and `git diff --check` for scoped
files.

# Output Contract

Return outcome, changed files, validation commands/results, deleted rows with
rationale or `none`, residual risks, and ticket recommendation.

# Child Output

Outcome: `stop`.

Changed files:

- `loom-playbooks/skills/loom-docs-sync/SKILL.md`
- `loom-playbooks/skills/loom-docs-sync/references/documentation-sync.md`
- `loom-playbooks/skills/loom-drive/SKILL.md`
- `loom-playbooks/skills/loom-drive/references/continuity-contract.md`
- `loom-playbooks/skills/loom-drive/references/tranche-decision-protocol.md`
- `loom-playbooks/skills/loom-git/SKILL.md`
- `loom-playbooks/skills/loom-git/references/parallel-ralph-with-git.md`
- `loom-playbooks/skills/loom-ship/SKILL.md`

Validation:

- Targeted scoped pipe-table scan: no output.
- `git diff --check -- <scoped files>`: no output.

Deleted rows: none.

Residual risks: Only scoped files were checked and edited. Validation was
structural, not a broader semantic review.

# Parent Merge Notes

Accepted for parent reconciliation. Whole-playbook evidence is preserved in
`evidence:playbook-table-removal-check`.
