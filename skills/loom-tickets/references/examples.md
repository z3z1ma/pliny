# Ticket Examples

## What To Notice In A Good Ticket

Look for these qualities:

- the summary names one coherent work item
- acceptance criteria are concrete enough to test
- implementation plan reflects the current expected path
- verification points to real evidence or clear next checks
- the journal captures meaningful changes in execution state

## Example Ticket Shape

A strong ticket usually has:

- one coherent work item in `Summary`
- enough context to explain why this work exists now
- a clear scope and clear non-goals
- acceptance that later verification can actually judge
- an implementation plan that teaches the next actor what to do
- a verification section that points to real evidence or real next checks

## Example Strong Ticket Summary

```text
Advance one bounded execution step for the packet compiler, verify the resulting contract shape, and reconcile the outcome into the ticket ledger.
```

## Example Ticket Creation Command

Use the shortest command that still makes the relationship graph explicit:

```bash
scripts/tickets.py create smoke-test-run \
  --status ready \
  --depends-on ticket:0002 \
  --path "repos/admin-ui/src/main.ts" \
  --link initiative:bootstrap-markdown-first-loom \
  --link plan:bootstrap-repository \
  --link spec:loom-repository-bootstrap \
  --link ticket:0004
```

`--link` accepts either `KEY=VALUE` or a record ref like `ticket:0004`, where the key is inferred from the ref prefix.

`--depends-on` is for hard upstream ticket prerequisites. Keep explanatory prose in the ticket `Dependencies` section even when the frontmatter edge exists.

## Example Dependency Mutation Command

```bash
scripts/tickets.py depends-on "ticket:0005" --add "ticket:0003"
```

Use this when the dependency edge should change without editing ticket frontmatter by hand.

The generated ticket id stays in `ticket:0004` form. The filename uses a scope-derived prefix such as `<repo-short-slug>-0004-smoke-test-run.md`, `multi-0004-smoke-test-run.md`, or `wksp-0004-smoke-test-run.md`.

Before creating a new ticket, scan the ticket ledger for an existing work item with overlapping ownership so you do not split execution truth accidentally.

## Worked Ticket Excerpt

```text
Summary
Execute one bounded smoke run for the root Loom repository and record the result as durable verification evidence.

Context
The workflow definition already exists, but a separate execution ticket is needed so one concrete run and its evidence can be tracked without overloading the workflow-design ticket.

Scope
- run the current smoke path in the root repository
- capture one verification record with command and outcome evidence
- record any failures, drift, or ambiguity honestly

Acceptance Criteria
- the smoke workflow is executed against the intended repository scope
- one durable verification record captures commands and outcomes
- any discovered blocker or failure is written into the ticket rather than implied

Implementation Plan
- confirm the command set from the governing workflow ticket
- run the bounded smoke checks
- create a verification record
- update the ticket status, verification section, and journal based on the run result
```

Why this is strong:

- it distinguishes workflow design from one concrete execution ticket
- the next actor knows what to run and what evidence must exist
- failure handling is explicit

## Example Journal Entry Pattern

Good ticket journal entries look like this:

```text
- 2026-03-31: refreshed packet contract after governing spec changes and updated verification expectations accordingly
```

The entry is durable because it says what changed and why that mattered to execution state.

## Example Weak Ticket Entry

This is weak:

```text
- made progress on the task
```

It is weak because a later reader cannot tell what changed, why it mattered, or what should happen next.

## Better Journal Entry Pattern

```text
- 2026-04-01: ran the bounded smoke checks against `repo:repos-admin-ui`, recorded command and outcome evidence in `verification:smoke-run-2026-04-01`, and left the ticket `blocked` because one downstream dependency still required a second repository owner.
```

Why this is strong:

- the change is specific
- the evidence is linked
- the next status implication is obvious
