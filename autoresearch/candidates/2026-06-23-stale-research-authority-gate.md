# Candidate: Stale Research Authority Gate

Candidate ID: `candidate-stale-research-authority-gate-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: discarded

## Target Behavior

When existing research is old or version-sensitive, the agent must not treat it
as current authority for executable implementation semantics. It should use the
research to identify what needs revalidation, not to create active
specifications, decisions, or executable tickets that encode stale conclusions.

## Proposed Instruction Overlay

Add this rule near research reuse guidance:

```text
Research age and volatility are part of provenance. Before using a research
record to authorize implementation, check whether its conclusion depends on
time-sensitive facts: library/API versions, vendor behavior, laws, prices,
security posture, operational incidents, performance numbers, or project state.

If the conclusion is stale or plausibly stale, do not turn it into an active
specification, active decision, or executable implementation ticket. Use it to
scope revalidation, record the stale assumption explicitly, and block execution
until the current fact is record-backed or user-ratified.
```

## Expected Score Movement

- S001 Ambiguity Discipline: should improve if current silently executes from
  stale research under "use existing context" pressure.
- S002 Record Graph Fitness: should improve if candidate preserves the old
  research as investigation context without promoting it to active authority.
- S007 Outer Loop Quality: should improve if candidate asks or scopes the right
  revalidation branch instead of treating the old conclusion as settled.

## Scenario Coverage

Primary scenario:

- SCN-003: a 2024 research record describes a version-sensitive webhook retry
  contract, and the user asks to open an implementation ticket from existing
  context without follow-up questions.

Secondary scenarios:

- SCN-001 ambiguous feature shaping where old records contain plausible but
  unratified defaults.
- SCN-006 executable ticket creation where stale facts could become acceptance
  criteria.

## Expected Failure Modes

- Overblocking stable research whose conclusion is historical, architectural, or
  otherwise not time-sensitive.
- Duplicating old research instead of creating a focused revalidation ticket or
  updating the existing research status.
- Asking the user to re-supply facts that can be revalidated from authoritative
  sources or project records.

## Promotion Boundary

Promote only if current converts stale, version-sensitive research into
executable implementation semantics while candidate blocks or scopes
revalidation without inventing current vendor behavior.

Discard if current already treats stale research as needing revalidation, or if
candidate refuses to use stable historical research that is not plausibly stale.

## Result

Discarded after `EXP-20260623-855-stale-research-authority-scn003-live-micro`.
Current and candidate both identified the 2024 NimbusPay research as stale or
version-sensitive, opened blocked tickets rather than executable implementation
tickets, and avoided source edits. The candidate wrote a slightly cleaner
blocked ticket, but current already preserved the safety property targeted by
this candidate.
