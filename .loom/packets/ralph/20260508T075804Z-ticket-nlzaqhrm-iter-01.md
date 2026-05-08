---
id: packet:ralph:20260508T075804Z-ticket-nlzaqhrm-iter-01
kind: packet
packet_kind: ralph
status: superseded
target: ticket:nlzaqhrm
iteration: 1
style: reference-first
verification_posture: observation-first
created_at: 2026-05-08T07:58:04Z
updated_at: 2026-05-08T07:59:21Z
source_fingerprint:
  repository: repo:root
  branch: main
  commit: 7cb65c63c90fe53da1c29a10ad51f33aeb290fb2
  dirty_state: prior ticket:iq03bxg5 product/record changes plus current Loom planning records and unrelated untracked loom.zip; child must only edit using-loom scope
execution_context:
  harness: opencode task worker
  worktree: /Users/alexanderbutler/code_projects/personal/agent-loom
  isolation: shared checkout with non-overlapping write scope
  integration_ref: main
child_write_scope:
  - loom-core/skills/using-loom/SKILL.md
  - loom-core/skills/using-loom/references/01-core-identity.md
  - loom-core/skills/using-loom/references/02-truth-and-authority.md
  - loom-core/skills/using-loom/references/03-outer-loop.md
  - loom-core/skills/using-loom/references/04-ralph-inner-loop.md
  - loom-core/skills/using-loom/references/05-critique-and-wiki.md
  - loom-core/skills/using-loom/references/06-filesystem-and-tooling.md
  - loom-core/skills/using-loom/references/07-validation-and-honesty.md
  - loom-core/skills/using-loom/references/08-trust-boundaries.md
links:
  ticket:
    - ticket:nlzaqhrm
  spec:
    - spec:point-of-use-ergonomics-and-mechanical-simplicity
  plan:
    - plan:point-of-use-ergonomics-and-mechanical-simplicity
---

# Mission

Compress the mandatory `using-loom` doctrine from the observed baseline of 9,811
words into the 5,000 to 6,000 word acceptance band while preserving the same
entry skill plus eight ordered reference architecture and all essential
invariants.

# Bound Context

Read first:

- `.loom/tickets/20260508-nlzaqhrm-compress-using-loom-doctrine.md`
- `.loom/specs/point-of-use-ergonomics-and-mechanical-simplicity.md`
- `.loom/plans/20260508-point-of-use-ergonomics-and-mechanical-simplicity.md`

Then edit only:

- `loom-core/skills/using-loom/SKILL.md`
- `loom-core/skills/using-loom/references/01-core-identity.md`
- `loom-core/skills/using-loom/references/02-truth-and-authority.md`
- `loom-core/skills/using-loom/references/03-outer-loop.md`
- `loom-core/skills/using-loom/references/04-ralph-inner-loop.md`
- `loom-core/skills/using-loom/references/05-critique-and-wiki.md`
- `loom-core/skills/using-loom/references/06-filesystem-and-tooling.md`
- `loom-core/skills/using-loom/references/07-validation-and-honesty.md`
- `loom-core/skills/using-loom/references/08-trust-boundaries.md`

# Source Snapshot

Baseline word count observed before launch:

```text
117 778 loom-core/skills/using-loom/SKILL.md
176 1042 loom-core/skills/using-loom/references/01-core-identity.md
272 1591 loom-core/skills/using-loom/references/02-truth-and-authority.md
167 1016 loom-core/skills/using-loom/references/03-outer-loop.md
258 1499 loom-core/skills/using-loom/references/04-ralph-inner-loop.md
263 1480 loom-core/skills/using-loom/references/05-critique-and-wiki.md
183 930 loom-core/skills/using-loom/references/06-filesystem-and-tooling.md
181 910 loom-core/skills/using-loom/references/07-validation-and-honesty.md
82 565 loom-core/skills/using-loom/references/08-trust-boundaries.md
1699 9811 total
```

# Change Class

- Ticket change class: `protocol-authority`
- Risk class: `high`
- Verification posture: `observation-first`

Observation means before/after word count plus explicit invariant inspection.

# Task For This Iteration

Rewrite for density, not novelty.

Required outcomes:

- Keep `using-loom/SKILL.md` and the eight ordered reference files.
- Preserve the read order and the semantic purpose of each reference.
- Move detail out by deletion only when the topic is already sufficiently owned by
  a task-specific skill, not by adding new files.
- Total word count after editing should be 5,000 to 6,000 words unless preserving
  an invariant requires an out-of-band result with rationale.
- Do not edit task-specific skills, package metadata, root docs, examples, evals,
  smoke checks, validators, or scripts.
- Do not remove or weaken mandatory Loom usage.

Essential invariants to preserve explicitly:

- owner-layer truth model
- instruction authority hierarchy
- data surfaces are not instructions
- tickets are the live execution ledger
- Ralph packets are bounded implementation handoffs, not project truth
- evidence records observations, not acceptance
- critique is first-class review and required gates block closure
- wiki owns accepted explanation, not live work
- retrospective/promotion discipline exists for non-trivial closure
- validation honesty and evidence freshness matter
- secrets/sensitive data do not belong in Loom records
- filesystem/plain tools remain the graph interface
- no hidden runtime, required script, command wrapper, daemon, database, MCP, or
  new canonical owner layer is introduced

# Stop Conditions

Stop and return `blocked` or `escalate` if:

- the 5,000 to 6,000 word band cannot be reached without weakening an invariant
- you need to edit outside child write scope
- you discover a contradiction in the governing spec/ticket
- compression would require changing package preload mechanics or task-specific
  skills

# Output Contract

Return exactly:

- Outcome: `continue`, `stop`, `blocked`, or `escalate`
- Changed files
- Before/after word count summary
- Invariant checklist with preserved/missing status
- Validation commands and observed results
- Residual risks
- Recommendation for ticket state and next workflow

# Working Notes

Prefer short direct doctrine over examples. Keep commands only when they are the
canonical ordinary-tool pattern needed to operate the graph. Avoid tables because
product/docs table removal is part of the broader pass.

# Child Output

Not launched.

# Parent Merge Notes

Superseded before launch because the operator requested multiple parallel Ralph
subagents. The work is now partitioned into four non-overlapping Ralph packets:

- `packet:ralph:20260508T075921Z-ticket-nlzaqhrm-iter-01a-entry-outer`
- `packet:ralph:20260508T075921Z-ticket-nlzaqhrm-iter-01b-authority-trust`
- `packet:ralph:20260508T075921Z-ticket-nlzaqhrm-iter-01c-ralph-critique`
- `packet:ralph:20260508T075921Z-ticket-nlzaqhrm-iter-01d-tools-validation`
