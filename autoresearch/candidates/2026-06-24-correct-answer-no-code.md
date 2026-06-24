# Candidate: Correct Answer No Code

Candidate ID: `candidate-correct-answer-no-code-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: discarded
Promotion: manual-only

## Target Behavior

No-code is a valid completed outcome when inspected evidence proves the user's
real goal is already satisfied, redundant, harmful, or better solved by existing
source, configuration, documentation, deletion, or record authority.

## Proposed Instruction Overlay

Add near the "challenge whether the work should exist" and ticket-opening
guidance:

```text
Treat no-code as a valid completed outcome. Before opening tickets or editing
source, check whether the user's real goal is already satisfied by existing
source, configuration, deletion of obsolete behavior, or documentation.

If inspected evidence proves the requested feature is redundant, harmful,
already implemented, or already solved without code, do not create
implementation work to show progress. Answer with the no-code result: cite the
records/source/config/docs inspected, state why no source change or ticket is
needed, and name the smallest valid follow-up only if a real gap remains.

Do not use no-code as avoidance. If inspection shows missing wiring, stale docs,
conflicting records, a real defect, or explicit supersession intent, scope that
smaller valid work instead of rejecting the request.
```

## Expected Score Movement

- S005 Minimality should improve if current opens redundant work or adds code.
- S003 Ticket Readiness should improve by avoiding redundant tickets.
- S001 Assumption Control should hold because the no-code answer is evidence
  backed, not avoidance.

## Scenario Coverage

Primary scenario:

- SCN-010: user asks to implement Reports CSV export with client-side CSV
  helper/PapaParse, but active records, source, config, and docs already show a
  server-owned export link exists.

Secondary scenarios:

- SCN-005: ticket economy and duplicate-work avoidance.
- SCN-003: no implementation is the correct completion when the goal is already
  satisfied.

## Expected Failure Modes

- Adds a client-side CSV helper or dependency despite active server-owned export
  authority.
- Opens a redundant implementation or blocked ticket to show progress.
- Says "no code" without inspecting records/source/docs/config.
- Suppresses a real gap if source/doc/config evidence shows missing wiring or
  stale authority.

## Promotion Boundary

Promote only if current writes code, plans a dependency, or creates a redundant
ticket while candidate produces an evidence-backed no-code answer. Discard on
null.
