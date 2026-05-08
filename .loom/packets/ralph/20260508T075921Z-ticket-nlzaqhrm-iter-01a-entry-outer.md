---
id: packet:ralph:20260508T075921Z-ticket-nlzaqhrm-iter-01a-entry-outer
kind: packet
packet_kind: ralph
status: consumed
target: ticket:nlzaqhrm
iteration: 1
slice: entry-outer
style: reference-first
verification_posture: observation-first
created_at: 2026-05-08T07:59:21Z
updated_at: 2026-05-08T08:07:10Z
source_fingerprint:
  repository: repo:root
  branch: main
  commit: 7cb65c63c90fe53da1c29a10ad51f33aeb290fb2
  dirty_state: other scoped tickets/records exist; child must edit only declared using-loom files
execution_context:
  harness: opencode task worker
  worktree: /Users/alexanderbutler/code_projects/personal/agent-loom
  isolation: shared checkout with non-overlapping file write scope
child_write_scope:
  - loom-core/skills/using-loom/SKILL.md
  - loom-core/skills/using-loom/references/01-core-identity.md
  - loom-core/skills/using-loom/references/03-outer-loop.md
links:
  ticket:
    - ticket:nlzaqhrm
  spec:
    - spec:point-of-use-ergonomics-and-mechanical-simplicity
---

# Mission

Compress the entry skill, core identity, and outer-loop doctrine without changing
their roles in the ordered using-Loom reference architecture.

# Bound Context

Read `ticket:nlzaqhrm`, `spec:point-of-use-ergonomics-and-mechanical-simplicity`,
and this packet. Edit only files in `child_write_scope`.

# Source Snapshot

Baseline for this slice: `SKILL.md` 778 words, `01-core-identity.md` 1042 words,
`03-outer-loop.md` 1016 words, 2836 words total.

Target for this slice: roughly 1500 to 1650 words total unless preserving an
essential invariant requires more.

# Task For This Iteration

- Keep the entry skill as the first-use index and mandatory doctrine loader.
- Keep reference 01 focused on mandatory identity, layers/loops/packets, ticket
  ledger, evidence, critique, wiki, packets, scope, and no-vibes completion.
- Keep reference 03 focused on outer-loop scoping, spec/research/plan/ticket
  routing, ticket readiness, loopbacks, and strategic restraint.
- Remove repeated explanation and examples already owned by task-specific skills.
- Avoid Markdown tables.

# Stop Conditions

Return `blocked` or `escalate` if you need to edit outside scope or cannot
compress without weakening mandatory Loom usage, owner layers, ticket readiness,
or outer-loop routing.

# Output Contract

Return outcome, changed files, before/after word counts for your three files,
invariant checklist, validation commands/results, residual risks, and ticket
state recommendation.

# Child Output

Outcome: `stop`.

Changed files: `SKILL.md`, `01-core-identity.md`, and `03-outer-loop.md`.

Word count: 2836 -> 1648.

Child reported all scoped invariants preserved, no missing invariants, no
Markdown pipe-table rows, and no whitespace errors.

# Parent Merge Notes

Accepted into parent reconciliation. Combined evidence is recorded in
`evidence:using-loom-compression-check`; mandatory critique remains next.
