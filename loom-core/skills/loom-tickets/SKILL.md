---
name: loom-tickets
description: "Maintain bounded execution and acceptance. Use when adding or changing code, tests, docs, config, refactors, migrations, cleanup, blockers, evidence/review disposition, or any done/close/acceptance claim."
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
- wiki or broader retrospective / promotion follow-through happened, was
  deferred, or was not required
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
- what assumptions or decision triggers could change scope or acceptance
- what evidence exists
- what the blockers are
- what remains open, blocked, under review, or ready for acceptance
- which acceptance IDs are in scope, without redefining the spec contract
- whether a claim matrix is actually needed, or whether inline coverage is enough

## Dependency Model

Use `depends_on` for hard upstream ticket prerequisites.

Use `links:` for softer relationships such as critique, wiki, or related work.

## Acceptance Boundary

Tickets own the live acceptance dossier: scoped acceptance IDs, evidence
disposition, critique disposition, retrospective / promotion disposition, wiki
disposition when applicable, accepted risk, blockers, and closure state.

Specs own reusable acceptance contracts. Tickets may own ticket-local acceptance
criteria only when no separate spec exists and the criteria are scoped to that
ticket. When a ticket owns local acceptance criteria, write stable local IDs such
as `ACC-001` in `# Acceptance` and cite them from other records as
`ticket:<token>#ACC-001`.

Optional commands, commits, PRs, packets, evidence, critique, and wiki pages may
feed that dossier. They do not close work by themselves.

## Native Creation Pattern

A common shell flow copies a ticket template from the installed Loom skill package
path for the current harness. In this split source checkout, use the core package
root; in a package-root install, the path may begin with `skills/`.

Use `templates/ticket-lite.md` for a small local ticket when the lightweight
ledger is enough. Use `templates/ticket.md` as the full copy target when the work
needs the complete acceptance, review, and follow-through worksheet.

Full-template use, or escalation from lite to full before downstream work depends
on the ticket, is required when any of these are present:

- high risk
- public/shared surface
- multi-ticket scope
- reusable acceptance
- migration/security/privacy boundary
- material ambiguity
- mandatory critique

When none of those triggers apply, the lite template is acceptable only if it can
still name scope, acceptance, evidence posture, live status/next move, blockers,
and journal facts truthfully.

```bash
token="$(LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c 8)"
stamp="$(date -u +%Y%m%d)"
slug="${LOOM_TICKET_SLUG:-}"

case "$slug" in
  ""|*[!a-z0-9-]*)
    printf 'Set LOOM_TICKET_SLUG to a lowercase slug before copying.\n' >&2
    exit 1
    ;;
esac

path=".loom/tickets/${stamp}-${token}-${slug}.md"
template="${LOOM_TICKET_TEMPLATE:-ticket.md}"
cp "loom-core/skills/loom-tickets/templates/${template}" "$path"
# package-root install alternative:
# cp "skills/loom-tickets/templates/${template}" "$path"
```

Set `LOOM_TICKET_TEMPLATE=ticket-lite.md` only after choosing the lite shape.
Then replace the placeholders in the copied file.

## Common Rationalizations

- **"The child said done, so I can close the ticket."** Reality: child output is
  input. Ticket-owned acceptance, evidence, critique, follow-through, and residual
  risk decide closure.
- **"This ticket is small, so evidence can stay in chat."** Reality: small tickets
  can use small evidence, but acceptance claims still need inspectable support or
  an explicit `not_required` rationale.
- **"I'll keep a claim matrix for every ticket because it is safer."** Reality:
  claim matrices are useful when coverage is complex. For simple tickets they add
  noise; inline acceptance and evidence links are clearer.
- **"The plan or packet says what happens next."** Reality: plans sequence and
  packets bound child work. Tickets own live execution state and acceptance
  disposition.

## Red Flags

- status says `closed` while evidence, critique, or promotion disposition is still pending
- acceptance criteria are vague enough that two implementations could both claim success
- assumptions that change behavior or UX are hidden in execution notes
- claim matrix rows duplicate simple coverage without adding clarity
- critique findings are listed without ticket-owned dispositions

## Verification

- [ ] `# Acceptance` names the owner and real covered IDs or ticket-local criteria.
- [ ] Evidence disposition says whether support is `sufficient`, `insufficient`, `challenged`, `stale`, `superseded`, `pending`, or `not_required`.
- [ ] Required critique policy and finding dispositions are closure-compatible.
- [ ] Assumptions or decision triggers are explicit, not silently converted into scope.
- [ ] Closure, if claimed, cites the ticket-owned acceptance basis.

## Done Means

- the ticket tells the truth about live execution
- status matches reality
- the current blockers, evidence gaps, review gaps, acceptance gaps, and journal
  make continuation legible to a fresh agent without a serialized workflow field
- evidence is linked, fresh enough for the acceptance claim, and explicit about
  observed support, observed challenge, and limitations; missing evidence is
  explicitly absent for a reason
- critique and retrospective / promotion follow-through are linked or explicitly
  pending, deferred, completed, or not required
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
7. `references/local-execution.md` when one bounded code, test, docs, config,
   refactor, migration, or cleanup change can be executed without a Ralph packet.
8. `references/acceptance-gate.md` when deciding whether closure is honest.
9. `templates/ticket-lite.md` or `templates/ticket.md` only when creating a
   ticket; keep `ticket.md` as the full copy target.
