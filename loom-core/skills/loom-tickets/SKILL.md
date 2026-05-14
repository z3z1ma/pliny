---
name: loom-tickets
description: "Manages Loom tickets: creates, scopes, prepares Ralph execution, updates, blocks, reviews, closes, and cancels self-contained bounded work units under .loom/tickets. Use whenever the user mentions tickets, scoping changes, implementing work, continuation from prior work, or closing/reviewing a scoped work item."
---

# loom-tickets

Tickets are Loom's fundamental unit of executable work.

A ticket owns one bounded change, live execution state, acceptance criteria,
material progress, evidence links, review posture, and closure. Ralph packets own
the bounded execution and review slices that act on the ticket.

A ticket contains enough instruction and context to compile Ralph packets from the
ticket and its linked records, then gives future agents a safe continuation point
after those packets return.

A ticket is not a vague issue, planning document, research note, scratchpad,
transcript summary, or parking lot.

Do not use a ticket to hide unresolved outer-loop judgment. Scope-selection,
exclusions, system-shape, data-model or state implications, design coherence, and
evidence posture must be settled enough, or owned by linked records, before a
ticket becomes executable.

## Use This Skill When

Use this skill when the task involves:

- creating a ticket
- deciding whether work is ready for a ticket
- shaping executable work into a ticket
- acting from an existing ticket
- resuming ticket work
- updating status, scope, acceptance, current state, blockers, or journal
- moving work to review
- closing or cancelling a ticket
- summarizing or inspecting ticket state

Do not create a ticket to force premature execution.

If the work is mainly behavior discovery, sequencing, tradeoff analysis, durable
policy, architectural judgment, data-model or state-modeling choice, coherence
question, ambiguous intent, or reusable knowledge, route it to the appropriate
surface first.

## Dispatch

If creating or shaping a ticket:

- read `references/creating-tickets.md`
- read `references/ticket-shape.md`
- inspect relevant records and source before asking the operator to repeat facts
- create the ticket only when value, executable boundary, scope, context, and
  acceptance are clear enough to act
- ensure scope, system-shape, data-model, state, coherence, and evidence choices
  are either settled in the ticket or linked to owning records
- use the single-closure-claim check: one ticket should produce one bounded result
  with one coherent evidence and closure story
- include enough instruction and record links that the first Ralph packet can be
  compiled from the ticket and its linked documents without relying on chat history

If acting from, resuming, updating, blocking, reviewing, closing, or cancelling a
ticket:

- read the whole ticket
- read `references/acting-on-tickets.md`
- read or already know the records named in `## Related Records`
- keep work inside the ticket boundary
- use `loom-ralph` for each bounded implementation, review, source-inspection, or
  audit slice that acts on the ticket
- update the ticket when future continuation would be worse without the update

If only finding, listing, or summarizing tickets:

- inspect `.loom/tickets/`
- report state without mutating records unless the operator asked for a change

## Finding Tickets

Tickets live under `.loom/tickets/`.

Useful starting points:

```bash
find .loom/tickets -name '*.md' -print 2>/dev/null | sort
grep -R '^ID: ticket:' .loom/tickets 2>/dev/null || true
grep -R '^Status:' .loom/tickets 2>/dev/null || true
grep -R '^Risk:' .loom/tickets 2>/dev/null || true
grep -R '^Priority:' .loom/tickets 2>/dev/null || true
grep -R '^Depends On:' .loom/tickets 2>/dev/null || true
```

When looking for a specific ticket, prefer ID and filename matches before fuzzy
search.

## Ticket IDs And Filenames

Use `ticket:YYYYMMDD-<slug>` IDs.

Use matching filenames without the `ticket:` prefix:

```text
.loom/tickets/YYYYMMDD-<slug>.md
```

Use the actual current date. Do not copy example dates.

If the slug would collide, choose a clearer slug or add a numeric suffix.

## Required Top Labels

Tickets use plain body labels near the top:

```text
ID: ticket:YYYYMMDD-<slug>
Type: Ticket
Status: open
Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Risk: low|medium|high - reason
```

Add only when useful:

