---
name: loom-constitution
description: Maintain Loom constitutional memory: constitution, policy, doctrine, principles, constraints, strategic direction, roadmap records, and decision records. Use when project identity, architecture principles, policy, doctrine, roadmap direction, or durable strategic decisions change. Not for ticket progress, implementation journaling, or operator-facing documentation.
compatibility: Designed for this Markdown-first Loom repository.
metadata:
  author: agent-loom
  version: "0.1"
  loom-layer: constitutional-memory
---

# loom-constitution

Constitution is the durable Loom policy and identity layer above execution-facing records and below the already-active Loom doctrine carried by the session.

Use this skill when the work changes what the project is, what it values, what constraints it accepts, or what strategic direction should remain durable over time.

## Use This Skill When

- the project identity or core mission needs to change
- a principle or hard constraint should become durable policy
- a major decision needs to stay visible to future agents
- strategic direction needs roadmap-level framing

## Do Not Use This Skill When

- you are updating day-to-day execution state
- you are tracking progress, blockers, or implementation notes
- the work belongs to tickets, plans, critique, or docs instead of policy

## What This Skill Governs

- constitution records
- decision records
- roadmap records

## Constitutional Posture

Constitutional work should be durable, explicit, and relatively stable.

Use this layer to explain:

- what Loom is in this repository
- what principles constrain future design choices
- what strategic direction is active now
- which major decisions should remain visible later

Treat every constitutional edit as something a future agent may rely on without seeing this transcript.

## Before You Write

1. read the existing constitution, related decisions, and active roadmap entries first
2. decide whether the change is identity-level, one bounded decision, or roadmap-level direction
3. read the downstream initiative, spec, or plan records that this change will constrain
4. decide whether you are updating an existing canonical record or creating a new one

## Record Selection Playbook

1. update the main constitution when the durable project identity, principles, constraints, or strategic direction itself is changing
2. create a decision record when one bounded architectural or policy choice needs its own durable history
3. create a roadmap record when the work is about strategic direction, sequencing, milestones, or focus areas rather than one decision

If more than one of those sounds plausible, prefer the narrowest record that still preserves the durable truth.

## Execution Playbook

1. identify the exact constitutional change being made
2. choose the owning record family deliberately
3. create the record only if no existing record already owns that truth
4. if you create a record, immediately populate it; creation alone is not completion
5. write the strategic meaning of the change, not a recap of the chat that led to it
6. state downstream implications clearly enough that initiatives, specs, plans, and tickets can align without guessing
7. keep downstream implications explicit in prose; use typed links for decision and roadmap records, but not for `constitution:main`
8. validate the final record before treating it as durable policy

## How To Use The Scripts

Read `references/scripts.md` for the bundled CLI surface, including argument meanings and example invocations.

- `scripts/constitution.py create constitution`: use when the main constitution record itself must be seeded or intentionally replaced
- `scripts/constitution.py create constitution`: after running it, fill in the actual constitutional content immediately; the command only scaffolds the record and does not accept outbound links for `constitution:main`
- `scripts/constitution.py create decision`: use when one bounded decision needs its own durable record under `.loom/constitution/decisions/`
- `scripts/constitution.py create decision`: after running it, explain the decision, why it matters, and what it changes downstream
- `scripts/constitution.py create roadmap`: use when strategic direction needs roadmap framing rather than identity or one decision
- `scripts/constitution.py create roadmap`: after running it, populate milestones, scope, and strategic intent so the roadmap is operationally useful
- `scripts/constitution.py link`: use after the prose is in place to add or remove typed downstream links on decision and roadmap records; `constitution:main` is implicitly linked to everything and should stay link-free
- `scripts/constitution.py diagnose`: use before leaving the constitutional layer so structure, status, and required sections are trustworthy

## Neighboring Layer Boundaries

- constitution records explain durable project identity and strategic framing
- initiatives, specs, plans, tickets, critique, and docs should align with constitutional direction rather than redefine it silently
- constitutional records should not become a shadow ticket ledger or a vague philosophy note with no operational meaning

## What Good Looks Like

- a future agent can read the record and understand the durable policy change without transcript archaeology
- the record makes downstream implications visible
- decision and roadmap links are explicit where they materially help
- the record reads as policy or strategy, not as execution churn

## Validation Focus

- required sections exist
- decisions declare supersession where relevant
- roadmap items link downstream work explicitly
- constitutional records describe strategic meaning rather than live execution state

## Failure Conditions

- the record claims durable policy but only describes a local implementation detail
- a decision is made durable without stating why it matters or what it constrains
- downstream consequences are left implicit
- a newly created record remains a mostly empty scaffold

## Done Means

- the right constitutional record owns the change
- the prose preserves durable strategic meaning
- `constitution:main` stays link-free while decision and roadmap links remain explicit where needed
- `scripts/constitution.py diagnose` passes

## Read In This Order

1. `references/schema-constitution.md`
2. `references/scripts.md`
3. `references/examples.md`

## References

- `references/schema-constitution.md`
- `references/scripts.md`
- `references/examples.md`
