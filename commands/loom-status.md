---
name: loom-status
description: "Produce a current-state Loom snapshot: active queues, blockers, review backlog, acceptance backlog, and the most sensible next move."
arguments: "<topic | path | initiative | ticket | blank for broad status>"
category: core
suggested_skills:
  - loom-workspace
  - loom-records
  - loom-tickets
  - loom-critique
  - loom-wiki
---

# /loom-status

You are running **Loom Status**.

Focus:
`$ARGUMENTS`

This command is the explicit state-synthesis surface.
It should tell the operator what is live, what is stuck, what is waiting for review or acceptance, and what Loom believes the next bounded move should be.

Hydrate only what you need from:
- `loom-workspace`
- `loom-records`
- `loom-tickets`
- `loom-critique`
- `loom-wiki`

## Goals

- summarize the current execution graph truthfully
- surface the ready queue and the blocked queue
- notice review and wiki follow-through debt
- identify contradictions or suspicious state drift
- recommend the next explicit command

## Procedure

1. **Orient quickly.**
   - Confirm the workspace root and `.loom/` structure.
   - Read `constitution:main` only as much as needed for context.

2. **Collect the execution ledger.**
   - List tickets grouped by status:
     `ready`, `active`, `blocked`, `review_required`, `complete_pending_acceptance`.
   - If `$ARGUMENTS` is specific, narrow to the relevant slice and its linked artifacts.

3. **Collect nearby owners.**
   - For the relevant slice, note linked initiatives, plans, research, specs, critiques, wiki pages, and evidence.

4. **Check for state drift.**
   - A ticket says `review_required` but has no critique path.
   - A ticket says `complete_pending_acceptance` but evidence is weak or dispositions are unresolved.
   - A plan is driving live execution instead of the ticket.
   - A wiki page or memory note is carrying owner truth it should not own.

5. **Summarize the queues.**
   - What's most ready to execute next?
   - What is blocked and on what?
   - What is waiting for critique?
   - What is waiting for wiki or acceptance?
   - What looks stale or suspicious?

6. **Recommend the next move.**
   - Usually one of `/loom-plan`, `/loom-work`, `/loom-review`, `/loom-retrospective`, `/loom-accept`, or `/loom-repair` when graph drift is the blocker.

## Native tools to prefer

- `rg -n '^status:' .loom/tickets --glob '*.md'`
- `rg -n '^(id|status|review_target):' .loom/{plans,tickets,critique,wiki} --glob '*.md'`
- `find .loom/{tickets,critique,wiki,evidence} -type f -name '*.md' | sort`
- `git status --short`
- `git diff --stat -- .loom`

## Guardrails

- Do not mutate records by default.
- Report contradictions explicitly instead of smoothing them over.
- Do not treat recency alone as truth; respect owner layers.
- Keep the summary compact but concrete.

## Required output

- status snapshot
- active, blocked, review, and acceptance queues
- contradictions or stale state worth fixing
- best next command and why
