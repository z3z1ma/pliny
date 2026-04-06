# Tickets Schema Reference

## Purpose

Tickets remain the sole live execution ledger.

Use the ticket schema to keep current execution truth inspectable and resumable.

Tickets should be written as self-contained units of execution.

A novice reader should be able to pick up the ticket, read its explicit links, and understand what to do next without reconstructing the task from hidden context or prior chat.

Ticket refs remain stable as `ticket:0001`, while ticket filenames use a repository-derived prefix such as `<repo-short-slug>-0001-<slug>.md`.

## A Strong Ticket Answers

1. what work item this is
2. why it matters now
3. what is in scope
4. what counts as done
5. what implementation path is currently intended
6. what verification exists or is still needed
7. what materially changed over time
8. what documentation obligation follows from the work

It should also answer whether another agent could resume execution truthfully from the ticket alone plus its explicit links.

It should also answer what the next actor should do, what evidence they should produce, and what would count as blocked or complete.

## Section Guidance

- `Summary`: define the work item in one durable statement
- `Context`: capture background that changes how the work should be interpreted
- `Why This Work Matters Now`: explain urgency or ordering
- `Scope`: list what the ticket currently includes
- `Non-goals`: keep the execution boundary visible
- `Acceptance Criteria`: define what must be true before closure
- `Implementation Plan`: describe the current best execution path
- `Dependencies`: identify upstream blockers or required linked work
- `Risks / Edge Cases`: preserve known complexity
- `Verification`: say what evidence already exists and what is still required
- `Documentation Disposition`: state whether docs work is required, deferred, or unnecessary
- `Journal`: append material changes over time

Each section should be specific enough that a fresh agent knows what it is for. Placeholder headings with placeholder prose are not enough.

## Frontmatter Expectations

Tickets should preserve:

- stable `id` like `ticket:0001`
- `kind: ticket`
- truthful `status`
- `repository_scope`
- `depends_on` for hard upstream ticket prerequisites that should be machine-visible
- links to governing plan, spec, initiative, related tickets, critique, docs, and verification where relevant
- timestamps that move when the durable execution state changes

Ticket ids remain stable as `ticket:<number>`. Ticket filenames may include a repository-derived prefix such as `<repo-short-slug>-0001-<slug>.md`.

## Dependency Semantics

Use first-class `depends_on` frontmatter when another ticket is a real upstream prerequisite for this one.

Use the prose `Dependencies` section and `Journal` to explain why the dependency matters, what is blocked, and what evidence or handoff is still needed.

Use frontmatter `links.ticket` for related ticket references that are informative but not strict prerequisites.

If a ticket is blocked by another ticket, prefer both:

- `status: blocked`
- the blocking ticket ref in `depends_on`

## Ticket Writing Standard

Good Loom tickets are:

- detail-first instead of blurb-first
- explicit about why the work matters now
- explicit about scope and non-goals
- specific enough that a novice can continue from them
- concrete about verification and docs disposition

Good tickets do not just store execution state. They teach the next actor how to continue that execution truthfully.

That usually means the ticket should contain enough context and direction to answer:

- what exact outcome is being pursued
- what constraints govern the work
- what the likely path is
- what evidence must exist before closure
- what to do if the work blocks or uncovers new risk

## Status Interpretation Guidance

- `proposed` means the work exists conceptually but is not yet ready to execute
- `ready` means another agent could begin safely from the ticket
- `active` means execution is underway now
- `blocked` means the ticket cannot proceed without some explicit upstream resolution
- `review_required` means execution progressed far enough that critique or acceptance review is the next durable step
- `complete_pending_acceptance` means the work and verification are largely done, but formal acceptance or reconciliation remains
- `closed` means the durable state truthfully supports completion
- `cancelled` means the work is intentionally no longer being pursued

## Ticket Reconciliation Discipline

If a packet run, critique pass, or docs update changes execution reality, the ticket should absorb that durable truth.

That usually means updating:

- status
- acceptance interpretation
- verification
- journal
- linked evidence
- docs disposition

## Worked Ticket Mindset

Write the ticket as if the next person to read it is capable but unfamiliar with the local history.

They should not have to guess:

- which artifact actually owns the work
- which evidence matters most
- which scope boundaries are important
- whether docs or critique are expected next

## Ticket Ledger Rule

If a run artifact, critique result, or docs update changes the execution reality, the ticket should be updated so a future agent can resume from the ticket without reconstructing hidden state.

## Failure Cases To Avoid

- a ticket that claims completion without evidence
- a ticket that never records a blocker even though execution stalled
- a ticket whose journal is stale after meaningful packet or critique activity
- a ticket that pushes execution truth into neighboring layers instead of concentrating it locally

## Done Means

- the ticket clearly owns the live execution truth
- status, verification, and docs disposition are truthful
- the journal reflects meaningful execution changes
- another agent can resume from the ticket plus its explicit links
