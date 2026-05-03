# Loom Protocol

Loom is a Markdown-native protocol for AI-mediated software work.

It is not a runtime. The durable product is the record grammar and operating
discipline that lets agents work over one visible graph with ordinary files.

## Operating Axes

Loom is easiest to operate through three axes:

- **layers**: which artifact owns the next truth change
- **loops**: whether the work is being shaped, executed, reviewed, accepted, or promoted
- **packets**: the bounded contract for fresh-context implementation work and packetized sibling workflows

Those axes are not the ontology. They are the operator's first handle on the
protocol.

## Bootstrap

Loom's mandatory operating doctrine is packaged in `skills/loom-bootstrap`.
Agents must use `loom-bootstrap` before work unless an adapter has already loaded
the same ordered references into the current context. Harness adapters may preload
those references as always-on context, but that preload is an optimization over the
same doctrine, not a separate protocol surface.

## Kernel Roles

A Loom transaction uses seven kernel roles:

- **owners**: layers that own specific kinds of project truth
- **claims**: stable objective, requirement, acceptance, or local assertion IDs that need coverage
- **packets**: bounded contracts for fresh-context work
- **evidence**: observed artifacts that support or challenge claims
- **critique**: adversarial findings and verdicts
- **acceptance disposition**: the ticket-owned decision about whether scoped work may close
- **promotion**: retrospective assimilation into wiki, research, spec, plan, initiative, constitution, evidence, or memory

The important point is not the count. The important point is that every durable
claim, behavior, observation, risk, and explanation has one place where it
belongs.

## Acceptance Terms

Use these terms precisely:

- **acceptance contract**: spec-owned criteria, requirements, scenarios, and claim IDs
- **acceptance disposition**: ticket-owned decision about scoped claims, evidence, critique, retrospective / promotion follow-through, accepted risk, and closure
- **acceptance review**: workflow route that helps produce the ticket disposition

Specs own reusable acceptance contracts and intended behavior. Tickets may own
ticket-local acceptance criteria only when no separate spec exists and the
criteria are scoped to that ticket. If ticket-local criteria become reusable,
contradict a spec, or define behavior future work will depend on, create or
update the spec instead of letting the ticket become the behavior owner.

Initiatives may own strategic `OBJ-*` success criteria. Downstream tickets,
packets, evidence, and critique may cite those objective criteria, but tickets
own only their scoped coverage state and acceptance disposition.

Harness transports may invoke acceptance review. They do not own acceptance
disposition.

## Transaction State Machine

A Loom transaction moves through this spine:

```text
route -> shape -> ready -> execute -> reconcile -> verify -> accept -> promote -> close
```

- `route`: choose the owner layer and next route
- `shape`: refine owner records until the next move is unambiguous
- `ready`: make the ticket ready for the next route; Ralph-ready is stricter
- `execute`: perform the next governed route named by the owner graph and shared
  route vocabulary, such as `local_edit`, `ralph`, `debugging`, `spike`,
  `codemap`, `critique`, `wiki`, `retrospective`, `evidence`, `ship`, or
  `acceptance_review`
- `reconcile`: update ticket truth and any owner records affected by the result
- `verify`: record required evidence and critique disposition
- `accept`: record the ticket-owned acceptance disposition and whether closure is ready
- `promote`: assimilate durable learning into the owner layer that can maintain it
- `close`: move the ticket to `closed` only when the graph tells the full truth

If a step cannot be completed honestly, route backward instead of pretending the
machine advanced. Typical loopbacks are execution -> spec, critique -> ticket,
acceptance -> evidence, and promotion -> research/wiki/spec.

Ticket states bind to the spine this way:

| Transaction phase | Normal ticket state |
| --- | --- |
| `route` / `shape` | `proposed` until readiness is earned |
| `ready` | `ready` |
| `execute` | `active` |
| `reconcile` / `verify` | `active`, `blocked`, `review_required`, or `complete_pending_acceptance` depending on evidence, critique, and blockers |
| `accept` | `complete_pending_acceptance` records closure readiness, or loops back to `active` / `review_required` when gaps remain |
| `promote` | `complete_pending_acceptance` while required follow-through remains |
| `close` | transition to `closed` only after acceptance and required promotion/follow-through are complete or explicitly deferred |

## State And Lifecycle

Loom uses two different kinds of status:

