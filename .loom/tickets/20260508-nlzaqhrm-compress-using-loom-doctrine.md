---
id: ticket:nlzaqhrm
kind: ticket
status: closed
change_class: protocol-authority
risk_class: high
created_at: 2026-05-08T07:41:56Z
updated_at: 2026-05-08T08:12:04Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  spec:
    - spec:point-of-use-ergonomics-and-mechanical-simplicity
  plan:
    - plan:point-of-use-ergonomics-and-mechanical-simplicity
  evidence:
    - evidence:using-loom-compression-check
  critique:
    - critique:using-loom-compression-review
external_refs: {}
depends_on: []
---

# Summary

Compress `using-loom` always-on doctrine into the 5,000 to 6,000 word acceptance
band while preserving the ordered reference architecture and essential invariants.

# Context

The current measured baseline is about 9,811 words across
`loom-core/skills/using-loom/SKILL.md` and its eight ordered references. The goal
is lower point-of-use token cost without weakening doctrine.

# Scope

In:

- Edit `loom-core/skills/using-loom/SKILL.md`.
- Edit `loom-core/skills/using-loom/references/01-core-identity.md` through
  `08-trust-boundaries.md`.
- Remove repetition already owned by task-specific skills.
- Preserve the mandatory ordered reference architecture.
- Preserve the invariant checklist named in the governing spec.

Out:

- No changes to task-specific skills except follow-up notes if a reference gap is
  discovered.
- No package preload mechanics or adapter behavior changes.
- No new mechanical word-budget check.

Assumptions / decision triggers:

- The target is an acceptance band, not a hard 5,500-word ceiling.
- If compression threatens an essential invariant, keep the invariant and record
  rationale for any out-of-band word count.

# Acceptance

Owner: spec-owned.

Covered IDs:

- `spec:point-of-use-ergonomics-and-mechanical-simplicity#ACC-004`

Ticket-local criteria:

- ACC-LOCAL-001: Evidence records before/after `wc -l -w` results.
- ACC-LOCAL-002: Evidence or critique explicitly checks owner-layer truth,
  instruction authority, ticket ledger authority, Ralph boundaries, evidence,
  critique, wiki, validation honesty, trust boundaries, and no-runtime doctrine.

# Current State

Status rationale: closed; four parallel Ralph slices, combined evidence,
mandatory critique, and ticket acceptance are complete for this slice.

Blockers: None.

Execution notes: Packet `packet:ralph:20260508T075804Z-ticket-nlzaqhrm-iter-01`
was superseded before launch. Four parallel packets compressed non-overlapping
`using-loom` file groups and returned `stop`. Combined word count is 5,750.

Continuation note: Rewrite for density first, then validate against the word band
and invariant checklist before critique.

# Evidence

Disposition: sufficient.

Records:

- `evidence:using-loom-compression-check` — supports word-count reduction,
  ordered reference preservation, smoke-check pass, and initial invariant checks.

Gaps / limits: Evidence is structural and needs mandatory critique for doctrine
completeness and operator clarity.

# Review And Follow-Through

Critique policy: mandatory.
Critique rationale: this changes mandatory always-on doctrine.
Critique disposition: completed.

Required critique profiles:

- protocol-authority
- doctrine-completeness
- operator-clarity

Findings:

- None - `critique:using-loom-compression-review` returned `pass` with no
  findings.

Promotion disposition: not_required.
Promotion / deferral rationale: durable doctrine changes landed directly in the
owning product surface and are covered by spec, ticket, evidence, and critique.
No separate wiki promotion is required for this bounded compression slice.

Promoted / deferred:

- None - not required for this bounded product-surface slice.

Wiki disposition: not_required - accepted explanation lives in the compressed
using-Loom doctrine itself.

# Acceptance Decision

Accepted by: OpenCode agent per user-delegated implementation authority.
Accepted at: 2026-05-08T08:12:04Z
Basis: `evidence:using-loom-compression-check` records the 9,811 -> 5,750 word
reduction, ordered reference preservation, no-table result, diff-check pass, and
core smoke pass; `critique:using-loom-compression-review` returned `pass` with no
findings.
Residual risks: No comprehension/eval evidence exists; future operator-confusion
reports may reveal over-compressed passages that need follow-up.

# Dependencies

None.

# Journal

- 2026-05-08T07:41:56Z: Created as a ready execution ticket from the active spec
  and plan.
- 2026-05-08T07:58:04Z: Moved to active and compiled Ralph packet
  `packet:ralph:20260508T075804Z-ticket-nlzaqhrm-iter-01`.
- 2026-05-08T07:59:21Z: Superseded the unlaunched single-worker packet and
  compiled four parallel Ralph packets with non-overlapping write scopes.
- 2026-05-08T08:07:10Z: Four parallel Ralph workers returned `stop`; parent ran
  combined word-count, invariant-term, no-table, diff-check, and smoke validation,
  recorded `evidence:using-loom-compression-check`, and moved the ticket to
  `review_required`.
- 2026-05-08T08:12:04Z: Recorded `critique:using-loom-compression-review` with
  verdict `pass` and no findings, marked promotion/wiki follow-through not
  required, accepted the ticket, and closed it.
