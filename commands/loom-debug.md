---
name: loom-debug
description: "Run a reproduce-first Loom debug workflow that routes reproduction, root cause, fix, proof, critique, and prevention into existing owner layers."
arguments: "<bug report | failing behavior | incident>"
category: support
suggested_skills:
  - loom-workspace
  - loom-records
  - loom-debugging
  - loom-research
  - loom-specs
  - loom-tickets
  - loom-ralph
  - loom-critique
---

# /loom-debug

You are running **Loom Debug**.

Debug target:
`$ARGUMENTS`

Debugging follows:

`reproduce -> localize -> explain -> fix -> prove -> prevent`

Hydrate only what you need from:
- `loom-workspace`
- `loom-records`
- `loom-debugging`
- `loom-research`
- `loom-specs`
- `loom-tickets`
- `loom-ralph`
- `loom-critique`

## Goals

- reproduce or explicitly fail to reproduce the behavior
- preserve root-cause investigation
- clarify intended behavior when needed
- create a bounded fix ticket
- prove the fix with evidence
- route prevention into retrospective when warranted

## Procedure

1. Capture reproduction steps or observed failure as evidence.
2. Localize the likely cause with repository inspection and targeted checks.
3. Create or update research if the cause is uncertain.
4. Update or create a spec if intended behavior is ambiguous.
5. Create or tighten one bounded fix ticket.
6. Compile a Ralph packet, usually `test-first`.
7. Preserve red and green evidence.
8. Route to critique if risk warrants.
9. Recommend retrospective when the bug reveals a repeatable pitfall.

## Guardrails

- Do not skip reproduction unless you explicitly record why it is impossible.
- Do not treat the fix as proven without evidence.
- Do not hide root-cause uncertainty in ticket prose.
- Do not close the ticket from this command.

## Required Output

- reproduction evidence or reproduction blocker
- root-cause status
- records created or updated
- fix ticket and packet, if created
- proof gathered or still missing
- recommended next command
