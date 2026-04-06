---
name: loom-plans
description: Maintain Loom execution plans and strategy: plan records, sequencing, milestones, dependencies, validation, recovery, rollout, rollback, and linked ticket coverage. Use when execution strategy or milestone sequencing across linked tickets needs a durable plan. Not for live task-by-task progress tracking, ticket journaling, or final behavior contracts.
compatibility: Designed for this Markdown-first Loom repository.
metadata:
  author: agent-loom
  version: "0.1"
  loom-layer: execution-strategy
---

# loom-plans

Plans are the Loom execution-strategy layer.

Use this skill to define execution strategy across a linked ticket set.

## Use This Skill When

- the work needs durable sequencing or milestone planning
- the team needs a strategy for how to realize a spec
- rollback, recovery, or validation approach needs to be made explicit

## Do Not Use This Skill When

- you are writing the intended behavior itself
- you are updating the live execution ledger
- the work only needs one small ticket and no broader sequencing record

## What This Skill Governs

- plan records

## Plan Posture

Plans should answer:

- what the big picture is
- what order of work makes sense
- what milestones matter
- what risks or dependencies shape the sequence
- which tickets execute the strategy

Plans explain how work should unfold. They do not replace the ticket ledger.

## Before You Write

1. read the governing spec, initiative, and active tickets first
2. decide whether the work truly needs a separate durable strategy record
3. identify the tickets that will execute the plan so the strategy stays grounded

## Execution Playbook

1. create a plan only when the work needs its own durable strategy record
2. if you create one, populate purpose, milestones, plan of work, validation, recovery, and risks immediately
3. make the intended order of work legible enough that another agent can resume safely
4. link governing and downstream records after the strategy is written
5. revise the plan when sequencing, dependencies, validation, recovery, or milestone shape changes materially
6. validate the final record before expecting others to follow it

## How To Use The Scripts

Read `references/scripts.md` for the bundled CLI surface, including argument meanings and example invocations.

- `scripts/plans.py create`: use when execution strategy needs a durable home in `.loom/plans/`
- `scripts/plans.py create`: after running it, populate the body immediately; the command only creates the scaffold
- `scripts/plans.py link`: use to add or remove linked constitution, initiative, spec, and ticket refs once the strategy is real

## Neighboring Layer Boundaries

- specs define intended behavior
- plans define execution strategy
- tickets define live execution state
- plans should not become a second ticket ledger full of micro-updates

## What Good Looks Like

- milestones make the path legible
- dependencies and risks are explicit
- validation and recovery thinking are present
- linked tickets show who actually executes the strategy
- the plan can guide work without pretending to be the live ledger

## Validation Focus

- required sections present
- linked tickets explicit
- status and revision notes truthful
- the plan remains strategy-oriented rather than becoming a second execution ledger

## Failure Conditions

- the plan duplicates another active strategy record
- the strategy is so vague that no downstream ticket can act from it
- the plan becomes a progress diary instead of sequencing guidance
- dependencies, rollback, or validation thinking are omitted when they matter
- a newly created plan remains an empty shell

## Done Means

- the strategy is durable, legible, and linked to real ticket execution
- milestones, dependencies, validation, and risks are explicit
- relevant links are present
- the scaffold and frontmatter are explicit enough for later workspace validation

## Read In This Order

1. `references/schema-plans.md`
2. `references/scripts.md`
3. `references/examples.md`

## References

- `references/schema-plans.md`
- `references/scripts.md`
- `references/examples.md`
