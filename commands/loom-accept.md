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

## Procedure

1. **Anchor the ticket.**
   - Prefer a ticket ID.
   - If `$ARGUMENTS` is broader prose, find the owning ticket or change target first.

2. **Read the acceptance chain.**
   - Ticket
   - linked spec, if any
   - linked research or evidence, if any
   - linked critique records
   - linked wiki pages or wiki disposition
   - any recent Ralph packet outcomes that matter

3. **Test the closure claim.**
   - Are the acceptance criteria actually met?
   - Is the evidence real and sufficient?
   - Were required critique steps completed or truthfully deferred?
   - Were required wiki or knowledge-promotion steps completed or truthfully deferred?
   - Are there unresolved medium or high-severity critique findings?

4. **Choose the honest outcome.**
   - `closed` only when the durable story is complete and coherent.
   - `complete_pending_acceptance` if the work is substantively done but the remaining acceptance step is real.
   - `review_required` if critique is still the next governed move.
   - `active` or `blocked` if the work is not actually done.
   - Create follow-up tickets when residual work is substantial.
   - If graph drift (broken references, owner-layer conflicts, dangling follow-up) is blocking an honest closure, route to `/loom-repair` before deciding.

5. **Update the record.**
   - Record the decision in the ticket journal.
   - Update status and links truthfully.
   - If closure changes a plan or wiki page materially, note the needed reconciliation.

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
