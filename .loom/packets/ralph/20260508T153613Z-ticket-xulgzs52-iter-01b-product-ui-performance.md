---
id: packet:ralph:20260508T153613Z-ticket-xulgzs52-iter-01b-product-ui-performance
kind: packet
packet_kind: ralph
status: consumed
target: ticket:xulgzs52
iteration: 1
slice: product-ui-performance
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
  - loom-playbooks/skills/loom-codemap/SKILL.md
  - loom-playbooks/skills/loom-performance/SKILL.md
  - loom-playbooks/skills/loom-performance/references/measure-optimize-guard.md
  - loom-playbooks/skills/loom-product-discovery/SKILL.md
  - loom-playbooks/skills/loom-simplification/SKILL.md
  - loom-playbooks/skills/loom-simplification/references/simplification-playbook.md
  - loom-playbooks/skills/loom-spike/SKILL.md
  - loom-playbooks/skills/loom-ui-browser/SKILL.md
  - loom-playbooks/skills/loom-ui-browser/references/ui-runtime-quality.md
links:
  ticket:
    - ticket:xulgzs52
  spec:
    - spec:point-of-use-ergonomics-and-mechanical-simplicity
---

# Mission

Remove Markdown pipe tables from scoped product, UI, performance, codemap, spike,
and simplification playbook files.

# Rules

- Preserve row content by default.
- Delete rows only if plainly duplicate or stale, and report the rationale.
- Preserve product-discovery, evidence, research, wiki, UI runtime, and performance
  measurement boundaries.
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

- `loom-playbooks/skills/loom-codemap/SKILL.md`
- `loom-playbooks/skills/loom-performance/SKILL.md`
- `loom-playbooks/skills/loom-performance/references/measure-optimize-guard.md`
- `loom-playbooks/skills/loom-product-discovery/SKILL.md`
- `loom-playbooks/skills/loom-simplification/SKILL.md`
- `loom-playbooks/skills/loom-simplification/references/simplification-playbook.md`
- `loom-playbooks/skills/loom-spike/SKILL.md`
- `loom-playbooks/skills/loom-ui-browser/SKILL.md`
- `loom-playbooks/skills/loom-ui-browser/references/ui-runtime-quality.md`

Validation:

- Targeted scoped pipe-table scan: no pipe table rows found.
- `git diff --check -- <scoped files>`: no output.

Deleted rows: none. Only Markdown table header/separator syntax was removed.

Residual risks: No rendered Markdown preview was run; validation was limited to the
packet's scoped files.

# Parent Merge Notes

Accepted for parent reconciliation. Whole-playbook evidence is preserved in
`evidence:playbook-table-removal-check`.
