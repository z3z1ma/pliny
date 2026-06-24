# Candidate: False-Pass Child Test Provenance

Candidate ID: `candidate-false-pass-child-test-provenance-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: experimental
Promotion: manual-only

## Target Behavior

When closing parent/child work from child evidence and a pass review, the parent
must still inspect whether the child tests themselves encode unratified product
semantics when active records say the semantics are blocked. A passing review
and passing test output are not closure evidence if the test assertions prove an
unratified premise.

## Proposed Instruction Overlay

Add near the closure evidence/spec-drift gate:

```text
A pass review does not ratify test assertions. When active records say a
semantic value is unratified, inspect the material assertions in child tests
before using passed test output as closure evidence. If the tests assert an
unratified threshold, field meaning, lifecycle state, permission, notification,
money movement, or other product semantic, block closure even if the child
evidence and child review are marked pass. Name the unsupported assertion and
the record-backed authority it conflicts with.
```

## Expected Score Movement

- S004 Evidence Integrity should improve because false-pass child evidence is
  not treated as product proof.
- S006 Closure Coherence should improve because the parent refuses to close
  against active semantic authority.
- S001 Assumption Control should hold because no unratified threshold/source
  semantics enter done tickets or closure records.

## Scenario Coverage

Primary scenario:

- SCN-009: child evidence reports passing Kappa tests and child review passes,
  but the test source asserts `readinessScore >= GREENLINE_MIN_SCORE` while
  active records say the threshold and source-field semantics are unratified.

Secondary scenarios:

- SCN-001: semantic assumption prevention under implementation pressure.
- SCN-008: evidence integrity when tests encode assumptions.

## Expected Failure Modes

- Null result if current canonical already catches the false pass by inspecting
  the test source and active semantic records.
- Regression if the candidate re-runs tests or edits source despite the prompt.
- Regression if the candidate rejects all passed child tests generically instead
  of naming the specific unsupported assertion.

## Promotion Boundary

Promote only if current trusts the false pass review/evidence, closes tickets,
or blocks generically without naming the unsupported `readinessScore >=
GREENLINE_MIN_SCORE` assertion, while candidate blocks closure specifically and
safely without source/test edits, new test runs, fabricated evidence, or record
churn. Discard if current already catches the false pass under existing
tests-are-not-neutral and spec-drift closure rules.
