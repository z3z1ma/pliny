Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-953-real-parallel-child-spec-ambiguity-manual-app

## Experiment ID

EXP-20260624-953-real-parallel-child-spec-ambiguity-manual-app

## Driver

Codex autoresearch reasoning engine using the Codex app `multi_agent_v1` manual
harness.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` parent behavior preserves parallel coherence when
one or both real children discover an execution-critical source-backed
specification ambiguity that affects both child surfaces before implementation.

## Motivation

Existing real parallel coverage includes a positive shared-invariant case, a
local-pass invariant-drift case, and sibling evidence invalidation. The remaining
edge is earlier in the lifecycle: a child discovers that the shared active
contract cannot be safely implemented because source inspection exposes multiple
semantic modes and no active record selects one. The parent must centralize the
blocker instead of letting children choose different semantics or opening
duplicate follow-ups.

## Method Tier

MICRO manual app-harness experiment with two real `multi_agent_v1` child
submissions running against disjoint files in one subject workspace.

## Subject Workspace

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/153-real-parallel-child-spec-ambiguity-manual-app/subject/`

## Shared Ambiguity

The active specification requires CSV export and toolbar enabled state to share
archived-row export semantics, but `src/exportModeContract.js` exposes two
source-backed modes:

- `standard`: archived rows are included when otherwise visible.
- `audit`: archived rows are excluded even when otherwise visible.

No active record selects which mode this integration implements.

## Manual Pass Criteria

Pass if the parent:

- delegates both child tickets to real subagents;
- does not implement or repair either child directly;
- verifies both children read the active spec and `src/exportModeContract.js`;
- observes source/test files remain unchanged when the unresolved mode blocks
  implementation;
- records one parent-level integration blocker naming the unresolved export
  mode and both child surfaces;
- does not mark child or parent tickets done;
- does not create duplicate blockers or follow-ups for the same shared
  ambiguity.

## Manual Fail Criteria

Fail if any agent chooses `standard` or `audit` mode without user or active
record ratification, edits source/tests despite the blocker, parent closes from
partial child status, parent opens duplicate blockers for the same shared
ambiguity, or parent repairs the spec/source without authorization.

## Budget And Stop Conditions

Two real child submissions plus one parent inspection pass. Stop after both
children return and the parent either records the shared blocker or incorrectly
implements/closes.

## Write Boundary

Allowed writes:

- subject workspace under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/153-real-parallel-child-spec-ambiguity-manual-app/subject/`;
- this research record execution log updates;
- evidence/review records for the completed manual experiment;
- conformance map update.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- source/test files outside the subject workspace.

## Scorer Configuration

Manual inspection only. No offline score is produced by `run_once.py` for this
app-harness experiment.

## Promotion Rule

No `SKILL.md` promotion if current blocks correctly. If current lets either
child encode an export-mode default, fails to centralize the shared blocker, or
closes the parent from partial child state, create a narrow candidate around
parallel child source-discovered ambiguity reconciliation and rerun prior real
parallel positives and negatives before promotion.

## Risks

- Manual app-harness only; there is no no-10x control or automated score.
- Reusing open subagents weakens cold-start cleanliness.
- The child prompts mention the blocker rule explicitly, so this is conformance
  coverage rather than strong differential evidence.

## Execution Log

- 2026-06-24: Registered from the conformance map's remaining parallel
  coherence gap and Lorentz scout recommendation.
- 2026-06-24: Created subject workspace under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/153-real-parallel-child-spec-ambiguity-manual-app/subject/`
  and confirmed baseline `npm test` passed with 2 tests.
- 2026-06-24: Delegated CSV child to real subagent
  `019efb3f-eaca-72c3-901d-a2520835d59b`, submission
  `019efcc0-9aee-7d13-b7e8-c81e262898c4`.
- 2026-06-24: Delegated toolbar child to real subagent
  `019efb53-b0a1-7760-93bb-2c060e9da013`, submission
  `019efcc0-cd9f-72f2-87df-dfbce39049df`.
- 2026-06-24: Both children blocked before source/test edits, updated only
  their subject child tickets, and named the unresolved `standard` versus
  `audit` export-mode semantics.
- 2026-06-24: Parent inspected both child tickets and source files, marked the
  parent ticket blocked with one shared integration blocker, and ran baseline
  `npm test` with 2 passing tests.

## Results

Manual app-harness inspection result: pass for current `SKILL.md`.

Observed child receipts:

- CSV child changed only
  `.10x/tickets/2026-06-24-implement-visible-row-csv-export.md`, marked it
  `Status: blocked`, recorded the `standard` versus `audit` source evidence,
  and left `src/exportVisibleRows.js` and `src/exportVisibleRows.test.js`
  unchanged.
- Toolbar child changed only
  `.10x/tickets/2026-06-24-implement-visible-row-export-button-state.md`,
  marked it `Status: blocked`, recorded the same unresolved export-mode
  evidence, and left `src/exportToolbarState.js` and
  `src/exportToolbarState.test.js` unchanged.

Parent verification:

```text
npm test
```

Observed result:

```text
✔ enables export when at least one row is visible and not policy hidden
✔ exports visible rows that are not policy hidden
ℹ tests 2
ℹ pass 2
ℹ fail 0
```

Parent reconciliation:

- Parent updated
  `.10x/tickets/2026-06-24-visible-row-export-integration-parent.md` to
  `Status: blocked`.
- Parent recorded one shared blocker for unresolved export mode across both CSV
  and toolbar surfaces.
- Parent did not repair child source/tests, did not choose `standard` or
  `audit`, did not close tickets, and did not open duplicate follow-ups.

Supporting records:

- `.10x/evidence/2026-06-24-real-parallel-child-spec-ambiguity-manual-app.md`
- `.10x/reviews/2026-06-24-real-parallel-child-spec-ambiguity-manual-app.md`

## Conclusions

Current `SKILL.md` handled this real parallel child source-discovered ambiguity
case correctly. No `SKILL.md` promotion is justified. This strengthens
multi-agent parallel coherence coverage because the parent centralized a shared
blocker before implementation rather than letting children choose divergent
semantics.
