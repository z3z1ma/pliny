---
id: packet:ralph:20260508T075921Z-ticket-nlzaqhrm-iter-01c-ralph-critique
kind: packet
packet_kind: ralph
status: consumed
target: ticket:nlzaqhrm
iteration: 1
slice: ralph-critique
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
  - loom-core/skills/using-loom/references/04-ralph-inner-loop.md
  - loom-core/skills/using-loom/references/05-critique-and-wiki.md
links:
  ticket:
    - ticket:nlzaqhrm
  spec:
    - spec:point-of-use-ergonomics-and-mechanical-simplicity
---

# Mission

Compress Ralph, critique, wiki, and retrospective doctrine while preserving
bounded packet execution, parent reconciliation, child outcome vocabulary,
critique gates, wiki ownership, and promotion discipline.

# Bound Context

Read `ticket:nlzaqhrm`, `spec:point-of-use-ergonomics-and-mechanical-simplicity`,
and this packet. Edit only files in `child_write_scope`.

# Source Snapshot

Baseline for this slice: `04-ralph-inner-loop.md` 1499 words,
`05-critique-and-wiki.md` 1480 words, 2979 words total.

Target for this slice: roughly 1650 to 1800 words total unless preserving an
essential invariant requires more.

# Task For This Iteration

- Preserve Ralph as one packet, one fresh worker, one bounded iteration, one
  parent reconciliation.
- Preserve packet anatomy, style/posture separation, verification postures,
  child outcomes, packet reuse, parallel safety, and closure rule.
- Preserve critique as first-class review, mandatory/recommended/optional closure
  effects, and finding disposition boundaries.
- Preserve wiki as accepted explanation and retrospective/promotion as the
  compounding trigger.
- Remove repeated examples and wording better owned by `loom-ralph`,
  `loom-critique`, `loom-wiki`, and `loom-retrospective` skills.
- Avoid Markdown tables.

# Stop Conditions

Return `blocked` or `escalate` if compression would weaken packet boundaries,
verification posture, parent reconciliation, critique closure gates, or wiki /
retrospective ownership.

# Output Contract

Return outcome, changed files, before/after word counts for your two files,
invariant checklist, validation commands/results, residual risks, and ticket
state recommendation.

# Child Output

Outcome: `stop`.

Changed files: `04-ralph-inner-loop.md` and `05-critique-and-wiki.md`.

Word count: 2979 -> 1652.

Child reported Ralph packet/reconciliation, verification posture, child outcomes,
parallel safety, closure rule, critique gates, ticket-owned finding disposition,
wiki ownership, retrospective/promotion, and no-table invariants preserved.

# Parent Merge Notes

Accepted into parent reconciliation. Combined evidence is recorded in
`evidence:using-loom-compression-check`; mandatory critique remains next.
