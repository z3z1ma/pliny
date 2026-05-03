# Status Lifecycle

This reference is the canonical shared source for Loom lifecycle status and
disposition vocabulary. Statuses should make a record's age and authority
legible without requiring a runtime enum, schema, validator, or command router.

Tickets keep their own execution state machine in
`skills/loom-tickets/references/state-machine.md`. Route tokens live in
`skills/loom-records/references/route-vocabulary.md`. This reference covers the
normal non-ticket record statuses plus boundary guidance for packet statuses,
finding states, and ticket-owned dispositions.

## Common Cross-Layer Status Words

These words are common across several layers. They are not the complete status
vocabulary; layer-specific status sets below are authoritative for each kind.

- `draft` — proposed but not accepted for downstream use
- `active` — current working truth for that layer
- `completed` — successful outcome reached; retained as historical owner truth
- `accepted` — reviewed or settled enough for downstream use
- `stale` — known to be out of date, but historically useful
- `superseded` — replaced by a named successor
- `retired` — intentionally no longer used

## Disposition And Acceptance Vocabulary Boundaries

Status, finding state, critique disposition, and acceptance decision are related
but not interchangeable.

- **Route tokens** such as `constitution`, `initiative`, `research`, `ralph`,
  `critique`, `continue`, and `stop` live in route fields and name the next
  governed move. They are not lifecycle statuses. When a Ralph child returns an
  outcome such as `continue`, `stop`, `blocked`, or `escalate`, the parent must
  reconcile it into ticket truth and translate it into the next owner-truth route
  before any route field treats it as routing truth.
- **Critique-owned finding state** lives inside critique records. Use `open` for a
  finding that remains part of the review output, or `withdrawn` when the
  critique itself retracts the finding with rationale. Critique records also own
  verdicts, severity, confidence, residual risks, and required follow-up. Only
  open medium/high findings require ticket-owned finding dispositions before
  closure. Withdrawn findings require critique rationale and may be cited by the
  ticket for audit history, but they are not closure-blocking merely because of
  severity.
- **Ticket-owned finding disposition** lives in the ticket's
  `# Critique Disposition` section for each qualified finding reference. Use
  `resolved`, `accepted_risk`, `superseded`, or `converted_to_follow_up`.
- **Ticket-owned critique disposition status** describes gate progress for the
  ticket as a whole: `pending`, `blocking`, `completed`, `deferred`, or
  `not_required`.
- **Ticket-owned acceptance decision** owns closure provenance and residual risk.
  A critique verdict, packet result, drive checkpoint, or support handoff may
  recommend a route, but it does not accept or close ticket work.

These vocabulary sets are Markdown protocol grammar. Do not turn them into a
required runtime enum, schema, validator, command router, or new owner layer.

Drive and checkpoint snapshots may summarize critique and acceptance state only by
citing the ticket and critique records that own it. They must not become a second
acceptance ledger.

## Canonical Owner Record Statuses

Use these sets for canonical owner records unless the owning skill records a
narrower one:

- constitution: `active | superseded | retired`
- decision: `active | superseded | retired`
- roadmap: `active | completed | superseded | retired`
- initiative: `active | completed | superseded | retired`
- research: `active | concluded | deferred_questions | superseded | retired`
- spec: `draft | active | accepted | superseded | retired`
- plan: `active | completed | superseded | retired`
- evidence: `recorded | superseded | invalidated`
- critique: `draft | final | superseded`
- wiki: `draft | accepted | stale | superseded | retired`

## Ticket Execution States

Tickets are canonical owner records, but their `status` field is a live execution
state rather than a general lifecycle status. Use the ticket state machine in
`skills/loom-tickets/references/state-machine.md` for ticket statuses such as
`proposed`, `ready`, `active`, `blocked`, `review_required`,
`complete_pending_acceptance`, `closed`, and `cancelled`.

Do not copy non-ticket lifecycle words into ticket `status` fields, and do not
use ticket execution states as route tokens.

## Support-Surface Statuses

Support surfaces may carry local lifecycle status, but those statuses do not make
the support surface a canonical truth owner.

- packet: `compiled | consumed | superseded | abandoned`
- workspace metadata records with `kind: workspace`:
  `active | stale | superseded | retired`
- workspace support records with `kind: workspace-support`:
  `active | superseded | retired`
- saved drive outer-loop handoff support artifacts:
  `draft | reconciled | abandoned | superseded`
- memory support files: lightweight local status is optional; when used, prefer
  retrieval-oriented values such as `active`, `stale`, `superseded`, or
  `retired`, and do not let memory status own canonical project truth, live
  execution state, evidence sufficiency, or accepted explanation. Validators
  should not require memory files to have a `status` field.
- support artifacts and handoff templates: any `status` field is support-local
  unless the owning skill says otherwise; it does not own objective state, live
  ticket state, acceptance, evidence sufficiency, critique verdicts, wiki truth,
  canonical truth, or packet lifecycle status

Packet records are the support-surface exception: their `status` field owns only
their own packet lifecycle state. Ralph, critique, and wiki packets share the
packet status values below, while `packet_kind` and the owning workflow keep body
shape, route ownership, and merge responsibilities separate.

