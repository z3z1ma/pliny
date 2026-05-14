# Ticket Shape

A good ticket is prose-rich but not vague.

It contains enough instruction, context, record links, scope, acceptance, current
state, and work history for a future agent to compile Ralph packets, consume
packet output, or continue the bounded work unit from the ticket and its linked
records.

A ticket is not a scratchpad, ambiguous ask, transcript summary, planning
substitute, or research note.

## Top Labels

Use these labels near the top:

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

`Priority:` is for sequencing pressure, not importance theater.

`Depends On:` is for hard prerequisites only. Loose relevance belongs in
`## Related Records`.

## Risk

Risk must include a reason.

Use:

* `low` when the change is narrow, reversible, and easy to verify
* `medium` when the change touches meaningful behavior, shared records, important
  workflow semantics, or non-trivial integration points
* `high` when the change affects core architecture, safety, data integrity,
  migration behavior, public contracts, or hard-to-reverse decisions

Raise risk when evidence is hard to gather or failure would be expensive.

## Core Sections

Use the default sections unless a ticket has a strong reason to vary:

* `## Summary`
* `## Related Records`
* `## Scope`
* `## Acceptance`
* `## Current State`
* `## Journal`

Remove `## Related Records` only when no existing records materially constrain or
inform the work.

`## Journal` stays last so agents and tools can append to the bottom.

## Summary

Summary should answer:

* what bounded executable work exists
* why it matters
* what outcome should be true when complete
* what context an acting agent needs before compiling the first Ralph packet

It should also make the single closure claim easy to see. If the Summary needs to
bundle independent stack, data, UI, feature, migration, review, and verification
outcomes, the work probably belongs in a plan with child tickets.

Keep it short, but not empty-calorie. The Summary should make the ticket
understandable without relying on chat history.

## Related Records

Use `## Related Records` when an acting agent should read specific records before
work.

Each entry should explain why the record matters, not only name the ID.

Example:

```markdown
- `<spec-id>` - defines the intended status semantics this ticket must preserve.
- `<research-id>` - records the tradeoffs behind the chosen implementation route.
```

Add only records that materially constrain or explain the ticket.

If a record is required to compile or run the ticket's Ralph packets safely,
include it. If the ticket depends on context that exists only in chat, move the
durable version into the ticket or the appropriate linked record.

## Scope

Scope can be prose, but it needs a real boundary.

Good scope names:

* what may be changed
* what must not be changed
* likely files, records, directories, commands, or interfaces involved
* assumptions the acting agent may rely on
* non-goals that would otherwise invite scope creep
* system-shape, data-modeling, state-modeling, abstraction, or coherence
  constraints that bound the change

If the scope cannot be bounded, the ticket is not ready.

If the ticket would require the acting agent to decide what the design is, what to
leave out, which data model or state model should exist, or which abstraction
should carry the work, the ticket is not ready. Shape that truth first or link the
owning record.

If the first Ralph packet boundary cannot be identified from the ticket and linked
records, the ticket is not ready.

## Acceptance

Every ticket has acceptance IDs.

Use `ACC-001`, `ACC-002`, and so on. Cite them outside the ticket as:

```text
ticket:YYYYMMDD-<slug>#ACC-001
```

Acceptance criteria should be observable. They should include the evidence needed
for closure and the audit target, lens, or explicit reason a separate audit would
not add useful trust.

Good acceptance criteria say what must be true and how that truth will be known.

Avoid vague criteria like:

* works
* looks good
* cleaned up
* improved
* aligned
* handled
* finalized

Those are acceptable only when made observable.

## Current State

Current State is a narrative snapshot of where the work stands now.

It can mention:

* progress
* blockers
* evidence
* audit state
* residual risk
* open decisions
* next likely move

Keep it current enough for a future agent to resume from the ticket and linked
records.

For a new ticket, Current State should usually say whether the ticket is ready to
start and what the first likely Ralph packet is.

Update it when the real state changes materially.

## Journal

The journal is append-friendly and stays at the bottom.

Append material entries for:

* progress
* decisions
* blockers
* evidence
* audit results
* status changes
* scope or acceptance changes
* closure or cancellation

Use short dated entries when helpful:

```markdown
- YYYY-MM-DD: Set status to active and inspected related records before editing.
- YYYY-MM-DD: Ran `pytest ...`; tests passed. ACC-001 and ACC-002 satisfied.
```

Do not rewrite history to make the work look cleaner. Correct errors when needed,
but preserve the material path.

## Closure Shape

A closed ticket should make trust cheap.

Before closure, the ticket should show:

* what changed
* why the change satisfies acceptance
* what evidence exists
* what audit happened, or why a separate audit was intentionally not useful
* what residual risk remains, if any
* why `Status: closed` is truthful

Close when the ticket, linked records, evidence, and audit state support the
closure claim.
