---
name: loom-plans
description: "Maintain execution strategy, decomposition, sequencing, rollout, and milestone coordination. Use when the work needs more than one ticket, when order matters, or when the project needs an explicit route from strategy to bounded execution."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: owner-layer
  owns_layer: plan
---

# loom-plans

Plans own execution strategy.

They explain how the work should be sequenced without trying to replace ticket truth.

## What This Skill Owns

- rollout strategy
- decomposition
- sequencing
- milestones at the execution-strategy layer
- explicit route from initiative/spec to ticket work

## Milestone Boundary

Plan milestones are execution-sequencing checkpoints.

They are not constitutional roadmap direction, initiative outcome metrics, or
ticket progress state. If a plan starts recording what happened today, move that
truth into the ticket journal or evidence.

## Use This Skill When

- multiple tickets need one sequencing owner
- rollout order matters
- dependencies need to be made visible
- the project needs an execution strategy that should outlive one ticket

## Do Not Use This Skill When

- the work is already one bounded ticket
- the layer should really be initiative or spec
- you are tempted to use the plan as a progress log

## Good Plan Questions

A strong plan answers:

- what the overall route is
- why the sequence is ordered this way
- what milestones exist
- what risks and dependencies shape the sequence
- which tickets should exist beneath it

## Done Means

- a future agent can see the intended route without reading transcript history
- the plan sequences the work without swallowing live execution state

## Read In This Order

Read immediately for normal plan creation or review:

1. `references/plan-shape.md` when creating or reviewing a plan's structure.

Then read conditionally:

2. `references/slicing.md` when decomposing a plan into ticket-sized work.
3. `skills/loom-workspace/references/problem-shaping.md` when the request is
   still too fuzzy to become a plan.
4. `templates/plan.md` only when creating or substantially reshaping a plan
   record.