Support artifacts saved under optional `.loom/support/` paths are
lazy-materialized support files. Their statuses are local to the artifact and do
not make `.loom/support/` a canonical owner layer or packet lifecycle surface.

Workspace metadata records such as `.loom/workspace.md` may use `status: active`
when the workspace aliases, repository scope notes, or local orientation metadata
are current. Use `stale` when that metadata is known to be out of date but still
useful, `superseded` when a named replacement exists, and `retired` when the
workspace metadata file should no longer be used. The `kind: workspace` lifecycle
describes metadata currency only; it does not own project identity, objective
state, live ticket state, acceptance, evidence sufficiency, critique verdicts,
wiki truth, canonical truth, or packet lifecycle.

## Layer-Specific Meanings

- `concluded` — research has reached evidence-bounded conclusions or recommendations.
- `deferred_questions` — research is intentionally preserving open questions without claiming conclusions.
- `recorded` — evidence has captured an observation and can be cited with its stated limitations.
- `invalidated` — evidence should no longer be used because its procedure, environment, or artifact is known to be false or obsolete.
- `final` — critique has completed its review surface and can be consumed by ticket disposition.
- `reconciled` — a support handoff has been reviewed by the parent and any
  accepted content has been moved into the owner records that actually own the
  truth.
- `abandoned` — a support handoff or packet will not be used and no successor is
  intended. For support artifacts, this is support-local only and does not affect
  packet lifecycle.

## Transition Guidance

Prefer explicit transitions:

### Canonical Owner Transitions

- `draft -> active` when a record becomes the current working source
- `draft|active -> accepted` when downstream work can rely on it
- `active -> completed` when an initiative, plan, or roadmap reached its
  intended success or exit criteria
- `active|accepted -> stale` when reality changed but no replacement exists
- `active|accepted|completed|stale -> superseded` when a successor is named
- `active|accepted|completed|stale -> retired` when the record should no
  longer be used
- `active -> concluded|deferred_questions` when research has either answered
  the question or intentionally preserved unanswered questions
- `recorded -> invalidated` when later observation shows the evidence should no
  longer support its claims
- `draft -> final` when critique findings, verdict, evidence reviewed, residual
  risks, and acceptance recommendation are complete

### Support-Surface Transitions

- workspace metadata: `active -> stale` when workspace aliases or scope notes are
  no longer current, `active|stale -> superseded` when a named replacement takes
  over, and `active|stale -> retired` when the metadata file should no longer be
  used
- support-local drive handoffs: `draft -> reconciled` after parent merge,
  `draft -> abandoned` when not used, or `draft|reconciled -> superseded` when a
  later handoff replaces the support artifact. A saved handoff may also be pruned
  after parent review when accepted content has been reconciled into the declared
  owner records and no support audit or recovery value remains; pruning is cleanup,
  not a lifecycle status and not evidence that owner truth was accepted.

Packet transitions are listed separately below because packet records own their
own support lifecycle.

Do not use status as a progress log. Use the body, ticket journal, critique, or
evidence for the details that justify the status.

## Completed Is Not Retired

Use `completed` when a roadmap, initiative, or plan succeeded and should remain
readable as the finished strategic owner.

Use `retired` when the record is intentionally no longer used even if it did
not succeed, or when the project has decided not to pursue it.

## Supersession Rule

When setting `status: superseded`, name the successor in `links:` or in a clear
body section.

When setting `status: stale`, say what is stale and what evidence supports that
claim.

## Packet Transitions

Use packet statuses as operational state, not as archival decoration. This
packet lifecycle is packet-record-owned support state and applies to current
Ralph, critique, and wiki packet families; `packet_kind` still decides which
workflow owns the packet body and route.

Packet terminal statuses are `consumed`, `superseded`, and `abandoned`.
`compiled` is non-terminal and means the packet is ready for launch or pending
parent action.

- `compiled -> consumed`: child output returned and parent merge notes were
  written
- `compiled -> superseded`: governing records, source fingerprint, scope, or
  child write scope changed before launch
- `compiled -> abandoned`: packet will not be launched and no successor is
  intended
- `consumed -> superseded`: a later packet or owner correction invalidated the
  result

After reconciliation, parent should update packet status away from `compiled`.
When a launched child result is rejected, corrupted, stale, or overscoped, the
packet still needs an honest terminal status plus parent merge notes; do not let
the status imply acceptance unless the ticket and owning records actually accept
the result.

When discovering an old `compiled` packet, treat the query result as a launch
safety warning, not as proof of staleness. Read the packet, compare its target,
source fingerprint, governing records, child write scope, and intended iteration
against current owner truth, and then choose the packet-owned disposition:

- leave `compiled` only when the same launch contract is still fresh enough
- change to `superseded` when a corrected packet replaces the stale contract
- change to `abandoned` when no successor is intended

Packet status remains support-state only. It does not own ticket execution,
acceptance, evidence sufficiency, critique verdicts, or next route, and it does
not require a runtime enum, schema, validator, generated index, merge script, or
new reconciliation record kind.
