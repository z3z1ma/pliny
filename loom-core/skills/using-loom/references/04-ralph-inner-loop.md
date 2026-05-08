# Ralph Inner Loop

This is an ordered reference for the `using-loom` skill.

Ralph is Loom's implementation loop: one packet, one fresh worker, one bounded
iteration, one truthful parent reconciliation.

Use Ralph when a ticket delegates implementation-sized work and the next mutation
needs explicit scope, write boundaries, stop conditions, verification posture, and
output. Do not use it to make ordinary local cleanup ceremonial; do use it when
continuing in chat would make execution less auditable or safe.

## Parent And Child

The parent owns the live workflow. It reads the governing records, decides that
Ralph is the next move, compiles the packet, chooses style, write boundary, and
verification posture, launches or hands off the worker, inspects the return, and
reconciles truth into the ticket and any other owner layer that must change.

The child owns only the iteration. It reads the packet fully, stays inside the
declared scope and write boundary, performs the bounded task, stops when a stop
condition applies, and reports outcome, changed files, evidence, blockers,
residual risks, and recommendation. A packet can authorize edits only inside its
scope; it cannot make the child owner of the ticket, spec, plan, critique, wiki,
or whole project.

## Routing Boundary

Ralph is for packetized implementation. Critique and wiki may reuse packet
discipline, but the domain route activates first: critique packets are owned by
the critique workflow, wiki packets by the wiki workflow. Route by the truth being
changed, then choose packetization if fresh context or a bounded handoff helps.

## Packet Contract

A Ralph packet is a replayable contract, not project truth. It should make these
facts explicit:

- target ticket and governing hierarchy
- iteration mode, packet style, change class, and verification posture
- allowed reads and writes
- source snapshot or fingerprint, expected execution context, and context budget
- task for this iteration, progress definition, stop conditions, and blocked path
- output contract and what the parent must reconcile

The body normally includes `Mission`, `Bound Context`, `Source Snapshot`, `Change
Class`, `Task For This Iteration`, `Stop Conditions`, `Output Contract`, `Working
Notes`, `Child Output`, and `Parent Merge Notes`. Keep packet contents bounded:
enough for a fresh worker to act without guessing, not a transcript dump.

A packet may also serve as a working pad for parent notes, selected child output,
stale-assumption markers, and supersession breadcrumbs. That history helps
replay the iteration without turning packets into the canonical ledger.

## Style And Verification

Packet style controls how much context the packet carries.

- `reference-first`: points to canonical records with only key excerpts; use when
  the worker can read the workspace and brevity is valuable.
- `snapshot-first`: includes curated excerpts and summaries; use when the parent
  wants more context carried in the packet.
- `hermetic`: tries to carry everything practical and limits outside reads; use
  when replayability, portability, or stricter trust boundaries matter most.

Verification posture is separate and is chosen per packet.

- `test-first`: produce a failing check before implementation and drive it green
  inside the iteration. Use when behavioral acceptance can be exercised.
- `observation-first`: observe current behavior before changing it and observe the
  new behavior after. Use when automated tests are impractical but evidence must
  still be inspectable.
- `none`: use only for genuinely verification-neutral work such as structural
  record hygiene or packet compilation.

Do not use `none` merely because the change is Markdown. Protocol, workflow,
operator guidance, acceptance, and completion edits often need structural
evidence, observation-first evidence, or critique. The posture belongs in packet
frontmatter so neither child nor parent can silently change the evidence bar.

## Outcomes And Reconciliation

The child returns exactly one outcome:

- `continue`: meaningful progress happened and another bounded pass is likely
- `stop`: this iteration is complete and another Ralph pass may not be needed
- `blocked`: a concrete blocker prevented progress
- `escalate`: higher-order reframing, review, or policy work is the right next move

After return, the parent may accept and continue, route to critique or wiki,
revise the ticket and compile a new packet, loop back to research/spec/plan, or
reject the iteration for scope or truth-boundary violations. The child's
recommendation is evidence for the parent; it is not the acceptance decision.

## Freshness, Parallelism, And Closure

Reuse a packet only while the target ticket, governing records, scope, allowed
write boundary, source fingerprint, and intended iteration remain materially the
same. If they drift, compile a fresh packet instead of asking the child to infer
what changed. After reconciliation, the parent should move the packet away from
`compiled` to `consumed`, `superseded`, or `abandoned`.

Parallel Ralph is safe only when tickets have no dependency conflict and packet
write scopes do not overlap. Shared migrations, generated files, lockfiles,
stateful resources, or ambiguous ownership require sequential execution or more
planning.

A Ralph run is not complete because the child says done. It is complete only when
the ticket and supporting evidence truthfully record what happened, required
claims are routed to their owning layers, and packet-only knowledge has not become
shadow truth.
