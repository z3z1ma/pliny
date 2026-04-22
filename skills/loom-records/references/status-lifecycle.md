# Status Lifecycle

Statuses should make a record's age and authority legible without requiring a
runtime.

Tickets keep their own execution state machine in
`skills/loom-tickets/references/state-machine.md`. This reference covers the
normal non-ticket record statuses.

## Universal Vocabulary

- `draft` — proposed but not accepted for downstream use
- `active` — current working truth for that layer
- `accepted` — reviewed or settled enough for downstream use
- `stale` — known to be out of date, but historically useful
- `superseded` — replaced by a named successor
- `retired` — intentionally no longer used

## Layer-Specific Status Sets

Use these sets unless the owning skill records a narrower one:

- constitution: `active | superseded | retired`
- decision: `active | superseded | retired`
- roadmap: `active | superseded | retired`
- initiative: `active | superseded | retired`
- research: `active | concluded | deferred_questions | superseded | retired`
- spec: `draft | active | accepted | superseded | retired`
- plan: `active | superseded | retired`
- wiki: `draft | accepted | stale | superseded | retired`
- packet: `compiled | consumed | superseded | abandoned`
- evidence: `recorded | superseded | invalidated`
- critique: `draft | final | superseded`

## Transition Guidance

Prefer explicit transitions:

- `draft -> active` when a record becomes the current working source
- `draft|active -> accepted` when downstream work can rely on it
- `active|accepted -> stale` when reality changed but no replacement exists
- `active|accepted|stale -> superseded` when a successor is named
- `active|accepted|stale -> retired` when the record should no longer be used

Do not use status as a progress log. Use the body, ticket journal, critique, or
evidence for the details that justify the status.

## Supersession Rule

When setting `status: superseded`, name the successor in `links:` or in a clear
body section.

When setting `status: stale`, say what is stale and what evidence supports that
claim.
