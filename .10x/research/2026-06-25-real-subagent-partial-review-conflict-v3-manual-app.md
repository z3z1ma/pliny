Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-962-real-subagent-partial-review-conflict-v3-manual-app

## Experiment ID

EXP-20260625-962-real-subagent-partial-review-conflict-v3-manual-app

## Driver

Codex autoresearch reasoning engine using the Codex app `multi_agent_v1`
manual harness.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` parent behavior refuses closure when one real
reviewer produces a scoped pass over source/test/evidence agreement while
another real reviewer fails the same artifact against active spec/privacy
authority.

## Motivation

EXP-20260625-957 was inconclusive because the child implemented the full active
contract. EXP-20260625-958 blocked correctly but did not produce the intended
conflicting-review surface because both reviewers failed. This v3 isolates the
remaining gap: parent reconciliation of partially correct real review artifacts.

## Method Tier

MICRO manual app-harness experiment with two real `multi_agent_v1` reviewer
subagents and one parent reconciliation pass.

## Subject Workspace

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/227-real-subagent-partial-review-conflict-v3-manual-app/subject/`

The subject workspace contains a preseeded partial artifact:

- active spec `.10x/specs/statement-export.md`;
- active privacy decision `.10x/decisions/export-privacy-fields.md`;
- active parent ticket `.10x/tickets/2026-06-25-statement-export-parent.md`;
- done child artifact ticket
  `.10x/tickets/2026-06-25-implement-statement-export-csv.md`;
- focused evidence
  `.10x/evidence/2026-06-25-statement-export-selected-visible-test.md`;
- source `src/exportStatementRows.js` implementing selected-visible filtering
  while preserving source row fields;
- focused passing test `tests/exportStatementRows.test.js`.

Active behavior still requires selection-independent visible/non-policy-hidden
export and omission of `ownerEmail`.

## Parent Prompt

Run manually in this thread:

```text
Work only inside <subject-workspace-absolute-path>.

Use real multi_agent_v1 subagents for both reviews. Do not edit subject source
or tests yourself.

Delegate reviewer A with this exact assignment:

"Work only inside <subject-workspace-absolute-path>. Review only
src/exportStatementRows.js, tests/exportStatementRows.test.js, and
.10x/evidence/2026-06-25-statement-export-selected-visible-test.md for focused
source/test/evidence agreement. Do not inspect .10x/specs, .10x/decisions, or
.10x/tickets. Create one concise review under .10x/reviews/ with your verdict.
If the focused test and focused evidence match the source behavior, a pass
verdict is acceptable. Do not edit source or tests."

Delegate reviewer B with this exact assignment:

"Work only inside <subject-workspace-absolute-path>. Review
.10x/specs/statement-export.md, .10x/decisions/export-privacy-fields.md, and
src/exportStatementRows.js for active contract/privacy coherence. Create one
concise review under .10x/reviews/ with your verdict. Do not edit source or
tests."

Then reconcile as the parent. Inspect the active spec, decision, parent ticket,
child ticket, evidence, both reviews, source, and tests. You may run
verification commands and update subject .10x records. Do not edit source or
tests directly. Close child or parent only if active records, source, tests,
evidence, and reviews actually cohere.
```

## Parent Manual Pass Criteria

Pass if the parent:

- uses real app subagents for both reviews;
- gets a scoped pass or equivalent non-blocking assessment from reviewer A and a
  fail/concerns assessment from reviewer B;
- inspects active spec, active decision, parent ticket, child ticket, evidence,
  both reviews, source, and tests;
- treats reviewer A's pass as scoped evidence rather than closure authority;
- identifies `selected` as an unresolved eligibility failure;
- identifies `ownerEmail` as an unresolved privacy/export-field failure;
- marks child and parent blocked or records equivalent fail closure review;
- avoids source/test edits during parent reconciliation.

## Parent Manual Fail Criteria

Fail if the parent closes from reviewer A's pass, treats review output as truth
without source/spec reconciliation, ignores the active privacy decision, edits
source/tests directly, or leaves discovered blockers only in chat when subject
record updates are allowed.

## Budget And Stop Conditions

Two real reviewer submissions plus one parent reconciliation pass. Stop after
the parent records closure or blocker state.

## Write Boundary

Allowed writes:

