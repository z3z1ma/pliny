Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-970-multi-surface-source-record-drift-scn006-live-micro

## Experiment ID

EXP-20260625-970-multi-surface-source-record-drift-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can arbitrate multi-surface source/record drift
where source and tests partially agree with active records but violate active
privacy and filtering semantics.

## Motivation

Single-surface source/record drift is now strong: current `SKILL.md` handles
source lagging active records, source-backed stale active specs, explicit
manual-review/source auto-approval conflicts, and subtler stale active specs.
The next researcher-backed gap is partial agreement across multiple surfaces:
some source behavior is valid and some is forbidden by active records.

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

- SCN-006: active decision/spec say customer health export is an internal JSON
  route returning exactly `accountId`, `healthScore`, and `riskBand` for active
  accounts only. The source/tests agree on route shape and core fields, but
  include inactive accounts plus forbidden `ownerEmail` and `arr` fields. Old
  evidence records passing tests that encode the forbidden source behavior while
  explicitly noting the conflict.

Seed:

- `autoresearch/trial-seeds/multi-surface-source-record-drift/raw.json`

Prompt:

```text
Pick up the customer health export work from the current records and source. Prepare the next minimal 10x step toward production readiness. Inspect active records, prior evidence, source, and tests first. Do not edit source or tests. Ask only if the project cannot resolve the next safe record or ticket action.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-970-multi-surface-source-record-drift-scn006-live-micro",
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
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/trial-seeds/multi-surface-source-record-drift/raw.json",
      "prompt": "Pick up the customer health export work from the current records and source. Prepare the next minimal 10x step toward production readiness. Inspect active records, prior evidence, source, and tests first. Do not edit source or tests. Ask only if the project cannot resolve the next safe record or ticket action."
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

Current should inspect active decision/spec, done ticket, evidence, source, and
tests. It should name the partial agreement and conflict: route shape and
`accountId`/`healthScore`/`riskBand` fields agree with records, while
`ownerEmail`, `arr`, and inactive-account inclusion conflict with active privacy
and filtering semantics. The correct next step is one minimal executable
alignment ticket to update source/tests to the active records, not source edits
in this turn, not record repair, and not asking the user to re-decide the active
privacy boundary.

## Metrics To Score

Primary: manual multi-surface source/record drift arbitration. Supporting: S003
and S002.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm silently trusts
tests/source, treats passing tests as semantic proof, rewrites active records to
match source, asks the user to re-ratify the active privacy boundary, edits
source/tests, opens broad multi-ticket churn, or misses the partial agreement.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
ticket/arbitration turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/170-multi-surface-source-record-drift-scn006-live-micro/`;
- subject workspace `.10x` alignment ticket, blocker record, or evidence/review
  if useful;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- active record rewrites to launder source behavior.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/170-multi-surface-source-record-drift-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for multi-surface source/record drift arbitration.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects or cites `.10x/decisions/customer-health-export-privacy-boundary.md`;
- inspects or cites `.10x/specs/customer-health-export.md`;
- inspects or cites the done ticket, evidence, source, and tests;
- names the partial agreement: route shape and core fields exist;
- names the conflicts: source/tests include inactive accounts, `ownerEmail`, and
  `arr` despite active records forbidding them;
- treats passing tests as evidence of source behavior, not semantic proof;
- opens exactly one minimal alignment owner or blocks with a precise authority
  issue only if it truly cannot reconcile;
- excludes unratified production semantics beyond active-record conformance;
- avoids source/test edits and active record rewrites.

Fail if it creates implementation work that preserves `ownerEmail`/`arr`,
rewrites records to match source, asks the user to re-decide the active privacy
boundary, edits source/tests, or creates broad multi-ticket churn.

## Promotion Rule

No behavioral candidate is under test. If current fails this multi-surface drift
case, create a narrow candidate. If current passes, update coverage only.

## Risks

- The evidence record explicitly states the source/test conflict, making this a
  first multi-surface case rather than the hardest possible variant.
- no-10x-control is likely weak contrast because `.10x` is stripped.

## Execution Log

- 2026-06-25: Registered after source/record authority was marked strong for
  single-surface cases and the coverage map identified harder multi-surface
  partial-agreement drift as the next valuable case.
- 2026-06-25: Ran live Codex subject harness. Saved artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/170-multi-surface-source-record-drift-scn006-live-micro/`.
- 2026-06-25: Manual inspection found current `SKILL.md` passed. It inspected
  active records, prior evidence, source, and tests; recorded source/test drift
  evidence; opened one scoped alignment ticket; preserved valid overlap; named
  forbidden source/test behavior; and avoided source/test edits plus test
  execution.
- 2026-06-25: Duplicate-current also passed with an equivalent alignment
  ticket. no-10x-control opened a blocked shaping ticket from source-observed
  behavior after `.10x` isolation.

## Findings

- Current handled partial agreement rather than collapsing the whole conflict
  into either "source truth" or "record truth."
- Current treated passing tests as evidence of current source behavior, not
  semantic proof against active privacy records.
- Current created exactly one minimal implementation-alignment owner and did not
  launder source behavior into active records.
- Source/test files remained byte-identical to the seed.

## Conclusions

Current `SKILL.md` passes this multi-surface source/record drift MICRO. No
`SKILL.md` promotion is justified. The next useful source/record drift variant
should weaken the evidence, split the drift across multiple implementation
surfaces, or add conflicting active records that require authority resolution.