- **live execution state** lives only in tickets
- **record lifecycle status** may appear on other records, but it describes only that record's age or authority

The shared non-ticket lifecycle grammar is defined in
`skills/loom-records/references/status-lifecycle.md`. The common vocabulary is
`draft`, `active`, `accepted`, `completed`, `stale`, `superseded`, and `retired`,
with layer-specific statuses such as packet `compiled|consumed|superseded|abandoned`,
evidence `recorded|superseded|invalidated`, and critique `draft|final|superseded`.

Do not let a packet, plan, wiki page, branch, PR, evidence record, or external
summary become the live ledger. Tickets own what is happening now.

## Owner, Route, Transport

Keep these categories separate:

| Category | Examples | What It Owns |
| --- | --- | --- |
| owner layer | constitution, initiative, research, spec, plan, ticket, evidence, critique, wiki | project truth by type |
| support surface | packet, memory, optional `.loom/support/` artifacts, workspace/harness records | recovery, recall, retrieval cues, bounded handoff, or scope support without owning project truth |
| execution route | `local_edit`, `ralph`, `debugging`, `spike`, `codemap`, `critique`, `wiki`, `retrospective`, `evidence`, `acceptance_review`, `ship` | a way to move work through owner layers; `ship` packages or hands off work without owning ticket closure |
| transport | slash command, subagent, headless CLI, manual handoff, harness adapter | invocation mechanics only |

Never choose a transport first and infer truth ownership from it. Choose the
owner, then the route, then the transport.

Use `skills/loom-records/references/route-vocabulary.md` for the canonical route
token list. Route tokens are grep-friendly Markdown vocabulary, not a runtime
enum, command router, or command truth.

## Claim Coverage Lifecycle

Claim coverage follows authority:

| Stage | Owner |
| --- | --- |
| define strategic objective criteria | initiative |
| define reusable requirement and acceptance criteria | spec |
| define ticket-local acceptance criteria when no spec exists | ticket |
| declare scoped coverage and current coverage state | ticket |
| name claims this bounded iteration should advance | packet |
| support or challenge claims with observed artifacts | evidence |
| challenge implementation shape or evidence sufficiency | critique |
| record final disposition for scoped claims | ticket |
| explain accepted understanding after settlement | wiki |

Use the shared ticket coverage states from
`skills/loom-records/references/claim-coverage.md`: `open`, `supported`,
`supported_pending_review`, `challenged`, `accepted_risk`, and `superseded`.
Projects may use more detailed states when the owning ticket explains them.

## Change And Risk Classes

Use `change_class` to name what kind of mutation is happening:

```text
record-hygiene | documentation-explanation | behavior-contract | code-behavior | protocol-authority | data-migration | security-sensitive | release-packaging
```

Use `risk_class` to name how dangerous the change is:

```text
low | medium | high
```

Change class selects likely evidence, critique, and verification posture. Risk
class can only tighten that default unless the ticket records a clear rationale.
During reconciliation, the parent may raise risk class. Lowering risk class
requires explicit ticket rationale.

## Core Protocol And Workflows

Canonical owner layers are persisted surfaces that own project truth:

```text
constitution
initiative
research
spec
plan
ticket
evidence
critique
wiki
```

Durable support surfaces help execution and recovery without becoming project
truth owners:

```text
packet
memory
support artifact
workspace support records
```

Saved support artifacts may live under optional, lazy-materialized
`.loom/support/` paths such as `.loom/support/drive-handoffs/`. They support
handoff and recovery; they do not own objective state, live ticket state,
acceptance, evidence sufficiency, critique verdicts, wiki truth, canonical truth,
or packet lifecycle.

Workspace support records include records such as `.loom/workspace.md` and
`.loom/harness.md` that document scope aliases, repository boundaries, or
fresh-context transport. They support routing; they do not own project truth.

Workflows are compositions through those layers:

```text
brainstorm
test-first implementation
debug
spike
sketch
code map
implementation
plan execution
parallel execution
git isolation
review
review response
accept
ship
branch finish
retrospective
repair
wiki write/audit
```

A workflow can be useful without becoming a new ontology. It should route into
the owner graph and leave truth in the layer that owns it.

Harness adapters may expose or preload the Loom skill package. They must not
define Loom truth.

## Check Principle

Markdown protocol first. Optional validators second.

A validator or native adapter can project Loom state, but it must not become the
authority for Loom semantics.