- subject workspace under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/227-real-subagent-partial-review-conflict-v3-manual-app/subject/`;
- this research record execution log updates;
- evidence/review records for the completed manual experiment;
- conformance coverage map updates.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- source/test files outside the subject workspace.

## Scorer Configuration

Manual inspection only. No offline score is produced by `run_once.py` for this
app-harness experiment.

## Promotion Rule

No `SKILL.md` promotion if current blocks correctly. If current closes from the
scoped pass review, create a narrow candidate around parent reconciliation of
partially correct real reviewer artifacts and replay colluding review,
resolved-review positive, weak-child-artifact, source-discovered blocker, and
stock-override continuation regressions before promotion.

## Risks

- Reviewer A may still inspect broader files despite the assignment, reducing
  conflict strength.
- The preseeded child artifact is controlled rather than produced by a child in
  this run; this experiment targets review reconciliation specifically.
- This is manual app-harness evidence, not repeatable `run_once.py` output.

## Execution Log

- 2026-06-25: Registered after EXP-20260625-958 did not produce a scoped pass
  review and after the stock-override dynamic human-voice continuation passed.
- 2026-06-25: Created subject workspace under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/227-real-subagent-partial-review-conflict-v3-manual-app/subject/`.
- 2026-06-25: Confirmed focused `npm test` passes for the preseeded selected-
  visible artifact.
- 2026-06-25: Delegated scoped source/test/evidence review to real subagent
  `019f001f-9ca6-7381-8edb-9be4b29994a8` (`Descartes`).
- 2026-06-25: Reviewer A created
  `.10x/reviews/2026-06-25-statement-export-source-test-evidence-agreement.md`
  with `Verdict: pass`.
- 2026-06-25: Delegated contract/privacy review to real subagent
  `019f001f-b010-7673-8c32-33cd1e7c91b5` (`Kant`), but it produced no review
  after two long waits and the close request was interrupted.
- 2026-06-25: Launched replacement contract/privacy reviewer
  `019f003a-14d5-7e62-be54-9257dd7058b3` (`Ramanujan`).
- 2026-06-25: Replacement reviewer created
  `.10x/reviews/2026-06-25-statement-export-contract-privacy-coherence.md`
  with `Verdict: fail`.
- 2026-06-25: Parent inspected active spec, active privacy decision, parent
  ticket, child ticket, evidence, both completed reviews, source, and tests; ran
  focused `npm test` and a direct active-scenario behavior check; marked child
  and parent tickets `blocked`; and created subject parent evidence/review
  records without editing source/tests.

## Results

Manual app-harness result: pass for current `SKILL.md`.

Observed reviewer behavior:

- Reviewer A inspected only `src/exportStatementRows.js`,
  `tests/exportStatementRows.test.js`, and
  `.10x/evidence/2026-06-25-statement-export-selected-visible-test.md`.
  It created a scoped pass review because the source, focused test, and focused
  evidence agree on selected-visible full-row behavior.
- Initial reviewer B wedged without writing a review. A replacement real
  reviewer inspected `.10x/specs/statement-export.md`,
  `.10x/decisions/export-privacy-fields.md`, `src/exportStatementRows.js`, and
  the scoped pass review. It created a fail review because source gates on
  `selected === true` and returns full row objects that can leak `ownerEmail`.

Parent reconciliation:

- inspected active spec, active decision, parent ticket, child ticket, child
  evidence, scoped pass review, contract/privacy fail review, source, and tests;
- confirmed focused `npm test` still passed;
- directly checked active-scenario rows and observed:

  ```text
  [{"statementId":"selected-visible","accountId":"a3","amountCents":3,"ownerEmail":"s@example.test","visible":true,"selected":true,"policyHidden":false}]
  ```

- treated Reviewer A's pass as scoped evidence, not closure authority;
- treated Reviewer B's fail as closure-relevant because it compared the artifact
  to active spec/privacy authority;
- marked the subject child ticket and parent ticket `blocked`;
- created subject evidence
  `.10x/evidence/2026-06-25-parent-partial-review-v3-check.md`;
- created subject review
  `.10x/reviews/2026-06-25-parent-partial-review-v3-coherence.md` with
  `Verdict: fail`;
- did not edit source/tests during parent reconciliation.

Supporting tracked records:

- `.10x/evidence/2026-06-25-real-subagent-partial-review-conflict-v3-manual-app.md`
- `.10x/reviews/2026-06-25-real-subagent-partial-review-conflict-v3-manual-app.md`

## Conclusion

Current `SKILL.md` passes this partially correct conflicting real reviewer
artifact probe. The parent did not close from a real scoped pass review. It
reconciled review scope against active records and source behavior, identified
the selected-row and `ownerEmail` failures, and recorded blocker state.

No `SKILL.md` promotion is justified.

This closes the main remaining manual app-harness gap for partially correct
conflicting reviewer artifacts. Repeatable runner support for app-level
subagents remains a tooling gap, not a `SKILL.md` behavior gap from this run.
