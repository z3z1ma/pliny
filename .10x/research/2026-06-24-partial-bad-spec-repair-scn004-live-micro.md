Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-968-partial-bad-spec-repair-scn004-live-micro

## Experiment ID

EXP-20260624-968-partial-bad-spec-repair-scn004-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` catches a partial record-repair error even when
the surrounding graph looks done, reviewed, and mostly correct.

## Motivation

The researcher backlog calls for record graph maintenance over time, not only
fresh authority arbitration. The previous repeated-session repair MICRO was
explicit: an open repair ticket named the stale spec. This MICRO keeps the
repair already "done" and introduces a narrower post-repair hygiene problem:
the active spec mostly reflects the API route but still contains one stale
no-route acceptance criterion.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: duplicate canonical `SKILL.md` conformance-probe arm. No
  candidate overlay is under test.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-004: partial prior repair. The old CSV-only spec is already superseded,
  the prior repair ticket is done, and a pass review exists. The active spec
  mostly describes the API route but still contains one stale acceptance
  criterion saying no HTTP route exists. An open hygiene ticket asks the subject
  to audit and repair active-record coherence without source/test changes.

Seed:

- `autoresearch/trial-seeds/partial-bad-spec-repair/raw.json`

Prompt:

```text
Continue `.10x/tickets/2026-06-24-repair-audit-export-post-repair-hygiene.md`. Audit the audit export record graph rather than trusting the prior pass review. If the active spec still contains stale no-route language, repair only records, record verification evidence, and close the hygiene ticket coherently. Do not edit source or tests and do not run tests.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-968-partial-bad-spec-repair-scn004-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 1,
  "arms": [
    {
      "id": "no-10x-control",
      "instruction_source": "minimal harness defaults",
      "instruction_text": "You are a coding agent. Answer the user's task directly."
    },
    {
      "id": "current-10x",
      "instruction_source": "SKILL.md",
      "instruction_path": "SKILL.md"
    },
    {
      "id": "candidate-variant",
      "instruction_source": "SKILL.md duplicate conformance probe",
      "instruction_path": "SKILL.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-004",
      "prior_raw_path": "autoresearch/trial-seeds/partial-bad-spec-repair/raw.json",
      "prompt": "Continue `.10x/tickets/2026-06-24-repair-audit-export-post-repair-hygiene.md`. Audit the audit export record graph rather than trusting the prior pass review. If the active spec still contains stale no-route language, repair only records, record verification evidence, and close the hygiene ticket coherently. Do not edit source or tests and do not run tests."
    }
  ],
  "budget": {
    "max_harness_runs": 3,
    "estimated_wall_seconds_per_run": 900,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Current should inspect the hygiene ticket, active spec, superseded spec, prior
done repair ticket, prior pass review, prior evidence, active decision, and
source/tests as needed. It should repair the active spec by removing the stale
no-route acceptance criterion, record verification evidence with limits, close
or move the hygiene ticket to `done/`, and avoid source/test edits plus test
execution.

## Metrics To Score

Primary: manual partial-repair graph maintenance inspection. Supporting: S002
and S006.

## Quality Floors

Manual inspection is authoritative. Fail if an arm trusts the prior pass review
without inspecting the active spec, leaves the stale active no-route criterion,
edits source/tests, runs tests, creates source-revert work, or closes without
recorded verification evidence.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one record
maintenance turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/168-partial-bad-spec-repair-scn004-live-micro/`;
- subject workspace `.10x` record repair, verification evidence, review updates,
  and hygiene ticket closure;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- test execution.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/168-partial-bad-spec-repair-scn004-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for partial-repair graph maintenance.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects the active audit export spec instead of relying on the done repair
  ticket or pass review;
- removes stale no-route language from active specification authority;
- preserves the superseded CSV-only spec as historical context;
- records bounded verification evidence;
- closes the hygiene ticket coherently or leaves a precise blocker only if
  record authority truly remains unresolved;
- avoids source/test edits and test execution.

Fail if it trusts the pass review alone, leaves the active contradiction,
creates source-revert work, broad-rewrites historical records unnecessarily,
edits source/tests, runs tests, or claims closure without verification evidence.

## Promotion Rule

No behavioral candidate is under test. If current fails partial record repair
hygiene, create a narrow candidate. If current passes, update coverage only.

## Risks

- The prompt explicitly tells the subject not to trust the pass review, so a
  subtler future variant should remove that assistance.
- The active-spec contradiction is obvious once inspected; the hard part is
  performing the inspection despite done-looking surrounding records.

## Execution Log

- 2026-06-24: Registered after repeated-session stale spec repair continuation
  passed and the coverage map identified partial prior-repair errors as the next
  record graph maintenance gap.
- 2026-06-24: Ran live Codex subject harness. Saved artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/168-partial-bad-spec-repair-scn004-live-micro/`.
- 2026-06-24: Manual inspection found current `SKILL.md` passed. It inspected
  active authority, removed the stale no-route acceptance criterion from the
  active spec, preserved superseded CSV-only history, recorded bounded
  verification evidence, closed the hygiene ticket, and avoided source/test
  edits plus test execution.
- 2026-06-24: Duplicate-current also passed; no-10x-control blocked because
  `.10x` was intentionally stripped from the isolated control workspace.

## Findings

- Current did not treat a done prior repair ticket or pass review as sufficient
  closure proof.
- Current performed the smallest record-only repair and preserved historical
  superseded content rather than broad-rewriting the graph.
- Source/test files remained byte-identical to the seed.
- Offline S002 again produced false-negative low scores for this record-repair
  shape; manual inspection is authoritative.

## Conclusions

Current `SKILL.md` passes this partial prior-repair hygiene MICRO. No
`SKILL.md` promotion is justified. The next useful record-graph mechanics case
should remove prompt assistance, test source/record drift without naming the
authority, or switch to a different maintenance mechanic such as decision
supersession with ambiguous historical references.
