# Plan Shape

A good plan is prose-rich but not vague.

It tells a future agent what complex work is being decomposed, why the route
exists, which records constrain it, which child tickets carry execution, what
milestones matter, what the current plan-level state is, and what has happened so
far.

A plan is not a scratchpad, research note, spec, progress log, ticket substitute,
or parking lot for unresolved thought.

## Top Labels

Use these labels near the top:

```text
ID: plan:YYYYMMDD-<slug>
Type: Plan
Status: open
Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Risk: low|medium|high - reason
```

Risk must include a reason.

Use:

- `low` when the plan coordinates narrow, reversible, easy-to-verify work
- `medium` when the plan coordinates meaningful behavior, shared records,
  integration points, migration steps, or cross-cutting implementation
- `high` when the plan affects core architecture, safety, data integrity,
  migration behavior, public contracts, or hard-to-reverse decisions

Raise risk when sequencing errors, weak evidence, or expensive failure would make
the plan hard to trust.

## Core Sections

Use the default sections unless a plan has a strong reason to vary:

- `## Summary`
- `## Related Records`
- `## Strategy`
- `## Execution Units`
- `## Milestones`
- `## Current State`
- `## Journal`

`## Journal` stays last so agents and tools can append to the bottom.

## Summary

Summary should answer:

- what complex work is being decomposed
- why it matters
- why it needs more than one ticket
- what outcome should exist when the plan completes

Keep it short, but make the plan understandable without relying on chat history.

## Related Records

List records an acting agent should understand before using the plan.

Each entry should explain why the record matters.

Plans often relate to specs, research, constitution records, tickets, evidence,
audit, knowledge, source paths, or external references.

Add only records that materially constrain or explain the plan.

If the plan depends on context that exists only in chat, move the durable version
into the plan or the appropriate linked record.

## Strategy

Strategy explains the route.

Include:

- what belongs in the plan and what is deliberately left out
- why this decomposition makes sense
- why this order makes sense
- which system-shape, data-modeling, state-modeling, abstraction, or coherence
  choices shape the route
- what risks shape the route
- what can run independently
- what must be sequential
- what validation posture downstream tickets should inherit
- what should trigger replanning

Keep live progress out of Strategy.

## Execution Units

Execution units are prose-first, but each unit should point to a concrete child
ticket ID.

Each unit should make clear:

- the child ticket ID
- the outcome the ticket should produce
- the likely scope boundary
- the design, system-shape, data, or state constraint the ticket must preserve when
  it matters
- the order or dependency reason
- validation, evidence, and audit expectations
- loopback or stop conditions

The ticket owns executable detail and live state.

The plan owns decomposition, strategy, sequencing, milestone shape, and plan-level
coordination.

If an execution unit cannot be made into one bounded child ticket, split it or
keep shaping.

## Milestones

Milestones are meaningful checkpoints across child tickets.

They should say what will be true when the milestone is reached and which child
tickets contribute to it.

Milestones are not progress checklists.

Do not duplicate every child ticket state.

## Current State

Current State is a concise plan-level snapshot.

It can summarize:

- strategy state
- milestone state
- plan-level blockers
- residual risks
- child ticket state when useful
- next plan-level move

Do not duplicate every ticket journal entry.

Update Current State when the plan-level story would otherwise be stale or
misleading.

## Journal

The journal is append-friendly and stays at the bottom.

Append material entries for:

- plan creation
- child ticket creation
- strategy changes
- milestone movement
- blockers
- review
- completion
- cancellation

Do not turn the journal into a transcript.

Do not rewrite history to make the route look cleaner. Correct errors when
needed, but preserve the material path.

## Completion Shape

A completed plan should make the strategy story cheap to trust.

Before completion, the plan should show:

- every execution unit has a concrete child ticket ID
- every child ticket is closed, cancelled, or explicitly out of scope with reason
- milestones are satisfied or revised with authority before completion
- unsatisfied milestones are routed to continued review, cancellation, authorized
  scope change, or follow-up work instead of hidden inside completion
- validation, evidence, and audit expectations were handled at the right level
- plan-level audit or review happened when the strategy story needed independent
  pressure
- Current State summarizes the final plan-level story
- Journal records the material route to completion
- residual risks and follow-up work are named

Set `Status: completed` only when the plan tells one truthful strategy story and
the child tickets carry the live execution truth.
