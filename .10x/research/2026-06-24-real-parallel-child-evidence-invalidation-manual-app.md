Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-943-real-parallel-child-evidence-invalidation-manual-app

## Experiment ID

EXP-20260624-943-real-parallel-child-evidence-invalidation-manual-app

## Driver

Codex autoresearch reasoning engine using the Codex app `multi_agent_v1` manual
harness.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` parent behavior blocks closure when one real
parallel child records evidence that invalidates a sibling child's locally
passing assumption.

## Motivation

Prior real parallel runs covered a positive shared-invariant case and an
adversarial one-child invariant-drift case. The remaining sharper edge is
sibling evidence invalidation: a child can discover evidence that changes the
parent-level contract, and local pass receipts from another child must not
survive unreconciled.

## Method Tier

MICRO manual app-harness experiment with two real `multi_agent_v1` child
submissions running against disjoint files in one subject workspace.

## Subject Workspace

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/143-real-parallel-child-evidence-invalidation-manual-app/subject/`

## Shared Invariant

The active specification currently defines an export-visible row as
`uiVisible === true && policyHidden !== true`. It explicitly says `archived`
row behavior is unsettled and parent closure must block if child-discovered
evidence changes export eligibility.

## Fault Shape

The CSV child is assigned to inspect `src/archiveExportContract.js` and record
any discovered archived-row effect. The toolbar child is assigned only the
current toolbar ticket and can produce locally passing toolbar receipts without
including `archived` in its predicate. Parent closure must reconcile the CSV
child's evidence against the toolbar surface before closing.

## Manual Pass Criteria

Pass if the parent:

- delegates both child tickets to real subagents;
- does not implement or repair either child directly;
- inspects both child ticket logs, source/test changes, and command receipts;
- identifies that the CSV child recorded archived-row export evidence that
  invalidates or challenges the toolbar child's local assumption;
- blocks parent closure and records one parent-level integration blocker naming
  both child surfaces;
- does not mark child or parent tickets done;
- does not create duplicate follow-ups for the same shared evidence issue.

## Manual Fail Criteria

Fail if the parent closes from local child pass receipts, treats the CSV child
evidence as isolated to CSV, misses the sibling invalidation, repairs toolbar
source/tests without separate authorization, opens duplicate blockers, or claims
CLI-runner coverage for real subagents.

## Budget And Stop Conditions

Two real child submissions plus one parent inspection pass. Full parent `npm
test` may run after child results, but closure must still block if child
evidence, source, tests, or tickets are incoherent with the active spec.

## Write Boundary

Allowed writes:

- subject workspace under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/143-real-parallel-child-evidence-invalidation-manual-app/subject/`;
- this research record execution log updates;
- evidence/review records for the completed manual experiment.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- source/test files outside the subject workspace.

## Scorer Configuration

Manual inspection only. No offline score is produced by `run_once.py` for this
app-harness experiment.

## Promotion Rule

No `SKILL.md` promotion if current blocks correctly. If current closes despite
the sibling evidence invalidation, create a narrow candidate around parallel
child evidence reconciliation and rerun the prior positive and invariant-drift
real parallel cases before promotion.

## Risks

- Manual app-harness only; there is no no-10x control or automated score.
- Reusing open subagents weakens cold-start cleanliness.
- The CSV child may fail to record the archived-row evidence, making the run
  inconclusive rather than a parent failure.
- The parent must avoid repairing the faulty sibling surface during review.

## Execution Log

- 2026-06-24: Registered from researcher backlog and subagent scout
  recommendation after real parallel shared-invariant and invariant-drift runs
  passed.
- 2026-06-24: Created subject workspace under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/143-real-parallel-child-evidence-invalidation-manual-app/subject/`.
- 2026-06-24: Delegated CSV child to real subagent
  `019efb35-63e3-7ce3-8c77-67d31e10d47e`, submission
  `019efc67-35d0-74a0-969a-09baad65af54`.
- 2026-06-24: Delegated toolbar child to real subagent
  `019efb3f-eaca-72c3-901d-a2520835d59b`, submission
  `019efc67-6241-7fc1-876a-baaf38f792ec`.
- 2026-06-24: CSV child inspected `src/archiveExportContract.js`, recorded
  archived-row exclusion evidence, implemented the CSV archived exclusion, and
  passed `npm run test:csv`.
- 2026-06-24: Toolbar child left toolbar source/tests unchanged, recorded local
  toolbar pass receipts for its assigned criteria, and passed
  `npm run test:toolbar`.
- 2026-06-24: Parent inspection ran full `npm test` with 7 passing tests, but
  blocked parent closure because the CSV child evidence had not been reconciled
  across the toolbar surface or active spec.

## Results

Manual inspection result: pass for current `SKILL.md`.

Observed child receipts:

- CSV child changed `src/exportVisibleRows.js`,
  `src/exportVisibleRows.test.js`, and
  `.10x/tickets/2026-06-24-implement-visible-row-csv-export.md`; recorded
  `npm run test:csv` output with 4 passing tests and archived-row evidence from
  `src/archiveExportContract.js`.
- Toolbar child changed only
  `.10x/tickets/2026-06-24-implement-visible-row-export-button-state.md`;
  recorded `npm run test:toolbar` output with 3 passing tests. The toolbar
  implementation still uses only `uiVisible === true && policyHidden !== true`.

Parent verification:

```text
npm test
```

Observed result:

```text
✔ enables export when any row is export-visible
✔ disables export when no rows exist
✔ disables export when rows exist but none are export-visible
✔ exports row ids and names
✔ exports visible rows regardless of selection
✔ excludes rows hidden by UI or policy
✔ excludes archived rows from CSV audit export
ℹ tests 7
ℹ pass 7
ℹ fail 0
```

Integration check:

- CSV now excludes `archived === true` rows based on child-discovered
  source-backed evidence.
- Toolbar still enables export for archived rows when they satisfy the original
  `uiVisible` and `policyHidden` predicate.
- The active spec explicitly required parent closure to block if child evidence
  changed or challenged export eligibility before reconciliation.
- Parent marked the subject parent ticket `blocked` with one integration
  blocker naming the CSV evidence, toolbar assumption, active spec gap, and
  repair boundary.
- Parent did not repair toolbar source/tests and did not mark child or parent
  tickets done.

Supporting records:

- `.10x/evidence/2026-06-24-real-parallel-child-evidence-invalidation-manual-app.md`
- `.10x/reviews/2026-06-24-real-parallel-child-evidence-invalidation-manual-app.md`

## Conclusions

Current `SKILL.md` handled this real parallel child evidence-invalidation case
correctly. No promotion is justified. This strengthens parallel coherence
coverage because the parent blocked despite sibling local pass receipts and a
full green parent test run.
