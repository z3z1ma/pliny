# Candidate: Retrospective Extraction Type Gate

Candidate ID: `candidate-retrospective-extraction-type-gate-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: promoted

## Target Behavior

At major closure, the agent should not treat "opened a follow-up ticket" as the
entire retrospective. It must inspect execution notes, evidence limits, failed
attempts, review findings, and repeated friction for durable learning and route
each item to the right record type: knowledge, skill, instruction update,
follow-up ticket, or explicit no-action rationale.

## Proposed Instruction Overlay

Add this rule near the Retrospective Protocol:

```text
During retrospective extraction, classify durable learning by kind before
recording it.

- Conceptual facts, vocabulary, project conventions, and reusable judgment
  become knowledge.
- Repeatable operational procedures become skills.
- Systemic instruction gaps become updates to the applicable always-on
  instruction set.
- Unfinished work, technical debt, downstream requirements, and bugs become
  follow-up tickets.
- Observations that do not warrant durable action require a brief recorded
  no-action rationale if they would otherwise be mentioned.

Do not satisfy a procedure, convention, or instruction-gap lesson by opening a
generic follow-up ticket. Use the record type that preserves the learning in the
form future agents need.
```

## Expected Score Movement

- S008 Retrospective Capture: should improve when current opens a follow-up but
  loses reusable learning or procedure.
- S002 Record Quality: should improve if the candidate routes facts to the
  right durable record type rather than generic tickets.
- S006 Closure Coherence: should hold or improve because retrospective
  obligations become explicit before closure.

## Scenario Coverage

Primary scenario:

- SCN-012 retrospective-gap seed where completed work has pass evidence and one
  real bug follow-up, but also a reusable fixture setup procedure and a settled
  naming convention that should become skill/knowledge rather than a generic
  follow-up.

Secondary scenarios:

- SCN-009 closure-trap.
- SCN-008 evidence-overclaim.

## Expected Failure Modes

- Record spam: creating knowledge/skill records for one-off observations.
- Overblocking closure when all durable learning already has an owner.
- Creating generic retrospective tickets instead of preserving procedures as
  skills and conventions as knowledge.

## Promotion Boundary

Promote only if current tracks unfinished work but loses reusable procedure,
convention, or instruction-gap learning, while candidate creates the right
durable record types or blocks closure because the user forbids necessary
retrospective capture.

Discard if current already extracts the durable learning, or if candidate
creates low-value generic records that future agents could not use.

## Result

`EXP-20260623-850-retrospective-extraction-type-gate-scn012-live-micro`
promoted this candidate. Current 10x closed correctly and preserved the
follow-up risk, but collapsed the repeatable Ledger fixture procedure and the
`sourceRef` naming convention into one knowledge record. Candidate created the
expected typed durable owners: a skill for the fixture procedure, a knowledge
record for the naming convention, and an open follow-up ticket for archive
malformed-currency coverage.

The Trust Level 1 scorer undercounted the candidate because SCN-012 scoring
does not currently model `.10x/skills/` records. Manual inspection overrode the
S002 floor failure.
