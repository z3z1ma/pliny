---
id: packet:ralph:20260508T081302Z-ticket-58h4o1qo-iter-01b-ticket-spec-plan
kind: packet
packet_kind: ralph
status: consumed
target: ticket:58h4o1qo
iteration: 1
slice: ticket-spec-plan
style: reference-first
verification_posture: observation-first
created_at: 2026-05-08T08:13:02Z
updated_at: 2026-05-08T08:17:20Z
source_fingerprint:
  repository: repo:root
  branch: main
  commit: 7cb65c63c90fe53da1c29a10ad51f33aeb290fb2
  dirty_state: prior closed ticket edits and Loom records exist; child must edit only declared files
execution_context:
  harness: opencode task worker
  worktree: /Users/alexanderbutler/code_projects/personal/agent-loom
  isolation: shared checkout with non-overlapping file write scope
child_write_scope:
  - loom-core/skills/loom-specs/SKILL.md
  - loom-core/skills/loom-specs/templates/spec.md
  - loom-core/skills/loom-tickets/SKILL.md
  - loom-core/skills/loom-tickets/templates/ticket.md
  - loom-core/skills/loom-tickets/references/local-execution.md
  - loom-core/skills/loom-plans/SKILL.md
  - loom-core/skills/loom-plans/templates/plan.md
  - loom-core/skills/loom-plans/references/plan-shape.md
links:
  ticket:
    - ticket:58h4o1qo
  spec:
    - spec:point-of-use-ergonomics-and-mechanical-simplicity
---

# Mission

Remove Markdown pipe tables from scoped ticket, spec, and plan files by converting
them to label-led bullets or clearer non-table structures.

# Rules

- Preserve row content by default.
- Delete rows only if plainly duplicate or stale, and report the rationale.
- Preserve lite/full template guidance, acceptance vocabulary, ticket status,
  evidence/critique posture, and plan sequencing semantics.
- Do not edit `.loom`, `using-loom`, `loom-playbooks`, root docs, examples,
  package scripts, or files outside `child_write_scope`.

# Validation

Before return, run a targeted table search for your scoped files and
`git diff --check` for your scoped files.

# Output Contract

Return outcome, changed files, validation commands/results, deleted rows with
rationale or `none`, residual risks, and ticket recommendation.

# Child Output

Outcome: `stop`.

Changed files: scoped ticket, spec, and plan skills, templates, and references.

Validation: scoped table search found no pipe-table rows; scoped
`git diff --check` passed.

Deleted rows: none.

# Parent Merge Notes

Accepted into parent reconciliation. Combined evidence is recorded in
`evidence:core-table-removal-check`; critique is next.
