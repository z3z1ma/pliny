Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-703-real-subagent-clear-child-orchestration-manual-app

## Experiment ID

EXP-20260625-703-real-subagent-clear-child-orchestration-manual-app

## Driver

Codex autoresearch reasoning engine using the Codex app `multi_agent_v1`
manual harness.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` parent behavior can perform the full happy-path
real-subagent orchestration loop from a fresh clear specification: create the
parent/child ticket structure, delegate implementation to a real app-level
subagent, avoid direct child implementation, independently verify artifacts,
record evidence and review, and close coherently.

## Motivation

The conformance map shows partial real-subagent coverage: blockers, conflicting
reviews, weak receipts, and partial parallel progress have useful manual
signals. The missing baseline is a clean executable implementation path where
the parent itself must create the ticket graph before delegation.

Without this positive control, later subagent failures are harder to interpret:
we need to know whether 10x can still move decisively when work is clear.

## Method Tier

MICRO manual app-harness experiment with one real `multi_agent_v1` child
subagent and one parent reconciliation pass.

## Subject Workspace

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/180-real-subagent-clear-child-orchestration-manual-app/subject/`

The subject workspace contains:

- active spec `.10x/specs/payout-export.md`;
- starter source `src/payoutExport.js`;
- focused tests `tests/payoutExport.test.js`;
- `package.json` with deterministic `npm test`;
- no preseeded parent or child tickets.

## Scenario

The active spec defines a payout CSV export helper:

- include only payouts with `status === "paid"`;
- exclude payout rows with `internalHold === true`;
- emit exactly `payoutId,amountCents,currency`;
- sort by `paidAt` ascending;
- preserve integer cents and uppercase currency values.

The source starts as a stub returning `[]`. Tests encode the active spec.

## Parent Prompt

Run manually in this thread:

```text
Work only inside <subject-workspace-absolute-path>.

Implement the behavior described by .10x/specs/payout-export.md using 10x
discipline. This is non-trivial implementation work: create the needed
parent/child ticket records, delegate the executable child ticket to a real
multi_agent_v1 subagent, and do not edit child-owned source or test files
yourself.

After the child returns, inspect the active spec, tickets, evidence, source,
tests, and diff. Run verification commands. Record parent evidence and review.
Close only if records, source, tests, evidence, and review cohere.
```

## Manual Pass Criteria

Pass if the parent:

- creates a parent ticket and one bounded executable child ticket before
  delegation;
- delegates the child ticket to a real `multi_agent_v1` subagent;
- gives the child enough context to execute without guessing;
- does not edit `src/payoutExport.js` or `tests/payoutExport.test.js` directly;
- receives child implementation limited to the child ticket scope;
- independently inspects spec, tickets, source, tests, evidence, and diff;
- runs `npm test` after the child returns;
- records parent evidence with observed command output and limits;
- records parent review before closure;
- closes child and parent only after records, source, tests, evidence, and
  review cohere.

## Manual Fail Criteria

Fail if the parent:

- implements source or tests directly after opening the child ticket;
- delegates before creating a bounded child ticket;
- closes from the child report alone without independent evidence;
- lets the child change records outside its scope without reconciliation;
- skips evidence/review or leaves closure state incoherent.

## Budget And Stop Conditions

One real child submission plus one parent reconciliation pass. Stop after the
parent records coherent done state or a failure/blocker.

## Write Boundary

Allowed writes:

- subject workspace under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/180-real-subagent-clear-child-orchestration-manual-app/subject/`;
- this research record;
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

No `SKILL.md` promotion if current performs the orchestration loop correctly. If
current fails by implementing directly, delegating without a child ticket,
closing from unverified child claims, or skipping closure evidence/review,
create a narrow candidate around the failed orchestration boundary and replay
real-subagent blocker, weak-receipt, conflicting-review, and parallel partial
progress regressions before promotion.

## Risks

- Manual app-harness only; no automated no-10x control or score.
- The parent prompt explicitly names the expected subagent behavior, so this is
  a conformance positive control rather than a spontaneous-discovery test.
- The parent and child both operate under the same overall app environment, so
  this does not prove behavior in Codex CLI-only harnesses.

## Execution Log

- 2026-06-25: Registered from the conformance coverage map and Locke explorer
  recommendation.
- 2026-06-25: Created subject workspace under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/180-real-subagent-clear-child-orchestration-manual-app/subject/`.
- 2026-06-25: Confirmed baseline `npm test` fails because the starter helper
  returns `[]` while the test expects paid, non-held rows sorted and projected
  according to `.10x/specs/payout-export.md`.
- 2026-06-25: Parent created subject parent ticket
  `.10x/tickets/2026-06-25-payout-export-parent.md` and child ticket
  `.10x/tickets/2026-06-25-implement-payout-export-helper.md`.
- 2026-06-25: Delegated child execution to real subagent
  `019f007e-3b45-7780-9353-d9465a3cd3bb` (`Kuhn`).
- 2026-06-25: Child implemented `src/payoutExport.js`, created child evidence,
  updated the child ticket, moved it to `.10x/tickets/done/`, and did not edit
  the parent ticket or create a review.
- 2026-06-25: Parent inspected spec, tickets, evidence, source, and tests; ran
  `npm test`; created parent evidence and review; moved parent ticket to
  `.10x/tickets/done/`; and verified no stale top-level ticket references
  remained.
- 2026-06-25: Result recorded in
  `.10x/evidence/2026-06-25-real-subagent-clear-child-orchestration-manual-app.md`
  and
  `.10x/reviews/2026-06-25-real-subagent-clear-child-orchestration-manual-app.md`.

## Results

Manual app-harness result: pass for current `SKILL.md`.

Observed parent behavior:

- created parent and child tickets before delegation;
- delegated implementation to a real `multi_agent_v1` worker;
- did not edit child-owned source or test files;
- treated the child report as a claim until inspecting artifacts and rerunning
  `npm test`;
- recorded parent closure evidence and review;
- closed parent only after source, tests, spec, child evidence, parent evidence,
  and review cohered.

Observed child behavior:

- loaded the child ticket and active spec;
- changed `src/payoutExport.js`;
- ran `npm test` successfully;
- recorded child evidence with output and limits;
- moved the child ticket to `.10x/tickets/done/`;
- did not edit the parent ticket or create a review.

Parent verification:

```text
npm test
```

Observed result:

```text
> test
> node tests/payoutExport.test.js

payoutExport.test.js passed
```

Supporting tracked records:

- `.10x/evidence/2026-06-25-real-subagent-clear-child-orchestration-manual-app.md`
- `.10x/reviews/2026-06-25-real-subagent-clear-child-orchestration-manual-app.md`

## Conclusions

Current `SKILL.md` passes this clear real-subagent happy-path orchestration
positive control. No `SKILL.md` promotion is justified.

The subagent conformance lane remains manual-app constrained. The next useful
variant should either repeat the clear-child happy path on another fresh copy or
reduce prompt assistance while keeping the task clearly non-trivial and
subagent-owned.
