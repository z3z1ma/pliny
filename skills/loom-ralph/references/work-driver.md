# Work Driver

The work driver moves one ticket through bounded Ralph iterations and parent
reconciliation.

It is not "just code." It is ticket-owned execution.

## Inputs

- ticket
- linked plan, spec, research, and initiative as needed
- acceptance criteria and coverage targets
- evidence expectations
- critique and retrospective / promotion disposition

## Procedure

1. Anchor to one ticket.
2. Read the smallest governing chain needed.
3. Check Ralph-readiness: one bounded implementation iteration, write boundary,
   likely verification posture, and output contract are explicit.
4. Move the ticket to `active` only when work is genuinely starting.
5. For Git-backed file changes, use `skills/loom-git/SKILL.md` to resolve the
   integration baseline and choose branch/worktree isolation before launch.
6. Compile a Ralph packet with child write scope, parent merge scope, source
   fingerprint, Git execution context when relevant, context budget,
   verification posture, stop conditions, and output contract.
7. Launch the bounded iteration through the available harness transport.
8. Reconcile the child output as parent. Do this as a ticket-owned merge, not as
   a new reconciliation record kind:
   - compare the child outcome to the packet mission, stop conditions, output
     contract, verification targets, and verification posture
   - check scope discipline, child write boundary, and absence of forbidden
     machinery or owner-layer drift
   - check Git diff against the declared write scope when files changed
   - preserve observed red/green, before/after, structural, or skipped
     verification evidence in the evidence layer when the ticket will rely on it
   - translate the child recommendation into ticket journal, claim coverage,
     critique/wiki disposition, next route, and status; the child outcome does not
     set those fields by itself
   - update packet parent merge notes and move packet status away from `compiled`
     only after the ticket and any required evidence or critique records tell the
     truth
9. Decide the next route using
   `skills/loom-records/references/route-vocabulary.md` as the complete saved
   route grammar. Common execution-side outcomes include:
   - `ralph` for another bounded implementation packet
   - `debugging`, `spike`, or `codemap` when diagnosis, discovery, or mapping
     should happen before more implementation
   - `critique` when review is next
   - `wiki` or `retrospective` when accepted learning should be promoted
   - `research`, `spec`, `plan`, or `ticket` for owner-layer refinement
   - `acceptance_review` for ticket-owned acceptance evaluation
   - `ship` for packaging already-truthful work without closing the ticket

   This list is illustrative, not exhaustive. If the current state needs operator
   input, workspace repair, records repair, evidence preservation, continuation,
   or stop, choose that route instead of forcing another implementation route.

## Stop States

- `blocked`: a named blocker exists
- `review_required`: critique is next
- `complete_pending_acceptance`: work and evidence are largely complete
- never mark `closed` from work execution

## Guardrails

- Do not execute without a ticket owning live state.
- Do not force Ralph from a merely proposed or generally ready ticket; route back
  to ticket/spec/plan refinement when Ralph-readiness is missing.
- Do not let a packet outrank the ticket or owner records.
- Do not let a branch, worktree, commit, or PR replace ticket truth.
- Do not widen scope because a nearby fix looks easy.
- The child may recommend ticket updates; the parent commits ticket truth.
- Do not let packet parent merge notes become the execution ledger; they support
  ticket reconciliation and packet lifecycle only.
