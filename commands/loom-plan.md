---
name: loom-plan
description: "Turn a raw request into governed Loom work by creating or updating the minimal correct outer-loop chain: initiative, research/spec when needed, plan, and ready tickets."
arguments: "<idea | problem | request | outcome>"
category: core
suggested_skills:
  - loom-workspace
  - loom-records
  - loom-initiatives
  - loom-research
  - loom-specs
  - loom-plans
  - loom-tickets
  - loom-memory
  - loom-wiki
---

# /loom-plan

You are running **Loom Plan**.

Request:
`$ARGUMENTS`

This command is the explicit outer-loop shaping surface.
Read before inventing, create only the layers that actually need to exist, and leave behind a plan and ticket set that a fresh worker could honestly execute.

Hydrate only what you need from:
- `loom-workspace`
- `loom-records`
- `loom-initiatives`
- `loom-research`
- `loom-specs`
- `loom-plans`
- `loom-tickets`
- `loom-memory`
- `loom-wiki`

## Goals

- recover relevant prior knowledge before creating new records
- choose the minimal correct owner chain
- create or update a durable plan
- slice the work into bounded, dependency-aware tickets
- stop before implementation

## Procedure

1. **Orient first.**
   - Confirm the workspace root and `.loom/` structure.
   - Read `constitution:main`.
   - Find the initiatives, plans, tickets, wiki pages, and optional memory already relevant to `$ARGUMENTS`.

2. **Recall before inventing.**
   - Search `.loom/wiki/`, `.loom/research/`, `.loom/specs/`, `.loom/plans/`, `.loom/tickets/`, and optional `.loom/memory/`.
   - Reuse accepted understanding and prior evidence instead of re-deriving basics.
   - If a durable explanation already exists in the wiki, let it reduce planning thrash.

3. **Choose the minimal owner chain.**
   - Create or refine an **initiative** only if the outcome is strategic and spans multiple downstream artifacts.
   - Create **research** only if evidence is missing.
   - Create a **spec** only if intended behavior is unclear.
   - Create or update a **plan** when sequencing or rollout strategy needs a durable owner.
   - Always leave live execution owned by one or more **tickets**.

4. **Write or refine the records.**
   - Use the Loom templates and record grammar.
   - Keep truth in the right layer.
   - Link the chain in frontmatter and in concise prose where helpful.

5. **Slice into tickets.**
   - Favor the next smallest meaningful slice.
   - Each ticket should be independently legible, bounded, and testable or reviewable.
   - Use `depends_on` only for hard prerequisites.
   - Keep status truthful: usually `proposed` or `ready`.

6. **Check ticket readiness.**
   - A fresh worker should not need transcript archaeology.
   - Scope, non-goals, acceptance criteria, and evidence path should be visible.
   - If a ticket is not ready, refine it instead of forcing Ralph.

7. **Decide the next command.**
   - Usually `/loom-work <ticket-id>`.
   - If evidence is still missing, `/loom-research ...`.
   - If the work is a bounded experiment, `/loom-spike ...`.
   - If the work is bug investigation, `/loom-debug ...`.
   - If orientation is the blocker, `/loom-map ...`.
   - If behavior is still missing, `/loom-spec ...`.
   - If the work hinges on a citable architectural or policy choice, `/loom-decide ...` before proceeding.

## Native tools to prefer

- `find .loom -maxdepth 2 -type d | sort`
- `rg -n '<term>' .loom/{initiatives,research,specs,plans,tickets,wiki,memory} --glob '*.md'`
- `rg -n '^(id|status|links):' .loom/{initiatives,research,specs,plans,tickets} --glob '*.md'`
- `date -u +"%Y-%m-%dT%H:%M:%SZ"`
- `git status --short`
- `git diff --stat`

## Guardrails

- Do not implement product code in this command.
- Do not create empty ceremony layers.
- Do not leave live progress in the plan.
- Do not widen scope because a nearby improvement looks tempting.

## Required output

- concise planning summary
- records created or updated, with paths and IDs
- ticket list with status and dependencies
- unresolved questions, risks, or assumptions
- recommended next command
