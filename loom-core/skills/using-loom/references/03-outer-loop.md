# Outer Loop

This is an ordered reference for the `using-loom` skill.

The outer loop is Loom's scoping and framing engine. It makes work small enough,
clear enough, and honest enough that execution does not require guessing.

## The Outer Loop Questions

Before compiling a packet, coding, or choosing a route, answer what durable
problem exists, which layer owns it, what larger frame constrains it, what
evidence or behavior is missing, whether planning is needed, and what the next
bounded ticket-sized step is.

If those cannot be answered, stay in the outer loop.

## Routing Progression

Default backbone:

`constitution -> initiative -> plan -> ticket`

Route by changing truth:

- **constitution**: principles, identity, hard constraints, citable decisions
- **initiative**: strategic outcome framing or cross-cutting ownership
- **research**: evidence, tradeoffs, rejected options, investigations, conclusions
- **spec**: intended behavior, reusable acceptance, scenarios, requirements
- **plan**: high-level decomposition, sequencing, dependencies, rollout,
  milestones, execution waves
- **ticket**: one bounded live execution owner

Not every task needs every layer, but nontrivial work should fit this model.

## Ticket Readiness Standard

A ticket is ready only when a fresh worker or reviewer can identify the next
governed move without transcript context. Ralph-ready is stricter: it also names
one bounded implementation iteration, write boundary, likely verification
posture, and expected output contract.

A ready ticket makes these legible:

- why this work matters now
- what is in scope
- what is out of scope
- what acceptance means
- what artifacts constrain the work
- what evidence the parent will expect
- blockers, evidence gaps, critique gaps, acceptance gaps, or journal facts a
  fresh agent should inspect
- whether packaging or handoff is needed, without treating shipping as ticket
  closure

If the ticket cannot do that, keep working in the outer loop.

## Research, Spec, And Plan Triggers

Use **research** for weak evidence, material tradeoffs, assumptions that would
enter a spec/plan, or citable discoveries. Use a **spec** for underspecified
behavior, vague acceptance, divergent plausible implementations, or stable
behavior sources needed by critique/wiki. Use a **plan** when the work is too
complex for one ticket, order or rollout matters, dependencies exist, or future
tickets need waves/milestones. Research ends rediscovery; specs state intended
behavior; plans own high-level shape, not execution minutiae.

## Decomposition Rule

Keep decomposing until the next step fits one shape:

- one tiny local execution step with no packet
- one `ralph` implementation packet
- one workflow-coordinator pass such as `debugging`, `spike`, `codemap`, or
  `ship`
- one critique pass
- one wiki pass
- one owner-layer refinement or review pass

If the current state needs operator input, workspace repair, records repair,
evidence preservation, continuation, or stop, handle that need directly in the
owner layer instead of forcing another implementation pass.

If the next step still feels like "do the whole feature," it is not decomposed
enough.

## Loopback From Ralph

If Ralph returns ambiguous behavior, missing evidence/strategy/constraints, a
too-wide ticket, or unexpected scope growth, go outward instead of forcing
execution through ambiguity. Common loopbacks:

- Ralph -> research when evidence or tradeoffs are missing
- Ralph -> spec when intended behavior is ambiguous
- Ralph -> plan when the high-level execution shape or sequencing is wrong
- Ralph -> ticket refinement when the execution owner is too wide or stale
- Ralph -> initiative when objective or autonomy framing was missing
- Ralph -> constitution in rare architectural or policy cases

## Consult Constitution Before Deciding

Before a nontrivial architectural or policy choice, check whether constitution,
decision, or roadmap records already speak to it. They are precedent, not
history.

Typical checks:

- `rg -n '^id:' .loom/constitution` to list the current constitutional surface
- `find .loom/constitution/decisions -name '*.md' | sort` to scan prior decisions
- `rg -n '<topic>' .loom/constitution` to see whether this topic already has policy

If constitutional truth applies, inherit it. If the work contradicts it, amend
policy explicitly or change the work, not silently both.

## Strategic Restraint

Clarify without over-architecting. Do not create records for ceremony. Create
them when a future agent would genuinely need them to reduce ambiguity, improve
safety, preserve understanding, or choose the next bounded move.
