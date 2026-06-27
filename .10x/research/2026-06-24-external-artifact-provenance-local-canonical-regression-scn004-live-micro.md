Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-932-external-artifact-provenance-local-canonical-regression-scn004-live-micro

## Experiment ID

EXP-20260624-932-external-artifact-provenance-local-canonical-regression-scn004-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Regression hypothesis: `candidate-external-artifact-provenance-fields-v1` should
not over-apply thin-index behavior when the user explicitly ratifies local
`.10x/specs/` as the canonical implementation contract.

## Motivation

The provenance-field candidate strengthens the requirements for external
canonical artifact indexes. Before promotion, it must preserve the existing
authority-transfer behavior: when local `.10x` becomes canonical, the record
must become a full behavioral contract, with the external artifact retained as
provenance.

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

- SCN-004: the exported Google Doc PRD remains provenance, but Product and
  Engineering explicitly ratify the local `.10x/specs/` record as the canonical
  implementation contract.

Seed:

- `autoresearch/trial-seeds/external-local-spec-canonical-positive-control/raw.json`

Prompt:

```text
The exported Google Doc at `external-artifacts/google-docs/GDOC-nimbus-retention-prd.md` was the approved source PRD for Nimbus retention controls. Product and Engineering have now explicitly ratified that the local `.10x/specs/nimbus-retention-controls.md` record should become the canonical implementation contract. Create that active local `.10x` spec from the approved PRD content. Preserve the Google Doc URL, document ID, revision, and local export path as provenance, but do not leave the local record as only a thin index. Do not implement source changes, do not create implementation tickets, and do not run tests.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-932-external-artifact-provenance-local-canonical-regression-scn004-live-micro",
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
      "prior_raw_path": "autoresearch/trial-seeds/external-local-spec-canonical-positive-control/raw.json",
      "prompt": "The exported Google Doc at `external-artifacts/google-docs/GDOC-nimbus-retention-prd.md` was the approved source PRD for Nimbus retention controls. Product and Engineering have now explicitly ratified that the local `.10x/specs/nimbus-retention-controls.md` record should become the canonical implementation contract. Create that active local `.10x` spec from the approved PRD content. Preserve the Google Doc URL, document ID, revision, and local export path as provenance, but do not leave the local record as only a thin index. Do not implement source changes, do not create implementation tickets, and do not run tests."
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

Candidate should create one active local spec with enough behavior and
acceptance criteria to serve as the implementation contract. It should keep the
external Google Doc provenance, but should not leave the record as a thin
pointer.

## Metrics To Score

Primary: manual external authority-transfer inspection. Supporting: S002, S003,
and S005.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if candidate creates only
a thin pointer record, still says the Google Doc remains canonical, omits PRD
behavior needed for implementation, opens implementation tickets, edits source,
or runs tests.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one record
creation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/132-external-artifact-provenance-local-canonical-regression-scn004-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x/specs/nimbus-retention-controls.md`.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- implementation tickets;
- test execution.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/132-external-artifact-provenance-local-canonical-regression-scn004-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for external artifact authority transfer.

## Manual Inspection Requirement

Pass candidate only if it:

- reads the exported Google Doc PRD;
- creates `.10x/specs/nimbus-retention-controls.md` with `Status: active`,
  `Created`, and `Updated` headers;
- states the local `.10x` spec is the canonical implementation contract;
- includes the Google Doc URL, document ID, revision, and local export path as
  provenance;
- carries over enough purpose, scope, exclusions, behavior, scenarios,
  acceptance criteria, and constraints to be regeneration-grade;
- avoids creating a thin pointer only;
- avoids implementation tickets, source/test edits, and test execution.

## Promotion Rule

This is a regression control for
`candidate-external-artifact-provenance-fields-v1`. If candidate fails, do not
promote the candidate even though it won the PR-discussion primary scenario.

## Risks

- The prompt explicitly states the authority transfer, so this is a positive
  control rather than an adversarial ambiguity test.
- S002 may not distinguish thin indexes from full canonical specs; manual
  inspection is authoritative.

## Execution Log

- 2026-06-24: Registered after the PR-discussion provenance candidate primary
  run showed a candidate win over current.
- 2026-06-24: Ran live. Candidate, current, and no-10x-control each created one
  `.10x/specs/nimbus-retention-controls.md` record and no implementation work.

## Results

Automated Trust Level 1 score vectors:

- candidate-variant: `S002=75`
- current-10x: `S002=75`
- no-10x-control: `S002=60`

Manual inspection was decisive. Candidate passed:

- read the exported Google Doc PRD;
- created `.10x/specs/nimbus-retention-controls.md` with `Status: active`;
- stated the local `.10x` spec is the canonical implementation contract;
- preserved Google Doc URL, document ID, revision, observed status, owner,
  approved date, and local export path as provenance;
- carried over purpose, scope, exclusions, behavior, scenarios, acceptance
  criteria, and constraints;
- avoided creating a thin pointer only;
- edited no source/test files, opened no implementation tickets, and ran no
  tests.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/132-external-artifact-provenance-local-canonical-regression-scn004-live-micro/`

Supporting records:

- `.10x/evidence/2026-06-24-external-artifact-provenance-fields-result.md`
- `.10x/reviews/2026-06-24-external-artifact-provenance-fields-result.md`

## Conclusions

The candidate does not over-apply thin-index behavior when local `.10x` is
explicitly made canonical. It preserves external provenance while producing a
full local behavioral contract.
