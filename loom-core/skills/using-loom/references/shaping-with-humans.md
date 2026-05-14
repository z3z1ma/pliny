# Shaping With Humans

Before execution, the agent and operator shape the work until the next move is
small, clear, bounded, and honest. This outer loop is the core premise of Loom,
not a prelude to skip when implementation looks available.

Unless the operator's ask is concrete enough to act without hidden design choices,
the required first goal is to pinpoint ambiguity with the human. Do not skip this
because a patch or ticket looks easy to infer.

## Concrete Ask Gate

A fuzzy ask is not an implementation brief. Do not collapse broad, aspirational,
or under-specified requests into execution before the shaping work is done.

Treat a request as concrete only when these are already clear enough to act on
without choosing direction silently:

- operator or user outcome
- target surface, code area, workflow, or artifact
- scope boundary and important non-goals
- source, product, policy, or system constraints
- system-shape, data model, state, data-flow, or abstraction implications
- quality bar, success criteria, and non-examples
- evidence posture or observable proof path
- ticket, plan, spec, research, or other next Loom surface

If any of those are missing and would materially change what gets built, the next
move is mandatory shaping:

- inspect source and Loom records before asking what they already answer
- name the specific ambiguity or hidden choice
- ask one material question or offer two or three materially different options
- recommend a path when the tradeoff is clear
- preserve the resolved truth in the surface that owns it

Concrete enough does not mean the operator supplied every implementation detail.
It means the remaining choices are local execution choices inside an accepted
direction, not hidden direction, system-shape, data-model, state, or coherence
decisions.

## Outer Loop Posture

Inspect first. Do not ask the operator to restate what the repository or Loom
records can answer.

Then summarize only what gives the operator leverage:

- what you found
- what you think the real problem is
- which surface appears to own the next truth change
- what is unclear, risky, or stale
- what options exist
- which path you recommend and why

Compress the context into a useful decision point.

## Shape Vague Work Into Decisions

Broad requests are normal outer-loop inputs. Treat umbrella requests, quality
adjectives, and large verbs as invitations to identify the real decision behind
the words.

The objective is not to collect enough text to justify immediate implementation.
The objective is to locate the product, behavior, system-shape, workflow,
evidence, or scope ambiguity that would make an implementation guess unsafe.

Shape the hard parts explicitly:

- which outcomes belong in this direction
- which adjacent outcomes are deliberately excluded
- which system seams, data model, or state relationships the work implies
- how the pieces should fit together as one design
- what would make the design incoherent even if the code runs
- which surface should own each resulting decision before execution depends on it

Before writing durable artifacts or executing from them, shape the decision points
that affect the work:

- the user or operator outcome
- the quality bar and non-examples
- the meaningful non-goals
- the source, product, policy, or system constraints
- the domain model, data relationships, state relationships, and abstraction boundaries
- the evidence that would make success believable
- the ticket boundary or plan decomposition that would make execution bounded

When several directions are plausible, offer a small set of materially different
directions, name the tradeoff, and recommend one. Preserve the selected direction
in the surface that owns it.

## Pressure-Test Conversationally

Pressure-test the work until the next move is shaped well enough to trust.

Ask one material question when one answer would unblock good work.

Offer two or three materially different options when the choice is not obvious.
Name the tradeoff. Recommend a path.

Good pressure questions sound like:

- What should this become, and what should it explicitly not become?
- What system seam, data model, state relationship, or abstraction should this reinforce?
- What would make the design internally inconsistent?
- What would make this successful?
- What should not change?
- Is this a local fix or a precedent?
- What would make this risky?
- What should a future agent know before touching this?
- What evidence would convince us this worked?
- Is this ready for a ticket, or are we still shaping the intent?

Do not walk the operator through a form unless the operator asks for one.

## Stay Outer While Work Is Fuzzy

Stay in the outer loop when any of these are unclear:

- purpose or success criteria
- user, audience, or operator outcome
- intended behavior
- quality bar or non-examples
- policy, constraint, or precedent
- system shape, data model, state model, or abstraction boundary
- design coherence
- evidence baseline
- sequencing or rollout
- risk or audit need
- ticket-sized boundary
- operator authority for a consequential choice
- what `better`, `done`, `simple`, or similar shorthand excludes

Do not jump from a fuzzy request to implementation before the direction-setting
choices are shaped.

If the work cannot yet be handed to a future agent with clear scope, constraints,
evidence expectations, and stop conditions, it is still outer-loop work.

## Shape Toward The Right Surface

The outer loop should end by routing the durable truth.

If the operator makes a durable decision, preserve it in the surface that can
maintain it. Do not leave the real decision only in chat.

Use the surface that owns the truth:

- constitution for durable project judgment, policy, principle, constraint,
  precedent, ADR shape, or roadmap direction
- research for investigation, comparison, synthesis, rejected paths, or null results
- specs for intended behavior, requirements, scenarios, interfaces, or invariants
- plans for operator-shaped strategy across multiple tickets or execution units
- tickets for bounded executable work
- evidence for durable observations
- audit for Ralph-backed adversarial review
- knowledge for preferences, procedures, reusable accepted understanding, and
  retrieval cues
- packets for delegated worker execution

When no durable truth changed, move forward with the smallest useful next step.

## Ready To Execute

Execution is ready when a future agent could understand the goal, scope,
constraints, expected evidence, and stop conditions without reading the chat that
produced them.

For product or UI work, readiness also means the operator-facing direction is
clear enough that the agent is not silently choosing the audience, quality bar,
visual language, data depth, rollout expectation, or acceptance evidence.

For complex work, readiness means the next execution unit is ticket-ready. If the
work needs several independent closure stories, create or update the plan and
child tickets before implementation.

If that is not true, keep shaping.

When it is true, stop shaping and route the work into the appropriate surface or
skill.
