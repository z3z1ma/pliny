Status: active
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-934-real-parallel-child-shared-invariant-manual-app

## Experiment ID

EXP-20260624-934-real-parallel-child-shared-invariant-manual-app

## Driver

Codex autoresearch reasoning engine using the Codex app `multi_agent_v1` manual
harness.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can coordinate two real child tickets in parallel
without losing a shared specification invariant or letting child-local work
fragment parent-level coherence.

## Motivation

Prior app-harness experiments covered one real child at a time. The conformance
map still marks multi-agent parallel coherence as weak. This experiment tests
whether the parent can delegate two disjoint child tickets, verify both, and
reconcile the shared invariant before closure.

## Method Tier

MICRO manual app-harness experiment with two real `multi_agent_v1` child
submissions running against disjoint files in one subject workspace.

## Subject Workspace

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/134-real-parallel-child-shared-invariant-manual-app/subject/`

## Shared Invariant

An export-visible row is a row where `uiVisible === true` and
`policyHidden !== true`. `selected` is UI interaction state and must not control
CSV inclusion or export-button enabled state.

## Manual Pass Criteria

Pass if the parent:

- delegates both child tickets to real subagents;
- does not implement either child directly;
- keeps child write scopes disjoint;
- waits for both child results before closure;
- inspects both child ticket logs, source/test changes, and command receipts;
- runs parent full verification after both children return;
- verifies the shared invariant across both surfaces;
- closes only if both child tickets and the parent ticket are coherent.

## Manual Fail Criteria

Fail if the parent implements either child directly, closes from child summaries
alone, verifies only one child surface, misses a shared invariant drift, creates
duplicate follow-ups for one integration issue, or lets a child broaden scope.

## Budget And Stop Conditions

Two real child submissions plus one parent verification pass. Stop after parent
closure/blocker decision and manual inspection.

## Write Boundary

Allowed writes:

- subject workspace under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/134-real-parallel-child-shared-invariant-manual-app/subject/`;
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

No `SKILL.md` promotion if current passes. If current fails, create a narrow
candidate around the observed real parallel-coherence failure and rerun a
positive control with aligned children before promotion.

## Risks

- Reusing existing open subagents weakens cold-start cleanliness.
- Parallel writes in one subject workspace can create race noise, though child
  scopes are disjoint.
- Child agents may fail to update ticket progress or provide command receipts,
  turning the result into a weak-artifact case rather than a parallel-coherence
  case.

## Execution Log

- 2026-06-24: Registered from read-only subagent scout recommendation after
  weak-child-artifact coverage passed.
