# Creating Plans

Plan creation is outer-loop work.

Create a plan when complex codebase work needs more than one bounded ticket, or
when sequencing, dependencies, coordination, validation, or audit posture matter
across multiple execution units.

A plan should make the route executable. It should preserve the decisions,
constraints, decomposition, and child ticket links that shape execution.

The saved plan should already name the child tickets an agent is expected to run.
Execution starts from those tickets, not from an unsliced plan summary.

## Shaping Standard

Before writing the plan, shape the work until these things are true:

- strategic direction: what belongs in the change, what stays out, and why this is
  the right route are clear enough to preserve
- design coherence: system seams, data relationships, state relationships, and
  abstraction choices are resolved or owned by linked records
- decomposition need: the work genuinely exceeds one bounded ticket
- execution route: the route through the work is understandable and justified
- ticket set: the child tickets can be created now
- proof posture: validation, evidence, audit, risk, and loopback expectations are
  clear enough for downstream tickets

Resolve ambiguity before saving the plan. Inspect the codebase, read governing
records, ask the operator, or route unknowns to research, specs, or constitution.

Ask one material question at a time when operator input is needed. Offer a
recommended route when the tradeoff is clear.

Do not copy the whole shaping conversation into the plan. Preserve the route,
decomposition, decisions, constraints, risks, validation posture, and child ticket
links that change execution.

## Create A Plan Only When

Create a plan when all of these are true:

- the overall outcome is clear
- the work genuinely exceeds one bounded ticket
- intended behavior is clear enough or owned by a spec
- major tradeoffs or feasibility questions are resolved or owned by research
- system-shape, data-modeling, state-modeling, and abstraction choices that affect
  decomposition are resolved or owned by linked records
- durable policy, precedent, or architectural judgment is resolved or owned by
  constitution
- the route through the work is understandable
- the work can be sliced into ticket-ready execution units
- each execution unit can become a child ticket with concrete scope and `ACC-*`
  acceptance
- validation, evidence, audit, risk, and loopback expectations are clear enough
  for downstream tickets
- the plan's initial status can honestly be `open`

If the plan cannot yet produce ticket-ready units, keep shaping, inspect the
codebase, ask the operator, or route the unknowns to the owning Loom surface.

## Before Writing

Ground the plan before writing it.

Inspect relevant records and source reality before asking the operator to repeat
facts. Depending on the work, this may include specs, research, constitution
records, prior tickets, evidence, source paths, tests, interfaces, migrations, or
external references.

Then shape the route until these are clear:

- why the work needs a plan instead of one ticket
- what outcome the plan is driving toward
- what is intentionally left out of this plan
- what records constrain the work
- what system-shape, data-model, state, abstraction, or coherence constraints shape
  the route
- what decomposition makes sense
- what order matters and why
- what can run independently
- what must be sequential
- what validation and evidence child tickets should inherit
- what risks should be handled early
- what should trigger replanning

## Slicing Standard

Prefer thin execution units that leave the codebase in a working, testable state.

A strong slice does one meaningful thing completely enough to verify before the
next slice expands the change. It should produce observable progress without
requiring the acting agent to implement the whole feature in one pass.

Prefer slices that:

- follow a narrow path through real behavior
- can be tested or inspected independently
- keep unrelated changes separate
- make risk visible early
- let later tickets build on verified ground
- stop cleanly when behavior, evidence, policy, or sequencing questions appear

Use horizontal slices when the layer itself is valuable or is a bounded
prerequisite, such as migration preparation, a compatibility seam, a validation
harness, an adapter boundary, or a behavior-preserving refactor.

## Useful Slicing Routes

Use these routes when they clarify the plan:

- vertical-first: prove one narrow end-to-end path, then broaden coverage
- contract-first: define or tighten a shared interface before multiple tickets
  depend on it
- risk-first: prove the riskiest assumption or integration early
- evidence-first: create or repair validation before implementation would be hard
  to trust
- migration-first: establish the safe data or compatibility path before dependent
  changes
- cleanup-first: isolate behavior-preserving simplification when it makes later
  work easier to review

Use the route that best explains the sequence.

## Scope Discipline

Each execution unit should change one logical thing.

Keep feature work, bug fixes, refactors, dependency changes, generated-file churn,
and formatting-only cleanup separate unless bundling them is necessary and still
reviewable.

If an adjacent improvement is worth doing, give it its own ticket or leave it out.

## Creation Procedure

Use this sequence as the default path, not as a form:

1. Identify the overall outcome.
2. Inspect governing records and relevant source reality.
3. Shape the work until decomposition need, execution route, ticket set, and proof
   posture are clear.
4. Name scope-selection decisions and system-shape, data-model, state,
   abstraction, or coherence constraints.
5. Decide why this needs a plan rather than one ticket.
6. Write the strategy in prose.
7. Slice the work into ticket-ready execution units.
8. Create the child tickets.
9. Put each child ticket ID under the corresponding execution unit.
10. Add the plan to each child ticket's `## Related Records`.
11. Define milestones that group meaningful execution outcomes.
12. Name validation, evidence, audit, risk, and loopback posture.
13. Save the plan using `templates/plan.md`.

If a child ticket cannot be written yet, the execution unit is not ticket-ready.
Keep shaping or route the missing truth to the appropriate surface.

Before execution, test each proposed unit with the single-closure-claim rule from
`loom-tickets`: one child ticket should produce one bounded result with one
coherent evidence and closure story. If a unit combines independent stack, data,
UI, migration, feature, review, and verification outcomes, split it until each
child ticket can close honestly on its own evidence.

## Creation Questions

Good plan-shaping questions include:

- Why is this more than one ticket?
- What belongs in this plan, and what should be left out?
- What is the smallest useful sequence of child tickets?
- Which system seam, data model, state relationship, or abstraction decision shapes the route?
- What would make the decomposition internally inconsistent?
- Which slice should produce the first observable value?
- Which slice should prove the riskiest assumption?
- Which shared contract or interface must be settled before parallel work begins?
- Which validation should exist before implementation expands?
- Which work must be sequential?
- Which work can run independently later?
- Which files, records, interfaces, or systems create coordination risk?
- What validation should child tickets inherit?
- What evidence would make downstream closure honest?
- What should cause the plan to change?

Preserve the route, decomposition, decisions, constraints, risks, validation
posture, and child ticket links that change execution.
