# Outer-Loop Subagent Transport

This reference supports the `loom-drive` skill.

Use it only when optional outer-loop subagent transport is relevant. Normal
`loom-drive` activation does not require reading this reference, and the handoff
template remains conditional rather than part of the normal read order.

## Transport Boundary

A dedicated outer-loop subagent may help with context management when the parent
needs fresh synthesis of an objective chain, option set, tranche plan, or risk
list.

This is transport only:

- the subagent proposes owner-record changes, tickets, risks, and next routes
- the parent reviews the output before applying it
- canonical records retain truth ownership
- tickets retain live execution ownership
- parent reconciliation remains mandatory before dependent work launches

The parent must reconcile accepted results into the owner layer that owns that
truth. Do not depend on subagent output, launch dependent work, close tickets, or
treat evidence, critique, wiki, acceptance, or next-route claims as accepted
until that reconciliation happens.

## Saved Handoff Support Surface

The outer-loop handoff template is prompt-only by default. Save it only when a
durable support artifact is useful for reviewability, context recovery, or
handoff audit.

Saved outer-loop handoffs live under the optional, lazy-materialized,
non-canonical support surface
`.loom/support/drive-handoffs/<UTC compact timestamp>-<slug>.md` with
`kind: support-artifact`, `support_kind: drive-outer-loop-handoff`, and
`handoff_kind: outer-loop-synthesis`.

Do not create `.loom/support/` merely during bootstrap. Create it only when a
saved support artifact is intentionally materialized.

## Handoff Metadata Semantics

Saved handoff status is support-local: `draft`, `reconciled`, `abandoned`, or
`superseded`. It does not own objective state, live ticket state, acceptance,
evidence sufficiency, critique verdicts, wiki truth, canonical truth, or packet
lifecycle.

The outer-loop handoff template is not a packet family and not a truth owner. It
does not use `packet_kind`, does not participate in packet transitions such as
`compiled -> consumed`, and does not replace Ralph packet contracts.

Any handoff `handoff_write_scope` is proposal-time permission for that support
handoff, not Ralph `child_write_scope`. Legacy packet `write_scope` remains
packet compatibility only.

If any handoff metadata claim becomes durable project truth, move it into the
owner layer that owns that truth and leave the handoff as a support artifact.

## Template Use

Use `templates/outer-loop-handoff.md` only when a bounded handoff would reduce
context pressure or improve reviewability.
