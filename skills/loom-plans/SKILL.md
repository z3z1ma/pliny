---
name: loom-plans
description: "Decompose high-level work into ticket-ready execution units and maintain execution strategy. Use when a feature, refactor, migration, architecture change, or multi-step objective needs detailed slices, ordered tickets, dependencies, tranches, or parallel execution waves."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: owner-layer
  owns_layer: plan
---

# loom-plans

Plans own work decomposition and execution strategy.

They tease high-level work into detailed units of execution that can become
tickets. Sequencing, rollout, milestones, and waves organize those units; they do
not replace ticket truth.

Loom plans inherit the useful parts of self-orienting execution strategy: a fresh
agent should understand the purpose, context, route, proof strategy, dependencies,
and recovery posture. Loom does not turn plans into all-in-one execution ledgers:
tickets own live progress, evidence owns observations, research owns discoveries,
and retrospective/wiki/spec/constitution own promoted lessons.

## Planning Procedure

Before a plan drives tickets, grill the work until the decomposition is obvious
enough for a fresh agent to act without transcript context.

Use the grilling loop when the work still contains vague phases, overloaded terms,
hidden dependencies, unclear ticket boundaries, or uncertain verification:

- interview the operator relentlessly about every material branch of the plan until
  the execution strategy is shared and precise
- ask one material question at a time, waiting for the answer before moving to the
  next dependent branch
- when a question can be answered by inspecting existing records, source paths,
  tests, architecture notes, or prior decisions, inspect first instead of asking
  the operator to restate available facts
- provide a recommended answer for each question, including the evidence or owner
  record that makes the recommendation plausible
- challenge terminology conflicts and fuzzy labels immediately; a phase name is not
  a ticket slice until it has a concrete outcome, boundary, and verification target
- invent concrete execution scenarios that probe the first valuable path, riskiest
  path, failure path, migration path, rollback path, and review path when relevant
- walk dependent decisions one by one until each branch is resolved, routed to the
  right owner layer, or marked as a blocker
- preserve only the resulting execution units, assumptions, dependencies, rejected
  routes, and loopbacks in the plan; do not copy the interview transcript into the
  plan record

## What This Skill Owns

- decomposition
- detailed ticket-ready execution units
- explicit route from initiative/spec/research into ticket work
- sequencing
- rollout strategy
- milestones at the execution-strategy layer

## Naming

Create new plan records as `.loom/plans/<YYYYMMDD>-<slug>.md`.
The canonical ID remains `plan:<slug>` without the date prefix. Use the record
creation date for the filename prefix so plans support temporal discovery and
future retention or cleanup decisions.

## Milestone Boundary

Plan milestones are execution-sequencing checkpoints.

They are not constitutional roadmap direction, initiative outcome metrics, or
ticket progress state. If a plan starts recording what happened today, move that
truth into the ticket journal or evidence.

## Use This Skill When

- high-level work is too large or vague for one ticket and needs decomposition
- a spec, initiative, research conclusion, migration, or refactor needs detailed
  ticket-ready units before execution
- multiple tickets need one decomposition and sequencing owner
- rollout order matters
- dependencies need to be made visible
- the project needs an execution strategy that should outlive one ticket

## Do Not Use This Skill When

- the work is already one bounded ticket
- the layer should really be initiative or spec
- intended behavior is still unclear enough that a spec grilling pass must happen
  before decomposition
- you are tempted to use the plan as a progress log

## Good Plan Questions

A strong plan answers:

- what the overall route is
- what user-visible, operator-visible, or system-visible result the plan exists to
  make possible
- what context and orientation a fresh agent needs before creating tickets
- what high-level work is being decomposed and what owner records constrain it
- which execution units should become tickets beneath it
- what each unit is expected to change, observe, prove, and avoid
- which interfaces, dependencies, data, flags, migrations, records, or environment
  assumptions shape execution
- how the work should be validated and what evidence/critique tickets should expect
- how a future agent can retry, resume, or recover safely
- which execution-strategy decisions were made and why
- why the sequence is ordered this way
- what milestones exist
- what risks and dependencies shape the sequence
- which tickets should exist beneath it
- which slices are vertical enough to produce working, verifiable progress
- which sections are thin on confidence, such as weak rationale, vague file or
  record scope, missing test/evidence targets, or unresolved owner-layer gaps
- where checkpoints or loopbacks should happen before continuing

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "I'll figure out the order while implementing." | Hidden sequencing becomes rework. Plans exist when order, dependency, or parallelism matters. |
| "The plan is mostly a list of phases." | A useful plan decomposes work into ticket-ready execution units with outcomes, scope, evidence, and loopbacks. |
| "Progress belongs in the plan because another planning style tracks it there." | In Loom, tickets own live progress. Plans own route and decomposition; they point to tickets for current state. |
| "A complete plan should decompose everything." | Decompose enough to make the next safe tranche clear; do not manufacture roadmap theater. |
| "Parallel work is faster." | Parallel tickets are safe only when dependencies and write scopes do not conflict. |
| "The plan checklist can be the execution contract." | Ticket acceptance and packet task text own executable detail; plans name proof targets for tickets and packets to validate. |

## Red Flags

- tasks are horizontal layers that cannot be verified independently
- the plan names themes, phases, or waves but not ticket-ready units of execution
- context is so thin that a fresh agent must reconstruct the route from transcript
  history
- validation, acceptance, interfaces, dependencies, or recovery are left implicit
- ticket slices do not say what should change, where, how it will be verified, or
  when to loop back
- ticket slices are too large for one focused execution/review loop
- execution waves lack write-scope or dependency checks
- the plan is being used as a progress log
- evidence or critique expectations are absent for risky tranches

## Verification

- [ ] Claim/acceptance coverage maps to downstream tickets or explains why none applies.
- [ ] Purpose, context, interfaces, validation, and recovery are explicit enough for
      a fresh agent to orient.
- [ ] High-level work has been decomposed into ticket-ready execution units, not
      only phases or waves.
- [ ] Ticket slices are small, ordered by dependency where order matters, and leave
      reviewable checkpoints.
- [ ] Plan confidence gaps have been fixed, routed outward, or recorded as explicit assumptions.
- [ ] Parallel waves, if any, include non-overlap and parent reconciliation checks.
- [ ] Risks name owner-layer loopbacks when execution discovers missing truth.

## Done Means

- a future agent can see the intended route without reading transcript history
- a future agent can create or refine the next tickets from the execution units
  without guessing from transcript history
- the plan decomposes and sequences the work without swallowing live execution state

## Read In This Order

Read immediately for normal plan creation or review:

1. `references/plan-shape.md` when creating or reviewing a plan's structure.

Then read conditionally:

2. `references/slicing.md` when decomposing a plan into ticket-sized work.
3. `skills/loom-workspace/references/problem-shaping.md` when the request is
   still too fuzzy to become a plan.
4. `templates/plan.md` only when creating or substantially reshaping a plan
   record.