```text
Priority: low|medium|high - reason
Depends On: ticket:YYYYMMDD-<slug>
```

Use `Depends On:` only for hard prerequisites. Do not use it for loose relevance.

Update `Updated:` whenever materially changing status, scope, acceptance, current
state, blockers, evidence, review posture, or closure state.

## Status Lifecycle

Use this lifecycle:

* `open`: ready to start
* `active`: Ralph packet execution is underway or returned output is being
  reconciled into the ticket
* `blocked`: a concrete blocker prevents safe progress
* `review`: audit, acceptance review, or final verification is the next honest move
* `closed`: acceptance is satisfied and the ticket tells a truthful story
* `cancelled`: the work should not proceed, with the reason recorded

Tickets are not created as drafts.

If material questions remain, keep shaping outside the ticket or route to the
owning Loom surface.

## Default Template

Use `templates/ticket.md` as the default starting point. Keep the ticket bounded,
self-contained, grepable, actionable, and safe for continuation.

## Ticket Invariants

Every ticket must preserve these invariants:

* one bounded executable work unit
* one coherent closure claim
* enough context, instruction, and linked records to compile Ralph packets without
  chat history
* truthful `Status:`
* explicit scope boundary
* settled or linked scope, system-shape, data-model, state-modeling, and coherence
  choices relevant to execution
* concrete `ACC-*` acceptance criteria
* current state that reflects reality now
* material progress recorded in the journal
* evidence proportional to the closure claim
* related records read before they are relied on
* no unrelated cleanup
* no opportunistic batching
* no ambiguous asks disguised as executable work
* no silent expansion of scope
* no closure unless acceptance, evidence, and audit have been handled truthfully

If any invariant stops holding, update the ticket, split the work, block the
ticket, route back to shaping, or move it to the appropriate surface.

## Working From A Ticket

When executing from a ticket:

* set `Status: active` when work materially begins
* compile or consume a Ralph packet for the bounded ticket slice being implemented,
  reviewed, inspected, or audited
* execute from the Ralph packet, ticket, and linked records, not from unstated chat
  context
* keep implementation inside the declared scope
* update Current State when the next agent would otherwise be misled
* append journal entries for material progress, blockers, decisions, evidence,
  review, and closure
* record evidence where the evidence surface expects it
* do not rewrite acceptance criteria to match the implementation after the fact
* do not close over unresolved risk by making the ticket prose vaguer

Small edits do not require constant ticket churn. Update the ticket when the graph
would otherwise stop telling the truth.

## Blocking

Use `Status: blocked` only for a concrete blocker.

A blocked ticket should say:

* what is blocked
* why progress is unsafe or impossible
* what is needed to unblock
* who or what owns the next move, if known

Do not use `blocked` for ordinary uncertainty that should instead return to
shaping, research, specs, or planning.

## Review And Closure

Use `Status: review` when implementation may be complete but acceptance,
verification, audit, or final judgment is still the next honest move.

Close only when:

* each `ACC-*` item is satisfied or revised with authority before closure
* any unsatisfied acceptance is handled by a non-closed status, cancellation,
  authorized scope change, or follow-up work instead of hidden inside closure
* evidence supports the closure claim
* audit has happened, or the ticket explains why a separate audit would not add
  useful trust
* Current State reflects the final state
* the Journal records closure
* remaining risks or follow-ups are explicit

Close when the ticket, evidence, audit state, and affected records tell one
truthful story.

## Cancelling

Use `Status: cancelled` when the work should not proceed.

A cancelled ticket should record:

* why it was cancelled
* what changed or was learned
* whether any partial work remains
* where the durable truth moved, if anywhere

Cancellation is not failure. It is a truthful terminal state.

## Done Means

Ticket work is done when:

* the ticket still describes one bounded executable work unit
* the ticket and its linked records contain enough context to compile Ralph packets
  or trust returned packet output without chat history
* `Status:` matches reality
* `ACC-*` acceptance criteria are satisfied or revised with authority before
  closure
* evidence and audit state are truthful
* Current State says where the work stands now
* the Journal records material progress, blockers, decisions, evidence, review,
  and closure
* a future agent can continue or trust closure from the graph
