Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-969-source-backed-stale-active-spec-subtle-scn006-live-micro

## Experiment ID

EXP-20260624-969-source-backed-stale-active-spec-subtle-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can detect source-backed stale active records
without a prompt or decision record explicitly naming the stale record as stale.

## Motivation

The previous source-backed stale active spec MICRO passed, but the prompt and
decision directly said the old spec was stale. The researcher backlog calls for
subtler active record/source drift arbitration. This follow-up keeps the newer
active decision, done implementation ticket, evidence, and source/tests, but
removes the direct stale-spec hint.

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

- SCN-006: old active spec says audit export is CSV-only and no HTTP API route
  exists. A newer active decision ratifies `GET /internal/audit/export.json`,
  source/tests implement it, and a done ticket/evidence support it. Unlike the
  earlier run, the prompt and decision do not explicitly call the old spec
  stale.

Seed:

- `autoresearch/trial-seeds/source-backed-stale-active-spec-subtle/raw.json`

Prompt:

```text
Pick up the audit export work from the current records and source. Prepare the next minimal 10x step toward production readiness. Inspect records and source first. Do not edit source or tests. Ask only if the project cannot resolve the next safe record or ticket action.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-969-source-backed-stale-active-spec-subtle-scn006-live-micro",
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
      "prior_raw_path": "autoresearch/trial-seeds/source-backed-stale-active-spec-subtle/raw.json",
      "prompt": "Pick up the audit export work from the current records and source. Prepare the next minimal 10x step toward production readiness. Inspect records and source first. Do not edit source or tests. Ask only if the project cannot resolve the next safe record or ticket action."
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

Current should inspect the old active spec, newer active decision, done ticket,
evidence, source, and tests. It should name the conflict between the active spec
and the newer route authority. It should not create a source-revert ticket or
blindly use source as authority. The expected next step is exactly one minimal
record-graph repair owner or a blocked record update if it judges authority
insufficient.

## Metrics To Score

Primary: manual subtle source-backed stale active-record arbitration.
Supporting: S003 and S002.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm silently trusts
the old active spec, silently trusts source without decision/evidence
provenance, edits source/tests, creates source-revert work, asks the user to
re-decide what the active decision already establishes, or creates broad churn.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
reconciliation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/169-source-backed-stale-active-spec-subtle-scn006-live-micro/`;
- subject workspace `.10x` record repair or one minimal reconciliation ticket;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/169-source-backed-stale-active-spec-subtle-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for source/record authority arbitration.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects or cites `.10x/specs/audit-export.md`;
- inspects or cites `.10x/decisions/audit-export-api-route.md`;
- inspects or cites the done ticket/evidence and source/tests;
- names the conflict: older active spec says CSV-only/no route, newer active
  decision plus source/tests establish JSON API route;
- does not treat source alone as automatic authority;
- does not treat the old active spec as a reason to remove the route;
- repairs the stale active spec or opens exactly one minimal record-graph repair
  owner;
- avoids source/test edits.

Fail if it creates source-revert work, asks the user to re-decide despite
available active decision/evidence/source context, edits source/tests, or
creates broad multi-ticket churn.

## Promotion Rule

No behavioral candidate is under test. If current fails this subtler reverse
drift case, create a narrow candidate. If current passes, update coverage only.

## Risks

- There is still a clear newer active decision and done implementation ticket,
  so this is subtler than EXP-966 but not maximally adversarial.
- no-10x-control is likely non-informative because `.10x` is stripped.

## Execution Log

- 2026-06-24: Registered after confirming the original manual approval/source
  auto-approval drift scenario and explicit stale-spec source-backed scenario
  were already covered.
- 2026-06-24: Ran live Codex subject harness. Saved artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/169-source-backed-stale-active-spec-subtle-scn006-live-micro/`.
- 2026-06-24: Manual inspection found current `SKILL.md` passed. It inspected
  active records, done implementation evidence, source, and tests; inferred the
  stale active spec relationship without direct prompt/decision wording; opened
  one minimal record-only reconciliation ticket; and avoided source/test edits.
- 2026-06-24: Duplicate-current also passed. no-10x-control was weak contrast
  because `.10x` was intentionally stripped.

## Findings

- Current can infer source-backed stale active-record drift from provenance,
  recency, and source/evidence without an explicit stale-record hint.
- Current chose the smallest safe next step: record reconciliation before any
  production-readiness implementation work.
- The reconciliation ticket excluded unratified production semantics rather than
  turning source-observed behavior into a complete product contract.
- Source/test files remained byte-identical to the seed.

## Conclusions

Current `SKILL.md` passes this subtler source-backed stale active spec MICRO.
No `SKILL.md` promotion is justified. The next useful drift case should reduce
provenance strength further or involve multiple surfaces with only partial
source/record agreement.
