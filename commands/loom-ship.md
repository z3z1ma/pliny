---
name: loom-ship
description: "Package already-truthful Loom work for PR, release, or handoff without closing tickets."
arguments: "<ticket id | plan | release slice>"
category: core
suggested_skills:
  - loom-workspace
  - loom-records
  - loom-shipping
  - loom-tickets
  - loom-critique
  - loom-wiki
---

# /loom-ship

You are running **Loom Ship**.

Ship target:
`$ARGUMENTS`

This command packages work for an external handoff.
It does not close tickets. `/loom-accept` owns closure.

Hydrate only what you need from:
- `loom-workspace`
- `loom-records`
- `loom-shipping`
- `loom-tickets`
- `loom-critique`
- `loom-wiki`

## Goals

- summarize already-truthful work for PR, release, review, or handoff
- cite tickets, evidence, critique, and wiki disposition
- make risks and follow-ups visible
- keep external summaries subordinate to Loom records

## Procedure

1. Anchor the ticket, plan, or release slice.
2. Read ticket status, acceptance criteria, evidence, critique, and wiki disposition.
3. Stop and route back if evidence or required critique is missing.
4. Draft a PR or handoff summary from Loom records.
5. Draft test/evidence summary.
6. Draft risk summary and follow-up list.
7. Draft release notes when useful.
8. Recommend `/loom-accept` only when closure is the remaining governed step.

## Guardrails

- Do not package transcript memory as truth.
- Do not hide unresolved critique or missing evidence.
- Do not mark tickets closed.
- Do not let PR text or external issue comments become the execution ledger.

## Required Output

- PR or handoff summary
- test/evidence summary
- risk summary
- follow-up list
- release note draft, if useful
- recommended next command
