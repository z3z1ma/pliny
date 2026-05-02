---
name: loom-tickets
description: "Maintain live execution records and ticket-owned acceptance decisions. Use when new work needs a bounded owner, when execution status, blockers, evidence, critique, wiki, or retrospective disposition changes, or when Ralph and other workflow passes must reconcile their consequences into ticket truth."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: owner-layer
  owns_layer: ticket
---

# loom-tickets

Tickets are where Loom records live execution state.

That sentence is not metaphorical.
If execution truth changed, the ticket should absorb it.

## What This Skill Owns

- ticket creation
- ticket status transitions
- execution notes
- ticket-local acceptance criteria when no separate spec owns the contract
- change class and its evidence / critique implications
- claim coverage
- dependencies
- evidence / critique / retrospective / promotion disposition
- journal updates
- acceptance gate behavior
- acceptance and closure decisions

## Use This Skill When

- new bounded work needs an owner
- status changed
- blockers changed
- evidence changed
- critique changed what the ticket should say
- wiki or broader promotion follow-through happened, was deferred, or was not
  required
- a Ralph run needs to be reconciled
- acceptance or closure needs to be decided through the ticket-owned gate

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
- which ticket-local `ACC-*` IDs it owns, when no spec owns the acceptance
  contract
- what evidence exists
- what the blockers are
- what the next move is
- which acceptance IDs are in scope, without redefining the spec contract

## Dependency Model

Use `depends_on` for hard upstream ticket prerequisites.

Use `links:` for softer relationships such as critique, wiki, or related work.

## Acceptance Boundary

Tickets own the live acceptance dossier: scoped acceptance IDs, evidence
disposition, critique disposition, retrospective / promotion disposition,
route-specific wiki disposition when applicable, accepted risk, blockers, and
closure state.

Specs own reusable acceptance contracts. Tickets may own ticket-local acceptance
criteria only when no separate spec exists and the criteria are scoped to that
ticket. When a ticket owns local acceptance criteria, write stable local IDs such
as `ACC-001` in `# Acceptance Criteria` and cite them from other records as
`ticket:<token>#ACC-001`.

Optional commands, commits, PRs, packets, evidence, critique, and wiki pages may
feed that dossier. They do not close work by themselves.

## Native Creation Pattern

A common shell flow copies the ticket template from the installed Loom skill
package path for the current harness. In a source checkout or repo-root skill
installation, that may look like:

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
- closure, when claimed, is backed by the ticket-owned acceptance gate

## Read In This Order

Read immediately for ticket creation or status updates:

1. `references/state-machine.md` when setting, auditing, or explaining ticket
   status.
2. `references/readiness.md` when deciding whether a ticket can become `ready`.

Then read conditionally:

3. `references/dependencies.md` when modeling hard prerequisites or softer
   links.
4. `skills/loom-evidence/SKILL.md` when evidence artifacts need to be created,
   checked, or linked into the acceptance dossier.
5. `skills/loom-records/references/change-class.md` when selecting evidence,
   critique profiles, or verification posture from the kind of mutation.
6. `skills/loom-records/references/claim-coverage.md` when tying the ticket to
   spec acceptance or critique findings.
7. `references/acceptance-gate.md` when deciding whether closure is honest.
8. `templates/ticket.md` only when creating a ticket.
