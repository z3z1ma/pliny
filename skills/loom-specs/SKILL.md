---
name: loom-specs
description: Maintain Loom behavior contracts and specifications: specs, desired behavior, requirements, constraints, scenarios, acceptance criteria, and design notes. Use when intended behavior, acceptance, or requirements need a durable contract before or during implementation. Not for research-only notes, live execution updates, or final accepted documentation.
compatibility: Designed for this Markdown-first Loom repository.
metadata:
  author: agent-loom
  version: "0.1"
  loom-layer: behavior-contract
---

# loom-specs

Specs are the Loom behavior-contract layer.

Use this skill to write behavior contracts that define what the system should do, what constraints matter, and what evidence will count as acceptance.

## Use This Skill When

- intended behavior needs to become durable and testable
- implementation work is starting but expected behavior is still fuzzy
- acceptance criteria need to be made explicit before execution or critique

## Do Not Use This Skill When

- you are recording research evidence without locking intended behavior
- you are tracking progress or blockers
- the work is accepted explanatory documentation rather than a contract

## What This Skill Governs

- specification records

## Spec Posture

Specs should remain behavior-first.

They should tell another agent:

- what problem is being solved
- what desired behavior is expected
- what constraints apply
- what scenarios exercise the behavior
- what acceptance evidence will count

Do not let specs degrade into rollout notes, progress notes, or ledger state.

## Before You Write

1. read existing specs and research so you do not create competing contracts
2. define the actual behavior boundary before deciding whether a new spec is necessary
3. identify the downstream plans, tickets, critique, and docs work this spec will drive

## Execution Playbook

1. create a new spec only when the behavior does not already have a durable owner
2. if you create one, populate the problem framing, desired behavior, constraints, requirements, scenarios, acceptance, and design notes immediately
3. write requirements in language that downstream work can test or verify
4. keep implementation notes subordinate to intended behavior
5. link upstream evidence and downstream work after the contract is clear
6. validate the record before other layers start relying on it

## How To Use The Scripts

Read `references/scripts.md` for the bundled CLI surface, including argument meanings and example invocations.

- `scripts/specs.py create`: use when new behavior needs a durable contract in `.loom/specs/`
- `scripts/specs.py create`: after running it, fill the body immediately; the command only creates the scaffold
- `scripts/specs.py link`: use to add or remove typed upstream and downstream links once the contract shape is real

## Neighboring Layer Boundaries

- research feeds evidence into specs
- plans sequence the strategy that realizes the spec
- tickets carry execution truth while implementing it
- docs explain accepted reality after the work lands
- specs should not become a second plan or a ticket journal

## What Good Looks Like

- the problem framing is legible
- desired behavior is concrete
- constraints and scenarios are explicit
- acceptance is strong enough to guide implementation and critique
- linked evidence and downstream work are visible where needed

## Validation Focus

- required sections present
- acceptance exists
- scenarios and constraints are explicit
- spec language remains behavioral rather than drifting into rollout status or ledger state

## Failure Conditions

- the spec duplicates an existing active contract
- requirements are vague or impossible to verify
- the record mostly describes implementation activity rather than intended behavior
- acceptance is missing or too weak to guide downstream work
- a newly created spec stays mostly blank

## Done Means

- one spec clearly owns the behavior boundary
- behavior, constraints, scenarios, and acceptance are explicit
- relevant links are present
- the scaffold and frontmatter are explicit enough for later workspace validation

## Read In This Order

1. `references/schema-specs.md`
2. `references/scripts.md`
3. `references/examples.md`

## References

- `references/schema-specs.md`
- `references/scripts.md`
- `references/examples.md`
