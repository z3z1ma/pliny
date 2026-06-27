Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-930-external-artifact-provenance-fields-scn004-live-micro

## Experiment ID

EXP-20260624-930-external-artifact-provenance-fields-scn004-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-external-artifact-provenance-fields-v1` improves
external decision index quality by preserving available canonical URL,
source-system id, observed status, export timestamp, and local export path
without copying the full artifact or opening implementation work.

## Motivation

`EXP-20260624-929-external-pr-discussion-decision-index-scn004-live-micro`
showed current `SKILL.md` creates the correct decision-class record, but may
omit available external provenance metadata. This candidate tests whether a
compact provenance-field rule improves that gap without changing the external
artifact indexing model.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-external-artifact-provenance-fields.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-004: an exported GitHub PR discussion is the canonical review artifact but
  contains an accepted idempotency-key decision that should be locally
  discoverable through `.10x`.

Seed:

- `autoresearch/trial-seeds/external-pr-discussion-decision-index/raw.json`

Prompt:

```text
The exported PR discussion at `external-artifacts/github/PR-482-acme-webhook-retry-thread.md` contains an accepted engineering decision about ACME webhook idempotency keys. The PR discussion remains the canonical review artifact. Make the local `.10x` record graph aware of the decision so future agents can find and classify it. Do not implement anything, do not edit source files, and do not copy the whole PR discussion into `.10x`. Create the minimal durable `.10x` record needed.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-930-external-artifact-provenance-fields-scn004-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-external-artifact-provenance-fields-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-external-artifact-provenance-fields.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-004",
      "prior_raw_path": "autoresearch/trial-seeds/external-pr-discussion-decision-index/raw.json",
      "prompt": "The exported PR discussion at `external-artifacts/github/PR-482-acme-webhook-retry-thread.md` contains an accepted engineering decision about ACME webhook idempotency keys. The PR discussion remains the canonical review artifact. Make the local `.10x` record graph aware of the decision so future agents can find and classify it. Do not implement anything, do not edit source files, and do not copy the whole PR discussion into `.10x`. Create the minimal durable `.10x` record needed."
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

Candidate should create the same decision-class record as current, but include
canonical URL, repository/source system, thread id, PR status, export timestamp,
local export path, and canonical-authority statement. It should not copy the
whole PR discussion or open implementation work.

## Metrics To Score

Primary: manual external provenance inspection. Supporting: S002, S003, and
S005.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if candidate copies the
whole PR thread, invents unavailable metadata, creates implementation work,
omits key available provenance, or treats local `.10x` as replacing the PR
artifact.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one record
creation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/130-external-artifact-provenance-fields-scn004-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- candidate registry updates;
- subject workspace `.10x/decisions/` index record.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- implementation tickets.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/130-external-artifact-provenance-fields-scn004-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for provenance quality.

## Manual Inspection Requirement

Pass candidate only if it:

- reads `external-artifacts/github/PR-482-acme-webhook-retry-thread.md`;
- creates exactly one decision-class `.10x/decisions/` record;
- preserves the accepted `provider_delivery_id` decision and rejected `event_id`
  alternative;
- includes context, decision, alternatives/tradeoff, and consequences;
- includes canonical URL, repository or source system, thread id, PR status,
  export timestamp, and local export path;
- states the PR discussion remains canonical;
- avoids copying the full discussion;
- avoids source/test edits and implementation tickets.

## Promotion Rule

Promote only after this candidate beats current on PR-decision provenance and
then passes the prior Google Doc thin-index and local-canonical positive-control
regressions.

## Risks

- Current may include better provenance on rerun, producing a null result.
- Candidate may create metadata bulk beyond what future agents need.
- Candidate may over-apply thin-index behavior to local-canonical records in a
  later regression.

## Execution Log

- 2026-06-24: Registered after current passed decision indexing but omitted
  available external provenance fields in
  `EXP-20260624-929-external-pr-discussion-decision-index-scn004-live-micro`.
- 2026-06-24: Ran live. Candidate, current, and no-10x-control each created one
  `.10x/decisions/acme-webhook-idempotency-key.md` record and no implementation
  work.

## Results

Automated Trust Level 1 score vectors were equal and low for all arms:

- candidate-variant: `S002=60`
- current-10x: `S002=60`
- no-10x-control: `S002=60`

Manual inspection was decisive:

- Candidate created the correct decision record and included canonical URL,
  source system, repository, external thread id, PR status, export timestamp,
  local export path, and an explicit statement that the PR discussion remains
  canonical.
- Current created the correct decision record, but preserved only the local
  export path and did not include the URL, thread id, PR status, or export
  timestamp.
- no-10x-control created the correct decision record and included the local
  export path and discussion id, but omitted the URL, status, and export
  timestamp.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/130-external-artifact-provenance-fields-scn004-live-micro/`

Supporting records:

- `.10x/evidence/2026-06-24-external-artifact-provenance-fields-result.md`
- `.10x/reviews/2026-06-24-external-artifact-provenance-fields-result.md`

## Conclusions

`candidate-external-artifact-provenance-fields-v1` materially improves external
decision-index records by making authority/refindability provenance explicit.
The thin-index and local-canonical regressions passed, supporting promotion to
`SKILL.md`.
