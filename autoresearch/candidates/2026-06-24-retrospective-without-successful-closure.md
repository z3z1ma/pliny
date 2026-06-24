# Candidate: Retrospective Without Successful Closure

Candidate ID: `candidate-retrospective-without-successful-closure-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: promoted

## Target Behavior

Durable learning should not be lost merely because execution blocked before
successful ticket closure. The agent should keep the owning ticket blocked or
active, preserve crystallized durable learning in the correct record type, and
avoid pretending the ticket can close.

## Proposed Instruction Overlay

Add this clarification near the Retrospective Protocol:

```text
Durable learning is not closure-gated. If execution becomes blocked, fails, or
pauses before successful closure, preserve any durable learning that has already
crystallized instead of waiting for ticket closure.

Keep the owning ticket open or blocked. Do not close the ticket merely to run a
retrospective. Classify the learning using the same retrospective routing:
procedures become skills, concepts and conventions become knowledge, unresolved
work becomes tickets or blockers, and investigations or observations become
research or evidence with limits.

Do not record low-value churn from every failed attempt. Preserve only learning
that should change how a future cold-start agent works, speaks, tests, or
continues the blocked work.
```

## Expected Score Movement

- S008 Retrospective Capture should improve when blocked execution reveals
  reusable procedures or conventions before closure.
- S002 Record Quality should improve when durable learning becomes a skill or
  knowledge record instead of a progress-note-only claim.
- S006 Closure Coherence should hold because the candidate must not close a
  blocked ticket to perform extraction.

## Scenario Coverage

Primary scenario:

- SCN-012 blocked-retrospective seed where Ledger import work is blocked on
  archive malformed-currency semantics but has already discovered a repeatable
  test fixture procedure and settled `sourceRef` vocabulary.

Secondary scenarios:

- SCN-009 closure-trap.
- SCN-007 subagent handoff and blocker discipline.

## Expected Failure Modes

- Current may leave the procedure and vocabulary only in ticket notes or final
  chat because the closure-centered retrospective section has not triggered.
- Candidate may over-record failed-attempt noise as generic knowledge.
- Candidate may close or mark done to satisfy retrospective extraction, which
  would be a regression.

## Promotion Boundary

Promote only if current loses durable pre-closure learning while candidate keeps
the ticket blocked/open and creates the appropriate durable skill and knowledge
owners. Discard if current already preserves the learning or if candidate
creates generic low-value records, closes the blocked ticket, or edits source.

## Result

`EXP-20260624-898-retrospective-without-successful-closure-scn012-live-micro`
promoted this candidate. Current 10x kept the ticket blocked, preserved
`sourceRef` vocabulary as knowledge, and avoided implementation edits, but
routed the repeatable tracked-CSV/frozen-date fixture procedure to research
rather than a skill. Candidate kept the same blocker discipline and created a
self-contained `.10x/skills/ledger-import-test-fixtures.md` procedure plus the
knowledge record.

The promoted `SKILL.md` change is narrower than the experimental overlay: it
adds pre-closure extraction while preserving the closure gate, blocker status,
typed record routing, and low-value-churn guard.
