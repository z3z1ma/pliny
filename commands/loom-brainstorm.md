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

## Procedure

1. **Orient without committing.**
   - Confirm the workspace root and `.loom/` structure if not already known.
   - Read `constitution:main` and skim decisions and roadmap.
   - Skim the wiki index and any prior research adjacent to `$ARGUMENTS`.
   - Do not create records yet.

2. **Restate the request.**
   - Write back what the operator is asking, in one or two sentences.
   - Name what is not yet clear.

3. **Ask clarifying questions.**
   - What outcome would make this feel clearly solved?
   - Who is this for, and what do they currently do instead?
   - What existing Loom work does this touch?
   - What constraints or principles should bind the answer?
   - What is explicitly out of scope?
   - Prefer a small number of sharp questions over a long list.

4. **Check precedent and conflict.**
   - Does an existing decision record already address this?
   - Does the constitution constrain it?
   - Is there a wiki page that would reduce re-derivation?
   - Is there prior research, including rejected options and null results, that the new work should inherit?
   - Surface conflicts explicitly; do not silently route around them.

5. **Surface assumptions.**
   - List the assumptions the current understanding rests on.
   - Mark each as accepted, to-be-confirmed, or contested.

6. **Exit to the correct next owner.**
   - `/loom-plan` when the problem is legible enough for planning.
   - A deferred-questions research record (`status: deferred_questions`) when the request is still too fuzzy to plan but the questions should be preserved.
   - Cited precedent (constitution, wiki, existing research) when the question is already answered and the right move is to cite it.
   - `/loom-decide` when brainstorming produced a clear citable choice that should be recorded as an architectural decision before planning proceeds.

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
