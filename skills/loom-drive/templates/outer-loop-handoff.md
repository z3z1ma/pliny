---
id: support:drive-handoff-<UTC compact timestamp>-<slug>
kind: support-artifact
support_kind: drive-outer-loop-handoff
handoff_kind: outer-loop-synthesis
parent_objective: <initiative/spec/plan/ticket id; unrecorded objective only during intake>
status: draft
created_at: <UTC timestamp>
updated_at: <UTC timestamp>
scope:
  kind: repository
  repositories:
    - repo:root
links: {}
source_snapshot:
  compiled_at: <UTC timestamp>
  compiled_from:
    - <owner record id>
drive_checkpoint:
  anchor: <initiative id>
  active_tranche: <plan section or ticket ids>
  gate_status: "<TBD: choose clear or blocked before saving>"
handoff_write_scope:
  records:
    - "<TBD: proposal-time record write refs, or None - no writes>"
  paths:
    - "<TBD: proposal-time paths, or None - no writes>"
---

# Outer-Loop Synthesis Handoff

Use this template only when a dedicated subagent would help the parent manage
context while shaping an objective, tranche, or next route. It collects a
proposal for parent review; accepted results still land in the owning Loom
records.

This handoff is prompt-only by default. Save it only when the parent wants a
durable support artifact for reviewability, context recovery, or handoff audit.
If saved, place it under the optional, lazy-materialized, non-canonical support
surface
`.loom/support/drive-handoffs/<UTC compact timestamp>-<slug>.md` and keep the
support-local `id`, `kind`, `support_kind`, and `handoff_kind` fields above.

This is a bounded support handoff proposal. It is not a packet family, does not
use `packet_kind`, and does not own objective state, live ticket state,
acceptance, evidence sufficiency, critique verdicts, wiki truth, canonical truth,
or packet lifecycle. Its `handoff_write_scope` describes any proposal-time
mutation permission the parent grants for this handoff; it is separate from Ralph
packet `child_write_scope` and from legacy packet `write_scope` compatibility.

The frontmatter `status` is support-local proposal status for this handoff only:
`draft` means not yet reconciled, `reconciled` means the parent reviewed it and
moved any accepted truth into owner records, `abandoned` means it will not be
used, and `superseded` means a later support handoff replaced it. These statuses
are not canonical record truth, ticket execution state, or shared packet
lifecycle status, and they do not participate in packet transitions such as
`compiled -> consumed`.

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
- Continuity snapshot:
- Drive checkpoint / resume anchor:
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
- optional objective gap summary, only when current owner records do not already
  make the next gap clear
- conditional tranche detail, including included/excluded claims, likely tickets,
  dependencies, handoff write-scope conflict check, evidence/critique gates, and
  reassessment point when those facts are needed for a safe route decision
- gaps or ambiguities that block safe continuation
- proposed owner-record changes
- proposed tickets or ticket refinements
- required evidence and critique posture
- stop conditions or user questions

## Output Contract

- proposed next route: ask_user / workspace_status / records_repair / research /
  spec / plan / ticket / local_edit / ralph / evidence / critique / wiki /
  retrospective / acceptance_review / continue / stop
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
