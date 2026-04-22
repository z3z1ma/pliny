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

- `compiled -> consumed`: child output returned and parent merge notes were
  written
- `compiled -> superseded`: governing records, source fingerprint, scope, or
  child write scope changed before launch
- `compiled -> abandoned`: packet will not be launched and no successor is
  intended
- `consumed -> superseded`: a later packet or owner correction invalidated the
  result

After reconciliation, parent should update packet status away from `compiled`.
