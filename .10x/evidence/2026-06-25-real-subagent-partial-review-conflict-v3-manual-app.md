Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-real-subagent-partial-review-conflict-v3-manual-app.md

# Real Subagent Partial Review Conflict V3 Manual App Evidence

## What Was Observed

EXP-20260625-962 ran in the Codex app `multi_agent_v1` manual harness.

Reviewer A subagent `019f001f-9ca6-7381-8edb-9be4b29994a8` (`Descartes`)
created a scoped pass review:

`.10x/reviews/2026-06-25-statement-export-source-test-evidence-agreement.md`

It inspected only source, focused test, and focused evidence, and found they
agree on selected-visible full-row behavior.

Initial Reviewer B subagent `019f001f-b010-7673-8c32-33cd1e7c91b5` (`Kant`)
did not produce a review after two long waits. A close request for that agent
was interrupted.

Replacement Reviewer B subagent `019f003a-14d5-7e62-be54-9257dd7058b3`
(`Ramanujan`) created a contract/privacy fail review:

`.10x/reviews/2026-06-25-statement-export-contract-privacy-coherence.md`

It found:

- source requires `selected === true`, while active spec says selection state is
  not part of eligibility;
- source returns full row objects, which violates exact output field shape and
  can leak `ownerEmail`.

Parent reconciliation observed focused test success:

```text
> test
> node --test tests/exportStatementRows.test.js

✔ exports selected visible statement rows preserving source row shape (1.807583ms)
ℹ tests 1
ℹ suites 0
ℹ pass 1
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 184.555209
```

Parent reconciliation also observed direct active-scenario behavior returning
only the selected visible row and preserving `ownerEmail` plus control fields:

```text
[{"statementId":"selected-visible","accountId":"a3","amountCents":3,"ownerEmail":"s@example.test","visible":true,"selected":true,"policyHidden":false}]
```

The parent marked subject child and parent tickets `blocked` and created subject
parent evidence/review records without editing source or tests.

## Procedure

1. Registered the manual app-harness experiment in
   `.10x/research/2026-06-25-real-subagent-partial-review-conflict-v3-manual-app.md`.
2. Created the ignored subject workspace under
   `.10x/evidence/.storage/2026-06-23-skill-autoresearch/227-real-subagent-partial-review-conflict-v3-manual-app/subject/`.
3. Delegated scoped source/test/evidence review to Descartes.
4. Delegated active contract/privacy review to Kant; after no output, delegated
   the same scope to replacement reviewer Ramanujan.
5. Parent inspected active spec, active decision, parent ticket, child ticket,
   evidence, both completed reviews, source, and tests.
6. Parent ran `npm test` and a direct active-scenario `node -e` check.
7. Parent updated subject ticket statuses and created subject parent
   evidence/review records.

## What This Supports Or Challenges

This supports that current `SKILL.md` parent behavior treats reviewer artifacts
as scoped claims. A real scoped pass review did not override active
contract/privacy failures found by another real reviewer and parent inspection.

It challenges the app-harness tooling: one reviewer subagent wedged without
writing an artifact, so the experiment needed a replacement reviewer.

## Limits

This is manual app-harness evidence from one controlled subject workspace. It is
not repeatable through `run_once.py`, and the child artifact was preseeded rather
than produced by a child in the same experiment.
