# Candidate: Records-First Retrieval

Candidate ID: `candidate-records-first-retrieval-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: keep-testing
Promotion: manual-only

## Target Behavior

When the user asks about a surface whose context may already exist in `.10x`,
the agent should answer from records before interviewing the user. It should
cite the records it used, ask only if the records leave a named
execution-critical gap, and avoid creating duplicate records unless new durable
context emerges.

This is an instruction overlay candidate. It is not a canonical change to
`SKILL.md`.

## Proposed Instruction Overlay

Add this record retrieval rule:

```text
When the user asks about existing project context, prior decisions, terminology,
constraints, or next work, search and read the relevant `.10x` records before
asking the user to restate context.

After reading records:

1. Answer from the records and cite the record paths used.
2. Separate settled record-backed facts from gaps or stale assumptions.
3. Ask a follow-up only when the records leave an execution-critical gap, and
   name what decision the answer unlocks.
4. Do not create duplicate research, decisions, tickets, or knowledge records
   for context already present in `.10x`.
5. Create or update a record only when the current turn adds new durable context
   beyond what the existing records already contain.
```

## Expected Score Movement

- S001 Outer Loop Discipline: should improve by satisfying inspect-before-ask
  when records already answer the user.
- S002 Record Graph Fitness: should improve by avoiding duplicate records and
  preserving record-backed context.
- S007 Human Shaping Quality: should improve because the user is not asked to
  repeat settled context.

## Scenario Coverage

Primary scenario:

- SCN-003 existing-records-answer-the-question

Secondary scenarios:

- SCN-001 ambiguous-implementation-request
- SCN-006 ticket-boundary

## Expected Failure Modes

- Citation theater: citing record paths without actually using their content.
- Stale-record overtrust: treating old records as current when revalidation is
  needed.
- Under-questioning: failing to ask a necessary follow-up when records leave a
  real execution-critical gap.

## Promotion Boundary

This candidate cannot be promoted without live evidence, manual inspection,
held-out checks, review, and explicit human promotion. It must not directly edit
`SKILL.md`.

## Result

`EXP-20260623-826-records-first-retrieval-scn003-live-micro` kept this candidate
for further testing. Candidate scored `S001=100;S002=60;S007=80` versus current
`S001=100;S002=50;S007=60`; manual inspection favored candidate retrieval
clarity. Not promoted.

`EXP-20260623-827-records-first-retrieval-no-citation-scn003-live-micro`
repeated the same positive vector without explicit prompt wording to cite record
paths. Still not promoted; next confidence step is fresh-record retrieval.
