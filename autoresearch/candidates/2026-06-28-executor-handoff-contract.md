# Candidate: Executor Handoff Contract

Candidate ID: `candidate-executor-handoff-contract-v1`
Created: 2026-06-28
Canonical target: `SKILL.md`
Status: draft
Promotion: manual-only

## Target Behavior

Improve `S010` by making executable tickets and parent/child handoffs easier
for a fresh implementation agent to execute without rediscovery.

## Proposed Instruction Overlay

Add near the Tickets and Inner Loop rules:

```text
Before marking a ticket executable or handing work to a child/subagent, read it
as the next executor. The record must name the objective, governing spec or
authority, explicit exclusions, semantic blockers or assumptions, first source
or record locations to inspect, edge cases and boundaries, expected evidence,
and the next concrete action. Keep this compact; if another active record owns
the detail, link it and state the exact role it plays. A ticket with acceptance
criteria but no provenance, first inspection target, or evidence path is not
cold-start ready.
```

## Expected Score Movement

- Strongest on `SCN-006` ticket-boundary seeds and parent/child handoffs.
- May also improve closure coherence by making evidence expectations explicit.

## Expected Failure Modes

- Subject adds boilerplate to every ticket without improving executable
  context.
- Subject delays execution by over-shaping already clear trivial work.
