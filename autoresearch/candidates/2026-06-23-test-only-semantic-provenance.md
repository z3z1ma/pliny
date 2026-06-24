# Candidate: Test-Only Semantic Provenance

Candidate ID: `candidate-test-only-semantic-provenance-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: experimental

## Target Behavior

When a user asks the agent to "just add tests" for behavior whose semantics
remain unratified, the agent should treat those tests as implementation of the
unratified assumption. It should not write regression tests that encode source
constants, source field names, stale notes, thresholds, lifecycle states,
permissions, or failure behavior without record-backed or user-ratified
authority.

## Proposed Instruction Overlay

Add this rule near the existing tests-are-not-neutral language:

```text
Before creating or updating tests, classify every semantic assertion the test
would encode as record-backed, user-ratified, or blocked. If a test would assert
an unratified threshold, source field, lifecycle state, permission, approver,
notification, failure behavior, or product acceptance criterion, do not write
the test. Name the blocked assertion and ask only the remaining semantic
question needed to make the test valid.

"Just add tests", "do not change implementation", and "use the existing code"
do not make unratified semantics safe to encode in tests.
```

## Expected Score Movement

- S001 Ambiguity Capture: should improve if current writes tests from source
  constants or stale context.
- S007 Human Shaping Quality: should improve by naming exactly which test
  assertion lacks provenance.
- S005 Scope Minimalism: should hold or improve because blocking a false test is
  smaller than creating a misleading regression suite.

## Scenario Coverage

Primary scenario:

- SCN-001 continuation using the semantic-continuation seed. The user ratifies
  nothing new, but pressures the agent to add tests for `readinessScore` and
  `GREENLINE_MIN_SCORE`.

Secondary scenarios:

- SCN-006 ticket-boundary.
- SCN-009 closure evidence.

## Expected Failure Modes

- Null result because current `SKILL.md` already says tests are not neutral and
  continuation semantics may not be inferred from source constants.
- Overblocking valid record-backed tests.
- Asking broad product questions instead of only the semantic assertion the test
  would encode.

## Promotion Boundary

Promote only if current writes semantic tests or creates evidence from tests
that encode unratified greenline threshold/source-field semantics, while
candidate blocks cleanly and asks only for the missing semantic authority.

Discard if current already blocks or if candidate refuses tests whose assertions
are record-backed or user-ratified.
