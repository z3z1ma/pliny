---
name: loom-tickets
description: Maintain Loom ticket records as the live execution ledger: ticket status, scope, acceptance, implementation plan, verification, blockers, handoff notes, journal updates, and documentation disposition. Use when work needs a live execution owner or when execution truth, blockers, verification, review state, or docs disposition changed. Not for strategy, behavior design, or final explanatory docs.
compatibility: Designed for this Markdown-first Loom repository.
metadata:
  author: agent-loom
  version: "0.1"
  loom-layer: execution-ledger
---

# loom-tickets

Tickets are the canonical Loom execution ledger.

Use this skill to create, maintain, and close the durable record of live execution state.

## Use This Skill When

- new work needs a live execution owner
- implementation truth changed and the ticket ledger must absorb it
- verification, blockers, next steps, or docs disposition changed
- another layer produced durable execution consequences that must reconcile back into the ticket

## Do Not Use This Skill When

- the work is still only strategic framing, behavioral design, or research without active execution ownership
- you are trying to preserve packet output as if it were the primary ledger
- you want to explain accepted reality rather than track current execution truth

## What This Skill Governs

- ticket records
- ticket status transitions
- the durable ledger view of execution work

## Ticket Posture

Tickets should answer, at any moment:

- what the work is
- why it matters now
- what is in scope
- what counts as done
- what evidence exists
- what blocked or changed
- what should happen next

If another layer changes execution reality, the ticket should absorb that truth so a future agent can resume from the ticket instead of reconstructing state from scattered artifacts.

## Before You Write

1. read related tickets first so you do not split one work item across multiple ledger entries
2. decide whether the work is genuinely new or is already owned by an existing ticket
3. resolve repository ownership before broadening the ticket scope
4. decide whether you are creating a new ticket or reconciling truth into an existing one

## Execution Playbook

1. create a new ticket only when the work is genuinely new or when you intentionally need a separate ledger entry
2. if you create one, populate it immediately; a ticket shell is not a usable ledger record
3. write the body so `Summary`, `Context`, `Scope`, `Acceptance Criteria`, `Implementation Plan`, `Verification`, `Documentation Disposition`, and `Journal` teach the next actor what to do
4. add dependencies and related refs after the body is clear
5. create verification records as soon as execution produces durable evidence
6. validate structure and link integrity before changing status or handing the ticket off
7. after Ralph, critique, docs, or local execution changes reality, update the ticket immediately so it remains the single live ledger
8. close the ticket only when acceptance, verification, journal truthfulness, and docs disposition all support closure

## Status Playbook

- use `proposed` when the work exists conceptually but is not yet execution-ready
- use `ready` when the ticket is strong enough that another agent can begin without guessing
- use `active` when execution is underway now
- use `blocked` when progress depends on an unresolved external or upstream condition
- use `review_required` when execution landed far enough that critique or acceptance review is now next
- use `complete_pending_acceptance` when implementation and validation are substantially done but final acceptance or reconciliation remains
- use `closed` only when the durable state really supports completion
- use `cancelled` when the work is intentionally no longer being pursued

## How To Use The Scripts

Read `references/scripts.md` for the bundled CLI surface, including argument meanings and example invocations.

- `scripts/tickets.py create`: use when a new ticket record needs to be created in `.loom/tickets/`
- `scripts/tickets.py create`: after running it, fill the body immediately; the command only scaffolds the record
- `scripts/tickets.py create`: prefer shorthand links like `--link ticket:0004` when you already know the related refs
- `scripts/tickets.py link`: use to add or remove typed refs such as dependencies, verification, critique, and docs links after the body is in place
- `scripts/tickets.py verify`: use as soon as the ticket gains real execution evidence that should participate in the durable graph

## Neighboring Layer Boundaries

- plans explain execution strategy
- tickets explain current execution truth
- critique evaluates that work
- docs explain accepted reality after the work lands
- packets and runs support execution but do not replace the ticket ledger

## What Good Looks Like

- another agent can resume from the ticket alone plus its explicit links
- the next action is clear
- acceptance and verification are concrete enough to judge later
- blockers and changes are recorded explicitly
- the journal captures meaningful execution change rather than empty progress language

## Failure Conditions

- a significant execution event happened but the ticket was not updated
- the ticket claims completion without linked evidence
- the docs disposition is stale after a meaningful accepted change
- the ticket body no longer matches the actual execution state of the work
- a newly created ticket remains a shell but still gets treated as ready

## Done Means

- one ticket clearly owns the live execution truth
- status matches reality
- verification and docs disposition are explicit
- link integrity is explicit in frontmatter and can be validated later by workspace tooling

## Read In This Order

1. `references/schema-tickets.md`
2. `references/scripts.md`
3. `references/examples.md`

## References

- `references/schema-tickets.md`
- `references/scripts.md`
- `references/examples.md`
