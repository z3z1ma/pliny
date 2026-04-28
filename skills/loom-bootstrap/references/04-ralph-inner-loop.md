# Ralph Inner Loop

This is an ordered bootstrap reference for the `loom-bootstrap` skill.

Ralph is Loom's implementation loop.

It exists to make execution reliable by using:

- fresh context
- bounded packets
- explicit scope
- explicit write boundaries
- explicit stop conditions
- explicit output contracts
- parent-side reconciliation

## Ralph In One Sentence

One packet, one fresh worker, one bounded iteration, one truthful merge.

A parent frames the next bounded mutation, a packet declares the
read/write/stop/output contract, a fresh worker executes one slice, and the
parent reconciles the result back into ticket truth and any other owner layer
that needs to change.

## Parent And Child Roles

### Parent owns

- deciding whether Ralph is actually the next move
- reading the governing records
- compiling the packet
- choosing the packet style
- choosing the write boundary
- launching or delegating the fresh worker
- inspecting what came back
- merging truth into the ticket
- routing into critique or wiki next or another Ralph iteration if needed

### Child owns

- reading the packet fully
- doing one bounded step
- staying inside the declared scope
- staying inside the declared write boundary
- reporting outcome, evidence, blockers, and next recommendation
- updating allowed artifacts only if the packet grants that authority

The child does not own the whole workflow.
The child owns one iteration.

## When Ralph Is Required

Ralph is required when:

- a ticket delegates a bounded implementation mutation to a fresh worker
- the write boundary must be explicit for safety, auditability, or parallel work
- parent and child authority need a replayable contract

Ralph is recommended when:

- the next step is implementation-sized
- the ticket names one bounded implementation iteration
- the task benefits from fresh context
- the write boundary should be explicit
- a packet would reduce ambiguity
- the parent wants a replayable contract

Do not call critique or wiki work Ralph merely because it uses packet discipline;
those are critique/wiki routes.

You do not need Ralph for every small local note edit.
You do need Ralph whenever "just continue in the same transcript" would make the work sloppier or less auditable.

## Packetized Sibling Work

Critique and wiki work may use packet discipline, but the domain skill activates
first.

- critique packets are owned by the critique workflow
- wiki packets are owned by the wiki workflow
- Ralph owns packetized implementation and the parent/child execution discipline
  those workflows may reuse

Do not route a review or synthesis pass to Ralph just because it uses a packet.
Route by the truth being changed, then choose packetization if fresh context or a
bounded handoff would improve the work.

## Packet Anatomy

Every Ralph packet should answer these questions:

1. what exact target owns this iteration
2. what larger hierarchy constrains it
3. what mode and style is being used
4. what change class is being mutated
5. what the worker may read
6. what the worker may write
7. what the parent must reconcile
8. what source version the packet was compiled against
9. what execution context is expected
10. what context budget the worker should use
11. what counts as progress
12. what should happen if the worker gets blocked
13. what output the parent expects back

The packet body should normally include:

- Mission
- Bound Context
- Source Snapshot
- Change Class
- Task For This Iteration
- Stop Conditions
- Output Contract
- Working Notes
- Child Output
- Parent Merge Notes

## Packet Styles

### Reference-first

The packet points heavily at canonical records and gives only the most important excerpts.

Use when the worker can read the workspace and the parent wants a smaller packet.

### Snapshot-first

The packet includes more curated excerpts and summaries of the important source records.

Use when the parent wants the packet to carry more of the necessary context explicitly.

### Hermetic

The packet aims to contain everything the child should need and limits dependency on outside reads as much as practical.

Use when replayability, portability, or stricter trust boundaries matter more than packet brevity.

## Verification Posture

Packet style governs how much context is carried. Verification posture is a separate axis that governs how the child evidences the iteration. The parent chooses posture per packet, not per ticket — a test-first ticket can still have a refactor-only iteration that does not demand a new failing check.

Default postures:

### `test-first`

The child must produce a failing check (failing test, failing assertion, failing observed behavior) *before* any implementation change, and drive it to green inside this iteration. This is Loom's native shape for TDD: red first, green second, both inside one packet.

Use when the spec or acceptance criteria name a behavioral outcome that can be exercised. The stop conditions must include "a failing check exists, fails for the expected reason, and has been driven to green," and the output contract must carry evidence of both the red and green states.

### `observation-first`

The child must produce observed, inspectable evidence of current behavior before changing it, and produce observed evidence of the new behavior after. Use when automated checks are impractical or premature but the iteration still needs something concrete: a logged output, a captured artifact, a diffed behavior.

### `none`

No explicit verification beyond the normal output contract. Use only when the iteration is genuinely verification-neutral: non-semantic record hygiene, reference reconciliation, packet compilation, or another change whose correctness is structural rather than behavioral.

Do not use `none` merely because a change is written in Markdown. Protocol,
workflow, operator guidance, acceptance, or behavior-contract edits can change
how Loom behaves and usually need structural evidence, observation-first evidence,
or critique.

### Choosing posture

- if the spec or ticket names behavioral acceptance, default to `test-first`
- if behavior is observable but not yet testable, default to `observation-first`
- if the change affects protocol authority, completion, routing, or operator
  behavior, default to structural evidence plus critique unless a stricter
  posture is named
- if the iteration does not change behavior, `none` is honest

The posture is declared in the packet frontmatter so the child cannot quietly skip it and the parent cannot retroactively pretend it was demanded. Verification discipline is a property of the contract, not a property of the prose.

## Child Outcome Vocabulary

The child should return one of:

- `continue` — meaningful progress happened and another Ralph iteration is likely next
- `stop` — this bounded iteration is finished and Ralph may not be the next route
- `blocked` — a concrete blocker prevented progress
- `escalate` — the right next step is higher-order reframing, review, or policy work

The child should also return:

- changed files or records
- evidence gathered
- blockers or residual risks
- recommendation for the ticket state

## Parent Decision After Return

After a Ralph run, the parent decides among:

- accept the iteration and continue
- accept the iteration and route to critique
- accept the iteration and route to wiki
- revise the ticket and compile a new Ralph packet
- route back to research/spec/plan because the outer loop was incomplete
- reject the iteration because scope or truth discipline was violated

The child's recommendation matters.
The parent's reconciliation authority still matters more.

## Packet Reuse Rule

Reuse a packet only if all of these are still true:

- the target ticket has not changed materially
- the governing records have not changed materially
- the scope has not changed materially
- the allowed write boundary has not changed materially
- the intended iteration is still the same iteration

If any of those drifted, compile a fresh packet.

Before launch, compare the packet's source fingerprint with the governing
records and child-write-scope files. If they changed materially, supersede the
packet instead of asking the child to guess.

After reconciliation, parent should move packet status away from `compiled` to
`consumed`, `superseded`, or `abandoned`.

## Parallel Ralph Rule

Parallel Ralph is allowed only when tickets have no dependency conflict and
packet child write scopes do not overlap.

If shared migrations, generated files, lockfiles, stateful resources, or
ambiguous ownership could make two packets interfere, run them sequentially or
return to planning.

## The Working Pad Principle

A Ralph packet is not just a launch artifact.

It is also a working pad.

The parent can:

- append new notes
- carry forward selected child output
- mark stale assumptions
- supersede one packet with the next

That makes the iteration history inspectable without turning packets into the canonical ledger.

## The Closure Rule

A Ralph run is not complete because the child said "done".

It is complete only when the ticket and supporting evidence tell the truth about what actually happened.

If the child surfaced a durable claim, behavior change, evidence artifact, risk,
or explanation, the parent must route it to the layer that owns that kind of truth
instead of leaving it only in the packet or transcript.
