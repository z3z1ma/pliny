# Validation And Honesty

This is an ordered reference for the `using-loom` skill.

Loom is useful only when records are truthful and completion claims mean something.

## Done Means The Graph Tells The Truth

Work is done only when all relevant conditions are true:

- the owning ticket and ticket-owned acceptance decision tell the truth
- acceptance criteria are satisfied or explicitly revised
- required evidence exists and is fresh enough for the exact claim
- required critique gates are satisfied
- retrospective / promotion follow-through happened, was deferred, or is recorded
  as not required
- references are reconciled
- the result stayed within scope

A child assertion, command success, commit, PR, or green feeling is not enough.

## Minimum Validation

Before claiming a bounded step landed, perform the smallest validation that makes
the claim honest: structure, link/reference, and scope checks; behavioral tests or
observed outputs; manual inspection; acceptance comparison; or change-class
evidence.

Freshness matters. If evidence is not from the current source state, say when it
was gathered, what changed since, and why it remains valid; otherwise rerun the
check before claiming completion, fixed, passing, or ready to merge.

## Structural Checks

A record is structurally credible when it has frontmatter; `id`, `kind`,
`status`, `created_at`, and `updated_at`; expected major sections; valid links or
explicit stale/superseded markers; and filename/ID agreement. Ticket states are
live execution states; non-ticket `status` fields are lifecycle states. Use
`skills/loom-records/references/status-lifecycle.md` for shared grammar.

## Ticket Closure Discipline

Use ticket states deliberately:

```text
proposed -> ready | cancelled
ready -> active | blocked | cancelled
active -> blocked | review_required | complete_pending_acceptance | cancelled
blocked -> ready | active | cancelled
review_required -> active | complete_pending_acceptance | cancelled
complete_pending_acceptance -> closed | active | review_required | cancelled
closed/cancelled -> terminal unless explicitly reopened by ticket update
```

Meanings: `proposed` lacks earned readiness; `ready` is clear enough to begin;
`active` is in progress; `blocked` has a real blocker; `review_required` means
critique or acceptance review is next; `complete_pending_acceptance` means work
and evidence are substantially complete but final acceptance or follow-through
remains; `closed` means the graph tells a complete truthful story; `cancelled`
records that work should not proceed and why.

Do not jump to `closed` because a child returned `stop`.

## Reference Reconciliation

When removing, renaming, or superseding anything, search for its canonical ID,
search for path references, reconcile those references, perform the mutation, and
run a final spot-check. Broken graph edges make future recovery slower and less
trustworthy.

## Critique And Wiki Gates

Use these defaults unless the project says otherwise:

- meaningful workflow, behavior, or code changes usually deserve critique
- accepted understanding future agents need should become wiki, not only ticket
  prose
- unresolved open medium/high critique findings prevent full acceptance until the
  ticket owns a disposition
- mandatory critique blocks closure until there is a `final` critique record with
  an explicit verdict, and every open medium/high finding is ticket-dispositioned
  as `resolved`, `accepted_risk`, `superseded`, or `converted_to_follow_up`; a
  draft, stub, deferral, or `not_required` cannot satisfy a mandatory gate
- recommended critique needs a ticket-owned disposition before closure:
  `completed`, `deferred`, or `not_required` with rationale
- optional critique does not block closure unless a ticket, spec, plan, or human
  gate made it required
- withdrawn findings require critique-owned rationale, may be cited for audit,
  and do not block closure merely by severity

## Honesty Rules

Always distinguish evidence from inference, accepted truth from proposed truth,
current blockers from future possibilities, and inspected facts from assumptions.
Name residual risks instead of burying them.

Never claim completion because something probably works, imply critique happened
when it did not, let wiki overstate certainty, let memory become a second ticket
system, or hide scope expansion inside local optimization.

## If Validation Is Incomplete

Say so and leave the graph truthful: record what was validated, what was not, the
remaining risk, the right ticket state, and any needed follow-up. Honesty is not
failure; false completion is failure.
