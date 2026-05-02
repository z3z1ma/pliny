---
handoff_kind: outer-loop-synthesis
parent_objective: <initiative/spec/plan/ticket id; unrecorded objective only during intake>
status: draft
source_snapshot:
  compiled_at: <UTC timestamp>
  compiled_from:
    - <owner record id>
drive_checkpoint:
  anchor: <initiative id>
  active_tranche: <plan section or ticket ids>
  gate_status: <clear|blocked>
write_scope:
  records: []
  paths: []
---

# Outer-Loop Synthesis Handoff

Use this template only when a dedicated subagent would help the parent manage
context while shaping an objective, tranche, or next route. It collects a
proposal for parent review; accepted results still land in the owning Loom
records.

This is a bounded transient/support handoff proposal. It is not a packet family,
does not use `packet_kind`, and does not own canonical truth or live execution
state. Its `write_scope` describes any proposal-time mutation permission the
parent grants for this handoff; it is separate from Ralph packet
`child_write_scope` and from legacy packet `write_scope` compatibility.

The frontmatter `status` is support-local proposal status for this handoff only.
`draft` means the proposal is not yet reconciled by the parent. It is not
canonical record truth, ticket execution state, or shared packet lifecycle status,
and it does not participate in packet transitions such as `compiled -> consumed`.

## Parent Instructions

- Read the linked objective chain and only the source files named below.
- Propose owner-record updates, ticket slices, risks, and next routes.
- Do not modify files unless the parent explicitly grants a write scope.
- Do not close tickets, accept critique risk, or redefine success criteria.
- Return proposed changes for parent review and reconciliation.
- Treat unrecorded objectives as intake-only. Once an initiative, spec, plan, or
  ticket exists, cite owner record IDs instead of relying on conversation memory.

## Bound Context

- Objective / initiative:
- Drive Continuity Snapshot:
- Drive Checkpoint / resume anchor:
- Research:
- Spec:
- Plan:
- Tickets:
- Evidence / critique / wiki to inspect:
- Source paths, if any:

## Task

Summarize the current objective state and propose the next bounded tranche.

Include:

- current objective and measurable success criteria
- known constraints and non-goals
- objective gap matrix
- tranche contract, including included/excluded claims, likely tickets,
  dependencies, write-scope conflict check, evidence/critique gates, and
  reassessment point
- gaps or ambiguities that block safe continuation
- proposed owner-record changes
- proposed tickets or ticket refinements
- required evidence and critique posture
- stop conditions or user questions

## Output Contract

- proposed next route: continue / ask-user / critique / wiki / research / spec /
  plan / ticket / stop
- objective criterion IDs affected and proposed status changes
- current tranche assessment and proposed next tranche
- route decision priority applied and why
- safety gates checked and any blockers
- resume checkpoint updates required before parent stops
- owner-record changes proposed, grouped by layer
- ticket slices proposed, with scope and acceptance notes
- risks and unresolved questions
- evidence reviewed
- recommendation for parent reconciliation

## Parent Merge Notes

To be filled by the parent if this handoff is used. Record which proposed changes
were applied, rejected, or converted into follow-up work. A handoff is not
accepted drive truth until the parent reconciles it into owner records.
