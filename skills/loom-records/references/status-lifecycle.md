# Status Lifecycle

Statuses should make a record's age and authority legible without requiring a
runtime.

Tickets keep their own execution state machine in
`skills/loom-tickets/references/state-machine.md`. This reference covers the
normal non-ticket record statuses.

## Universal Vocabulary

- `draft` — proposed but not accepted for downstream use
- `active` — current working truth for that layer
- `completed` — successful outcome reached; retained as historical owner truth
- `accepted` — reviewed or settled enough for downstream use
- `stale` — known to be out of date, but historically useful
- `superseded` — replaced by a named successor
- `retired` — intentionally no longer used

## Layer-Specific Status Sets

Use these sets unless the owning skill records a narrower one:

- constitution: `active | superseded | retired`
- decision: `active | superseded | retired`
- roadmap: `active | completed | superseded | retired`
- initiative: `active | completed | superseded | retired`
- research: `active | concluded | deferred_questions | superseded | retired`
- spec: `draft | active | accepted | superseded | retired`
- plan: `active | completed | superseded | retired`
- wiki: `draft | accepted | stale | superseded | retired`
- packet: `compiled | consumed | superseded | abandoned`
- evidence: `recorded | superseded | invalidated`
- critique: `draft | final | superseded`
- workspace support records: `active | superseded | retired`
- memory support files: lightweight local status is optional; when used, prefer
  retrieval-oriented values such as `active`, `stale`, `superseded`, or
  `retired`, and do not let memory status own canonical project truth
- support handoff templates: any `status` field is template-local unless the
  owning skill says otherwise; it does not create canonical truth, ticket state,
  or packet lifecycle status

## Layer-Specific Meanings

- `concluded` — research has reached evidence-bounded conclusions or recommendations.
- `deferred_questions` — research is intentionally preserving open questions without claiming conclusions.
- `recorded` — evidence has captured an observation and can be cited with its stated limitations.
- `invalidated` — evidence should no longer be used because its procedure, environment, or artifact is known to be false or obsolete.
- `final` — critique has completed its review surface and can be consumed by ticket disposition.

## Transition Guidance

Prefer explicit transitions:

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

Use packet statuses as operational state, not as archival decoration:

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
