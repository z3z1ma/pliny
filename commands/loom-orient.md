---
name: loom-orient
description: "Enter a Loom workspace safely: establish structural trust, read constitution first, recover the governing artifact chain, and route to the correct next command."
arguments: "<path | record id | task | blank for broad orientation>"
category: core
suggested_skills:
  - loom-workspace
  - loom-records
---

# /loom-orient

You are running **Loom Orient**.

Target or request:
`$ARGUMENTS`

This command is the explicit cold-start and rerouting surface.
Use it when you are entering a repository, the owning layer is unclear, or the operator wants to know what Loom thinks should happen next.

Hydrate only what you need from:
- `loom-workspace`
- `loom-records`

## Goals

- confirm the workspace root
- establish structural trust in `.loom/`
- read `constitution:main` before downstream interpretation
- recover the most relevant owner chain for `$ARGUMENTS`
- decide whether the next move is outer-loop work, Ralph execution, critique, wiki work, or acceptance

## Procedure

1. **Confirm the root.**
   - Use the repository root if one exists.
   - If `$ARGUMENTS` points at a path, resolve which repository owns that path.
   - If ownership is ambiguous, stop and surface the ambiguity.

2. **Inspect Loom structure.**
   - Check for `.loom/` and the canonical directories:
     `constitution`, `initiatives`, `research`, `specs`, `plans`, `tickets`, `critique`, `wiki`, `packets`, `evidence`.
   - If Loom is clearly absent, say so.
   - If the operator's intent is to bootstrap Loom, propose or create the minimal tree and `constitution:main`.
   - Otherwise do not invent a parallel workflow.

3. **Read the constitutional frame.**
   - Read `constitution:main` first if it exists.
   - Capture the project's durable identity, constraints, and any principles that affect the target.

4. **Find the relevant chain.**
   - Search filenames and record IDs related to `$ARGUMENTS`.
   - Prefer the governing chain in this order:
     `constitution -> initiative -> research/spec -> plan -> ticket -> critique/wiki`
   - Read only as deep as needed to route correctly.

5. **Assess current execution state.**
   - Look for relevant tickets in `ready`, `active`, `blocked`, `review_required`, or `complete_pending_acceptance`.
   - Notice if a critique, wiki page, or evidence record already exists for the target.

6. **Route explicitly.**
   - If the request is still exploratory, route to `/loom-brainstorm`.
   - If scope is still fuzzy, route to `/loom-plan`.
   - If evidence is missing, route to `/loom-research`.
   - If behavior is missing, route to `/loom-spec`.
   - If a citable choice should be recorded, route to `/loom-decide`.
   - If a ready or active ticket already owns the work, route to `/loom-work`.
   - If implementation needs adversarial review, route to `/loom-review`.
   - If the main need is accepted explanation, route to `/loom-wiki`.
   - If graph drift is blocking honest work, route to `/loom-repair`.
   - If closure is the question, route to `/loom-accept`.
   - If recent work should be assimilated into owner layers, route to `/loom-retrospective`.

## Native tools to prefer

- `git rev-parse --show-toplevel`
- `find .loom -maxdepth 2 -type d | sort`
- `rg -n '^(id|status):|review_target:|page_type:' .loom --glob '*.md'`
- `rg -n '<term>' .loom --glob '*.md'`
- `git status --short`
- `git diff --stat`

## Guardrails

- Do not start implementation from this command.
- Do not trust downstream records before checking Loom structure.
- Do not guess the owner layer when the graph can tell you.
- By default this command is read-mostly; only bootstrap or repair structure when that is clearly the operator's intent.

## Required output

- workspace root and structural-trust assessment
- most relevant records found
- current owner layer and execution state
- the recommended next command, with reasoning
- any blockers or missing Loom structure
