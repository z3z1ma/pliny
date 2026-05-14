---
name: loom-plans
description: "Manages Loom plans: creates, shapes, updates, reviews, completes, blocks, and cancels operator-shaped strategy for complex work spanning multiple ticket-ready execution units. Use when high-level work must be decomposed into multiple ticket-ready execution units, or when sequencing, dependencies, rollout, milestones, or recovery strategy matter."
---

# loom-plans

Plans are Loom's strategy and decomposition surface for complex codebase work.

A plan turns a larger change into ticket-ready execution units with a clear route,
sequence, dependency shape, shared constraints, validation posture, and evidence
expectations.

A plan is not a progress log, ticket substitute, research note, spec, or parking
lot for unresolved thought.

A plan does not authorize execution from an unshaped idea. It preserves the
strategy after the direction-setting choices are clear enough: what belongs in the
change, what is left out, how system-shape, data-model, or state-modeling
decisions affect the route, and how the design stays coherent across child
tickets.

## Use This Skill When

Use this skill when:

- work exceeds one bounded ticket
- the operator is shaping a complex change across multiple units of work
- sequencing, dependencies, or coordination matter
- child tickets need one shared implementation strategy they can point back to
- a spec, research conclusion, migration, refactor, or architecture change needs
  ticket-ready execution units
- an existing plan needs to be updated, reviewed, completed, blocked, or cancelled

Use one ticket when one bounded ticket is enough.

When intended behavior, tradeoffs, feasibility, data-model or state-modeling shape,
design coherence, or durable policy are still too unclear, route those questions to
specs, research, or constitution first.

## Dispatch

If creating or reshaping a plan:

- read `references/creating-plans.md`
- read `references/slicing-work.md`
- read `references/plan-shape.md`
- inspect relevant records and source before asking the operator to repeat facts
- create the child tickets once execution units are ticket-ready
- ensure each child ticket links back to the plan in `## Related Records`
- keep execution in the outer loop until the saved plan names child tickets for
  the execution units it expects agents to run

If updating, reviewing, completing, blocking, or cancelling a plan:

- read the whole plan
- inspect the child tickets named in `## Execution Units`
- update Current State and Journal when the plan-level story would otherwise be stale
- keep live execution truth in tickets, not in the plan

If only finding or summarizing plans:

- inspect `.loom/plans/`
- report state without mutating records unless the operator asked for a change

## Finding Plans

Plans live under `.loom/plans/`.

Useful starting points:

```bash
find .loom/plans -name '*.md' -print 2>/dev/null | sort
grep -R '^ID: plan:' .loom/plans 2>/dev/null || true
grep -R '^Status:' .loom/plans 2>/dev/null || true
grep -R '^Risk:' .loom/plans 2>/dev/null || true
```

When looking for a specific plan, prefer ID and filename matches before fuzzy
search.

## Plan IDs And Filenames

Use `plan:YYYYMMDD-<slug>` IDs.

Use matching filenames without the `plan:` prefix:

```text
.loom/plans/YYYYMMDD-<slug>.md
```

Use the actual current date. Do not copy example dates.

If the slug would collide, choose a clearer slug or add a numeric suffix.

## Required Top Labels

Plans use plain body labels near the top:

```text
ID: plan:YYYYMMDD-<slug>
Type: Plan
Status: open
Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Risk: low|medium|high - reason
```

## Status Lifecycle

Use this lifecycle:

- `open`: strategy is accepted, execution units are ticket-ready, and child ticket
  work has not materially started
- `active`: at least one child ticket has started execution
- `blocked`: a concrete plan-level blocker prevents safe progress across the plan
- `review`: child tickets are resolved and final plan-level audit or review is next
- `completed`: child tickets are resolved and the plan-level outcome is accepted
- `cancelled`: the plan should not proceed, with the reason recorded

Plans are not created as drafts.

If material decomposition questions remain, keep shaping outside the plan or route
to the owning Loom surface.

## Plan Discipline

Creating a plan is outer-loop work.

Before saving a plan, shape the work until the route, slices, ticket set,
milestones, validation posture, evidence expectations, audit expectations, and
loopback conditions are clear enough to drive execution.

The plan should also state scope-selection decisions, system-shape, data-model or
state constraints, and coherence risks that make the decomposition make sense.

A saved plan should be usable from the plan and its linked records without relying
on chat history.

The plan owns decomposition, sequencing, strategy, milestones, and plan-level
coordination.

Child tickets own executable detail, live state, evidence, and closure.

## Template

Use `templates/plan.md` as the default starting point. Preserve useful structure
and remove empty sections.

## Review And Completion

Use `Status: review` when all child tickets are closed, cancelled, or otherwise
resolved but plan-level audit or review is not yet complete.

Complete a plan only when:

- every execution unit has a concrete child ticket ID
- every child ticket is closed, cancelled, or explicitly out of scope with reason
- milestones are satisfied or revised with authority before completion
- unsatisfied milestones are routed to continued review, cancellation, authorized
  scope change, or follow-up work instead of hidden inside completion
- plan-level audit or review has happened when the strategy story needs it
- Current State summarizes the final plan-level story
- Journal records the material route to completion
- residual risks and follow-up work are named

Set `Status: completed` only when the plan tells one truthful strategy story and
the child tickets carry the live execution truth.

## Done Means

Plan work is done when:

- the plan decomposes complex work into concrete child tickets
- the ticket set is created and linked back to the plan
- the strategy explains why this route and order make sense
- milestones describe meaningful checkpoints without becoming progress state
- validation, evidence, risk, audit, and loopback expectations are visible
- plan-level audit expectations are handled without duplicating child ticket truth
- Current State and Journal make plan-level continuation possible without chat history
