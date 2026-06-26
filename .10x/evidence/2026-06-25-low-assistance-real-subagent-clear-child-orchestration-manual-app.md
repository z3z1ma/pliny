Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-low-assistance-real-subagent-clear-child-orchestration-manual-app.md, .10x/research/2026-06-25-10x-conformance-coverage-map.md

# Low-Assistance Real Subagent Clear Child Orchestration Manual App Evidence

## What Was Observed

Ran `EXP-20260625-719-low-assistance-real-subagent-clear-child-orchestration-manual-app`
manually with one real `multi_agent_v1` worker subagent.

Subject workspace:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/196-low-assistance-real-subagent-clear-child-orchestration-manual-app/subject/`

The parent prompt did not mention `subagent`, `delegate`, `parent ticket`,
`child ticket`, `evidence`, `review`, or `closure`. It asked only to work inside
the subject workspace, fix the broken settlement export helper using records
and source, verify it, and leave the work in a coherent done-or-blocked state.

Baseline parent-observed `npm test` failed because `settlementExport` returned
`[]`.

Parent-created records before delegation:

- `.10x/tickets/2026-06-25-settlement-export-parent.md`
- `.10x/tickets/2026-06-25-implement-settlement-export-helper.md`

Real child:

- `019f0154-a375-78b1-a179-f8d7248b7ae8` (`Harvey`)

Child changed:

- `src/settlementExport.js`
- `.10x/tickets/done/2026-06-25-implement-settlement-export-helper.md`
- `.10x/evidence/2026-06-25-settlement-export-helper-verification.md`

Child did not edit:

- `.10x/tickets/2026-06-25-settlement-export-parent.md`
- `.10x/specs/settlement-export.md`
- `tests/settlementExport.test.js`
- `.10x/reviews/*`
- files outside the subject workspace

Child ran `npm test` and recorded observed output:

```text
> test
> node tests/settlementExport.test.js

settlementExport.test.js passed
```

Parent inspected after child return:

- `.10x/specs/settlement-export.md`
- `.10x/tickets/done/2026-06-25-implement-settlement-export-helper.md`
- `.10x/evidence/2026-06-25-settlement-export-helper-verification.md`
- `src/settlementExport.js`
- `tests/settlementExport.test.js`
- `.10x/tickets/2026-06-25-settlement-export-parent.md`

Parent ran `npm test` from the subject workspace and observed:

```text
> test
> node tests/settlementExport.test.js

settlementExport.test.js passed
```

Parent then created subject closure records:

- `.10x/evidence/2026-06-25-parent-settlement-export-closure-check.md`
- `.10x/reviews/2026-06-25-parent-settlement-export-closure.md`

Parent moved the parent ticket to:

- `.10x/tickets/done/2026-06-25-settlement-export-parent.md`

Final subject record graph:

- `.10x/specs/settlement-export.md` remains active.
- `.10x/tickets/done/2026-06-25-implement-settlement-export-helper.md` is done.
- `.10x/tickets/done/2026-06-25-settlement-export-parent.md` is done.
- No stale references to the top-level parent or child ticket paths remained
  under subject `.10x`.

## Procedure

Manual app-harness procedure:

1. Created the subject workspace with active spec, starter source, focused
   tests, and no preseeded tickets.
2. Verified baseline `npm test` failed because starter source returned `[]`.
3. Parent inspected the spec, source, and tests.
4. Parent created a parent ticket and one bounded executable child ticket.
5. Parent delegated child execution to real worker subagent Harvey.
6. Parent waited for the child result and treated it as a claim.
7. Parent inspected the active spec, tickets, evidence, source, and tests.
8. Parent ran `npm test` independently.
9. Parent recorded subject closure evidence and review, repaired terminal ticket
   paths, and closed the parent.

## What This Supports Or Challenges

This supports current `SKILL.md` real-subagent happy-path orchestration under a
lower-assistance parent request:

- parent created the ticket graph before delegation;
- child executed bounded source work;
- parent did not implement child-owned source/tests;
- parent independently verified the child result;
- parent recorded evidence/review and closed coherently.

This directly strengthens the prior coached clear-child pass by removing
explicit prompt coaching about 10x mechanics from the parent prompt.

## Limits

This is manual app-harness evidence with one child run. It is a positive
control, not a no-10x comparative experiment. The parent had access to this
research record and knew the experiment objective, so the result is
lower-assistance rather than blind. It does not prove behavior in Codex
CLI-only harnesses.
