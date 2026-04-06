---
name: loom-initiatives
description: Maintain Loom initiative records for strategic outcomes spanning multiple specs, plans, and tickets. Use when a cross-cutting goal, strategic objective, success metric, milestone set, or grouped downstream work needs one durable owner. Not for single bounded tasks, implementation details, or live progress tracking.
compatibility: Designed for this Markdown-first Loom repository.
metadata:
  author: agent-loom
  version: "0.1"
  loom-layer: strategic-context
---

# loom-initiatives

Initiatives are the Loom strategic-context layer.

Use this skill to manage strategic outcome containers that group multiple specs, plans, and tickets under one larger objective.

## Use This Skill When

- a cross-cutting outcome needs one durable strategic owner
- multiple specs, plans, or tickets should be grouped under one higher-level objective
- success metrics or milestones need to be visible above the ticket layer

## Do Not Use This Skill When

- the work is only one bounded implementation task
- you need live progress tracking rather than outcome framing
- the real need is a behavior contract, execution strategy, or ticket ledger entry

## What This Skill Governs

- initiative records

## Initiative Posture

Initiatives should stay strategic.

They should tell a future agent:

- what outcome matters
- why it matters now
- how success will be judged
- which downstream artifacts execute the work

Use initiatives to organize outcome-level truth, not to track every small step.

## Before You Write

1. read existing initiatives to avoid creating overlapping strategic umbrellas
2. define the outcome boundary before deciding whether a new initiative is warranted
3. identify the downstream specs, plans, and tickets that will actually execute the work

## Execution Playbook

1. create an initiative only when the outcome genuinely needs its own durable owner
2. if you create one, immediately populate objective, why-now, scope, success metrics, milestones, dependencies, and risks
3. make the outcome concrete enough that later plans and tickets can align without reinterpretation
4. link the downstream work explicitly after the strategic framing is written
5. update the initiative when strategic framing changes materially, not every time a single ticket moves
6. validate the record before using it as guidance for downstream work

## How To Use The Scripts

Read `references/scripts.md` for the bundled CLI surface, including argument meanings and example invocations.

- `scripts/initiatives.py create`: use when a new strategic outcome needs a durable record in `.loom/initiatives/`
- `scripts/initiatives.py create`: after running it, populate the strategy immediately; the command only scaffolds the record
- `scripts/initiatives.py link`: use to add or remove linked research, specs, plans, and tickets once the initiative body is real

## Neighboring Layer Boundaries

- initiatives explain strategic outcomes
- plans explain execution strategy
- tickets explain live execution state
- initiatives should not degrade into milestone-only checklists with no strategic context

## What Good Looks Like

- the objective is clear
- success is measurable enough to judge later
- in-scope and out-of-scope surfaces are visible
- linked downstream work is explicit
- the initiative stays strategic rather than turning into a micro-task list

## Validation Focus

- required sections present
- measurable outcomes or milestones exist
- linked work is explicit
- initiative language stays strategic rather than collapsing into task tracking

## Failure Conditions

- the initiative duplicates another active initiative
- the record claims strategy but only lists tasks
- success metrics are absent or too vague to matter
- downstream work is implied instead of linked explicitly
- a newly created initiative remains a shell

## Done Means

- one initiative clearly owns the strategic outcome
- the outcome, scope, metrics, and milestones are explicit
- downstream links are present where needed
- the scaffold and frontmatter are explicit enough for later workspace validation

## Read In This Order

1. `references/schema-initiatives.md`
2. `references/scripts.md`
3. `references/examples.md`

## References

- `references/schema-initiatives.md`
- `references/scripts.md`
- `references/examples.md`
