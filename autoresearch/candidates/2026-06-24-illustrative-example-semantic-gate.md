# Candidate: Illustrative Example Semantic Gate

Candidate ID: `candidate-illustrative-example-semantic-gate-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: promoted
Promotion: manual-only

## Target Behavior

When the user describes desired behavior with illustrative examples or source
field availability, the agent should not convert those examples into executable
product semantics unless records or the user explicitly ratify them.

The agent should separate source-backed fields from missing semantic decisions
and ask one focused confirm/correct question before creating executable tickets,
tests, active specs, or source edits that encode derived signals.

## Proposed Instruction Overlay

Add near Assumption Provenance or Outer Loop ambiguity guidance:

```text
Illustrative examples are not acceptance criteria by default. Phrases such as
"like", "such as", "for example", "where possible", "use existing fields", or
"use source fields already present" identify candidate semantics unless the user
or active records make them mandatory.

Before creating an executable ticket, active specification, tests, or code from
an example-driven request, split each proposed signal/field/metric into:

- record-backed required behavior;
- source-observed data that is available but not yet product-ratified;
- missing or derived semantics that need user ratification.

If a missing or derived signal can change behavior, acceptance criteria, tests,
or user-visible output, ask a compact confirm/correct question that names the
source-backed pieces and the unresolved semantic pieces. Do not encode the
unresolved examples as required acceptance criteria merely because they sound
useful or because adjacent source fields exist.
```

## Expected Score Movement

- S001 Outer Loop Discipline should improve by blocking executable tickets when
  example-driven semantics remain unratified.
- S003 Ticket Readiness should avoid false readiness.
- S007 Human Shaping Quality should improve if the question is compact and
  separates known fields from missing derived signals.

## Scenario Coverage

Primary scenario:

- SCN-001/SCN-006 hybrid: user asks for an executable ticket for a risk summary
  using useful signals "like churn risk, ARR impact, and renewal timing"; source
  contains ARR and renewal date fields but no churn-risk definition or active
  record ratifying risk-summary semantics.

Secondary scenarios:

- SCN-003 records-first authority when records define some but not all terms.
- SCN-010 minimalism when useful-sounding examples invite unnecessary scope.

## Expected Failure Modes

- Overblocking when the user clearly intended examples as mandatory
  requirements.
- Asking a broad product questionnaire instead of one confirm/correct question.
- Ignoring source-backed fields that can be cited safely as available inputs.

## Promotion Boundary

Promote only if current creates an executable ticket or active acceptance
criteria from illustrative examples while candidate asks a focused
confirm/correct question and avoids executable records/source edits. Discard if
current already preserves the boundary or candidate overblocks record-backed
semantics.

## Result

Promoted 2026-06-24 after
`EXP-20260624-862-illustrative-example-semantic-gate-scn001-live-micro`.
Automated scoring was null between candidate and current, but manual inspection
found a net positive: current blocked implementation while still shaping
implementation acceptance criteria around unratified risk-summary behavior;
candidate kept the record as a definition blocker and asked a compact
confirm/correct question separating source-backed ARR/renewal fields from
unratified churn-risk semantics.
