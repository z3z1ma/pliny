---
name: loom-brainstorm
description: "Divergent shaping surface: ask before proposing, capture ambiguity, check precedent, and exit into /loom-plan, a deferred-questions research record, cited precedent, or /loom-decide."
arguments: "<raw idea | fuzzy problem | half-formed request>"
category: core
suggested_skills:
  - loom-workspace
  - loom-research
  - loom-constitution
  - loom-wiki
  - loom-records
---

# /loom-brainstorm

You are running **Loom Brainstorm**.

Raw idea:
`$ARGUMENTS`

This command is the explicit divergent-shaping surface.
Use it when the request is still fuzzy, when assumptions have not been surfaced, or when the honest next step is questions rather than records.

Hydrate only what you need from:
- `loom-workspace`
- `loom-research`
- `loom-constitution`
- `loom-wiki`
- `loom-records`

## Goals

- make the request legible enough for `/loom-plan` to act on it honestly
- surface assumptions, constraints, and precedent the operator may not have stated
- catch situations where the request conflicts with existing constitution, wiki, or prior research
- ask before proposing and capture ambiguity before drafting
- exit to the correct next owner without creating initiatives, specs, plans, or tickets

## Canonical Procedure

Use `skills/loom-workspace/references/problem-shaping.md` as the procedure.

In short:

1. orient without committing
2. restate the request
3. ask only the sharp clarifying questions needed
4. check precedent and conflict
5. surface assumptions
6. route to the correct owner

## Native tools to prefer

- `rg -n '^id:' .loom/constitution`
- `find .loom/constitution/decisions -name '*.md' | sort`
- `rg -n '<topic>' .loom/{wiki,research,specs,plans,tickets} --glob '*.md'`
- `find .loom/wiki -type f -name '*.md' | sort`

## Guardrails

- Do not draft initiatives, specs, plans, or tickets from this command.
- Do not answer with code; this command shapes the problem, not the execution.
- Do not silently choose among ambiguous readings; surface the ambiguity.
- Do not manufacture clarifying questions when the request is already clear; route directly to the correct next command.
- Do not bypass conflicting constitutional truth; surface the conflict and let the operator amend policy or change the request.

## Required output

- restated request
- clarifying questions
- precedent found and how it constrains the work
- surfaced assumptions, marked accepted / to-be-confirmed / contested
- conflicts, if any
- recommended next command
