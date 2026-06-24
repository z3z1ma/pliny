# Candidate: Fish Before Opening Pressure

Candidate ID: `candidate-fish-before-opening-pressure-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: active

## Target Behavior

When the user explicitly says to open a ticket, the agent must still fish
through existing active, done, and cancelled tickets before creating one. If an
existing ticket already owns the issue, the request is satisfied by reusing or
updating that owner rather than creating a duplicate.

## Proposed Instruction Overlay

Add this rule under "Fish Before Opening":

```text
An explicit request to "open a ticket" does not override fish-before-opening.
First search active, done, and cancelled tickets for the same issue, behavior,
or durable owner.

If an active ticket already owns the issue, update that ticket with any new
context and tell the user it is the existing owner. Do not create a duplicate
ticket merely to satisfy the wording of the request.

If a done or cancelled ticket appears to own the issue, read it before deciding
whether the current report is a regression, a reopened issue, a distinct scope,
or already handled. Create a new ticket only when the current work is materially
distinct or the previous owner is terminal and no longer adequate.
```

## Expected Score Movement

- S002 Record Graph Fitness: should improve if current creates a duplicate
  ticket instead of updating the single durable owner.
- S005 Scope Minimalism: should improve if candidate satisfies the request with
  the smallest coherent record update.

## Scenario Coverage

Primary scenario:

- SCN-005: active ticket already owns a CSV export quote/newline coverage gap,
  and the user asks to open a follow-up ticket for that same gap.

Secondary scenarios:

- SCN-003 existing records answer the question.
- SCN-009 closure-time follow-up capture where a similar ticket already exists.

## Expected Failure Modes

- Over-deduplication: merging distinct issues into one stale ticket because the
  words look similar.
- Under-tracking: refusing to create a new ticket when the prior ticket is done
  or cancelled and the current issue is materially distinct.
- Chat-only reuse: saying an existing ticket exists but not recording the new
  context anywhere when the new report adds durable details.

## Promotion Boundary

Promote only if current creates a duplicate ticket or leaves new durable context
only in final prose while candidate reuses/updates the existing owner without
creating duplicate work.

Discard if current already reuses the existing ticket, or if candidate collapses
materially distinct issues into one ticket.
