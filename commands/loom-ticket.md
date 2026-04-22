---
name: loom-ticket
description: "Create, split, tighten, relink, or truthfully update one bounded execution ledger entry without doing the implementation."
arguments: "<ticket id | plan slice | execution request>"
category: support
suggested_skills:
  - loom-workspace
  - loom-records
  - loom-tickets
  - loom-plans
  - loom-specs
  - loom-research
---

# /loom-ticket

You are running **Loom Ticket**.

Ticket target or request:
`$ARGUMENTS`

This command is for direct ticket work.
Use it when the work clearly belongs in the execution ledger and the ticket itself should be created, sharpened, split, relinked, or truthfully updated.

Hydrate only what you need from:
- `loom-workspace`
- `loom-records`
- `loom-tickets`
- `loom-plans`
- `loom-specs`
- `loom-research`

## Goals

- ensure the work has one truthful ticket owner
- keep the ticket bounded and ready for Ralph
- correct links, dependencies, acceptance criteria, and status
- stop before implementation

## Procedure

1. **Locate or decide the ticket.**
   - If `$ARGUMENTS` names an existing ticket, open that ticket first.
   - If `$ARGUMENTS` is prose, find the governing plan or initiative and decide whether a new ticket or sibling ticket is needed.

2. **Read the governing chain.**
   - Read the linked plan, and any relevant spec or research.
   - Pull in only the upstream context that matters for execution readiness.

3. **Tighten or split.**
   - Tighten summary, scope, non-goals, acceptance criteria, evidence expectations, and critique/wiki disposition.
   - If several independent slices are hiding inside one ticket, split them.
   - Use `depends_on` only for hard prerequisites.

4. **Set truthful status.**
   - `proposed` if outer-loop work still remains.
   - `ready` only if a fresh worker could start without transcript archaeology.
   - `active` only if work is genuinely underway.
   - `blocked` only with a named blocker.

5. **Recommend the next step.**
   - `/loom-work <ticket-id>` when ready.
   - `/loom-plan ...` if the ticket revealed missing outer-loop structure.
   - `/loom-spec ...` or `/loom-research ...` if the ticket exposed missing contract or evidence.

## Native tools to prefer

- `rg -n 'ticket:[a-z0-9]+' .loom --glob '*.md'`
- `rg -n '^(id|status|depends_on):' .loom/tickets --glob '*.md'`
- `rg -n '<term>' .loom/{plans,specs,research,tickets} --glob '*.md'`
- `date -u +"%Y-%m-%dT%H:%M:%SZ"`

## Guardrails

- Do not start implementation from this command.
- Do not let the ticket redefine plan strategy or spec behavior. If the owner chain is wrong, fix the owner record.
- Do not call a ticket `ready` on faith.

## Required output

- ticket(s) created or updated, with paths and IDs
- readiness assessment
- dependencies and links added or changed
- recommended next command
