# Ticket State Machine

This reference owns ticket lifecycle states: the live execution ledger values for
ticket records. Do not use ticket states as route tokens or non-ticket record
statuses. Route tokens are owned by
`skills/loom-records/references/route-vocabulary.md`; non-ticket record statuses,
packet statuses, and disposition vocabulary boundaries are summarized in
`skills/loom-records/references/status-lifecycle.md`.

## Normal states

- `proposed`
- `ready`
- `active`
- `blocked`
- `review_required`
- `complete_pending_acceptance`
- `closed`
- `cancelled`

## Normal Transitions

```text
proposed -> ready | cancelled
ready -> active | blocked | cancelled
active -> blocked | review_required | complete_pending_acceptance | cancelled
blocked -> ready | active | cancelled
review_required -> active | complete_pending_acceptance | cancelled
complete_pending_acceptance -> closed | active | review_required | cancelled
closed/cancelled -> terminal unless explicitly reopened by ticket update
```

## Heuristics

### `ready`

Use when the ticket is clear enough to begin.

### `proposed`

Use when the ticket exists but readiness has not been earned yet.

### `active`

Use when the bounded execution is underway.

### `blocked`

Use when a concrete blocker exists and is named.

### `review_required`

Use when implementation landed and critique/acceptance review is clearly next.

### `complete_pending_acceptance`

Use when the work and evidence are mostly complete but final acceptance or final follow-through remains.

### `closed`

Use only when the story is truthful and complete.

### `cancelled`

Use when the work should not proceed and the cancellation reason is recorded.

## Anti-pattern

Do not use `closed` as a synonym for "I think the coding part is done."

Do not use `review_required`, `complete_pending_acceptance`, or `closed` as a
`next route:` value. If review, acceptance, or shipping is next, name the route
token such as `critique`, `acceptance_review`, or `ship` and keep the ticket
state truthful separately.
