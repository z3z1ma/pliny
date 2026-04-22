---
name: loom-tickets
description: "Maintain the sole live execution ledger. Use when new work needs a bounded owner, when execution status changes, when blockers or evidence change, or when Ralph, critique, or wiki passes must reconcile their consequences back into durable execution truth."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  loom_layer: ticket
  protocol_version: "2.0"
---

# loom-tickets

Tickets are the sole live execution ledger.

That sentence is not metaphorical.
If execution truth changed, the ticket should absorb it.

## What This Skill Owns

- ticket creation
- ticket status transitions
- execution notes
- acceptance criteria
- claim coverage
- dependencies
- evidence / critique / wiki disposition
- journal updates

## Use This Skill When

- new bounded work needs an owner
- status changed
- blockers changed
- evidence changed
- critique changed what the ticket should say
- wiki follow-through happened or was deferred
- a Ralph run needs to be reconciled

## Do Not Use This Skill When

- the real work is still strategic framing
- the work is still only a behavior contract
- you are tempted to use a plan or wiki page as the live ledger

## The Ticket Standard

A good ticket should let a fresh agent answer:

- what is this
- why now
- what is in scope
- what is out of scope
- what counts as done
- which acceptance IDs it covers, when a spec names them
- what evidence exists
- what the blockers are
- what the next move is

## Dependency Model

Use `depends_on` for hard upstream ticket prerequisites.

Use `links:` for softer relationships such as critique, wiki, or related work.

## Native Creation Pattern

A common shell flow is:

```bash
token="$(LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c 8)"
stamp="$(date -u +%Y%m%d)"
cp skills/loom-tickets/templates/ticket.md ".loom/tickets/${stamp}-${token}-short-slug.md"
```

Then replace the placeholders in the copied file.

## Done Means

- the ticket tells the truth about live execution
- status matches reality
- the next move is legible
- evidence and follow-through are linked or explicitly absent for a reason

## Read In This Order

1. `references/state-machine.md`
2. `references/dependencies.md`
3. `references/readiness.md`
4. `skills/loom-records/references/claim-coverage.md`
5. `templates/ticket.md`
