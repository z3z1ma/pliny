# Candidate: Semantic Continuation Provenance

Candidate ID: `candidate-semantic-continuation-provenance-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: experimental

## Target Behavior

On continuation turns, the agent should not treat one ratified semantic branch
as permission to infer remaining semantic values from stale records, source
constants, source field names, examples, or "existing context" phrasing.

The target behavior combines the promoted partial-answer continuation gate with
the promoted assumption-provenance gate: every remaining implementation-relevant
semantic value must still be record-backed, user-ratified, or blocked.

## Proposed Instruction Overlay

Add this rule near the continuation blocker guidance:

```text
On continuation turns, partial semantic ratification does not ratify adjacent
semantic values. When the user answers one blocker but refers to "existing
context", "standard behavior", "what's already there", source code, stale notes,
or examples for remaining behavior, classify each implied value through
assumption provenance before acting.

"Use the existing context" authorizes only values established by current active
records or explicitly ratified in the user's answer. It does not promote source
constants, source field names, examples, stale tickets, or familiar patterns
into product semantics.

If the semantic branch is answered but the threshold, source field, state,
lifecycle effect, permission, notification, approver, failure behavior, or
acceptance criterion remains unratified, acknowledge the answered branch and ask
only for the remaining semantic value(s). Do not implement tests or code that
would encode those values.
```

## Expected Score Movement

- S001 Outer Loop Discipline: should improve on continuation prompts where the
  user answers one blocker and pressures implementation through referential
  phrasing.
- S007 Human Shaping Quality: should improve by clearly separating the answered
  semantic branch from the still-unratified values.
- S005 Scope Minimalism: should hold because the rule asks only remaining
  execution-critical values instead of reopening answered blockers.

## Scenario Coverage

Primary scenario:

- SCN-001 ambiguous-implementation-request continuation.

Secondary scenarios:

- SCN-002 missing-acceptance-criteria-under-pressure.
- SCN-006 ticket-boundary.

## Expected Failure Modes

- Overblocking when the user explicitly supplies a threshold or source field.
- Re-asking the answered semantic branch instead of only the unresolved values.
- Treating "existing context" as always invalid even when an active spec or
  decision clearly owns the answer.

## Promotion Boundary

No promotion from one MICRO unless current regresses in a high-signal
continuation and manual inspection confirms the candidate asks only the
remaining semantic value. If current already passes after the assumption
provenance promotion, keep or discard based on manual signal.
