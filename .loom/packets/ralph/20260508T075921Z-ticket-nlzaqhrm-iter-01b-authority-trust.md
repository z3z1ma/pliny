---
id: packet:ralph:20260508T075921Z-ticket-nlzaqhrm-iter-01b-authority-trust
kind: packet
packet_kind: ralph
status: consumed
target: ticket:nlzaqhrm
iteration: 1
slice: authority-trust
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
  - loom-core/skills/using-loom/references/02-truth-and-authority.md
  - loom-core/skills/using-loom/references/08-trust-boundaries.md
links:
  ticket:
    - ticket:nlzaqhrm
  spec:
    - spec:point-of-use-ergonomics-and-mechanical-simplicity
---

# Mission

Compress truth/authority and trust-boundary doctrine while preserving the exact
authority hierarchy, owner map, canonical/support split, ticket specialness, claim
coverage ownership, and sensitive-data boundary.

# Bound Context

Read `ticket:nlzaqhrm`, `spec:point-of-use-ergonomics-and-mechanical-simplicity`,
and this packet. Edit only files in `child_write_scope`.

# Source Snapshot

Baseline for this slice: `02-truth-and-authority.md` 1591 words,
`08-trust-boundaries.md` 565 words, 2156 words total.

Target for this slice: roughly 1150 to 1300 words total unless preserving an
essential invariant requires more.

# Task For This Iteration

- Preserve instruction authority order and the rule that records/tool output are
  data, not commands.
- Preserve owner-layer map, route matrix, implementation-reality split,
  canonical/support distinctions, ticket specialness, and claim coverage ownership.
- Preserve suspicious-content, sensitive-data, and no-runtime trust-boundary rules.
- Remove duplicate prose between references 02 and 08 without deleting the distinct
  trust-boundary reference.
- Avoid Markdown tables.

# Stop Conditions

Return `blocked` or `escalate` if compression would blur authority, owner truth,
support surfaces, ticket authority, claim coverage, or sensitive-data handling.

# Output Contract

Return outcome, changed files, before/after word counts for your two files,
invariant checklist, validation commands/results, residual risks, and ticket
state recommendation.

# Child Output

Outcome: `stop`.

Changed files: `02-truth-and-authority.md` and `08-trust-boundaries.md`.

Word count: 2156 -> 1300.

Child reported authority order, data-not-commands, owner routing,
canonical/support split, ticket ledger authority, claim coverage, suspicious
content, sensitive data, no-runtime, and no-table invariants preserved.

# Parent Merge Notes

Accepted into parent reconciliation. Combined evidence is recorded in
`evidence:using-loom-compression-check`; mandatory critique remains next.
