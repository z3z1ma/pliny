---
name: loom-accept
description: "Make a fail-closed acceptance decision for a ticket or change target: verify evidence and follow-through, then close honestly or reopen with concrete gaps."
arguments: "<ticket id | change target>"
category: core
suggested_skills:
  - loom-workspace
  - loom-records
  - loom-tickets
  - loom-critique
  - loom-wiki
  - loom-specs
  - loom-research
---

# /loom-accept

You are running **Loom Accept**.

Acceptance target:
`$ARGUMENTS`

This command exists because `closed` is not a vibe.
It is a governed decision.

Hydrate only what you need from:
- `loom-workspace`
- `loom-records`
- `loom-tickets`
- `loom-critique`
- `loom-wiki`
- `loom-specs`
- `loom-research`

## Goals

- compare the claimed outcome against the actual acceptance contract
- verify evidence, critique disposition, and wiki disposition
- close only when the durable story is truthful
- otherwise leave a precise and actionable non-closure state

## Canonical Procedure

Use `skills/loom-tickets/references/acceptance-gate.md` as the procedure.

In short:

1. anchor the ticket
2. read the acceptance dossier
3. test evidence, coverage, claim matrix, critique, and wiki disposition
4. choose the honest ticket state
5. record the decision in the ticket journal

## Native tools to prefer

- `rg -n '^(id|status|depends_on):' .loom/tickets --glob '*.md'`
- `rg -n '<ticket-id>|<target>' .loom/{critique,wiki,evidence,specs,research,plans,packets} --glob '*.md'`
- `git status --short`
- `git diff --stat`

## Guardrails

- Fail closed.
- Do not close a ticket because the coding feels done.
- Do not ignore unresolved critique findings.
- Do not let acceptance live only in chat.

## Required output

- acceptance verdict
- ticket status after the decision
- evidence and critique basis for that decision
- follow-up tickets or gaps if not closed
- recommended next command
