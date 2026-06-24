Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-931-external-artifact-provenance-thin-index-regression-scn004-live-micro

## Experiment ID

EXP-20260624-931-external-artifact-provenance-thin-index-regression-scn004-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Regression hypothesis: `candidate-external-artifact-provenance-fields-v1` should
preserve external provenance without weakening the already-passing thin-index
behavior when a Google Doc PRD remains canonical.

## Motivation

`EXP-20260624-930-external-artifact-provenance-fields-scn004-live-micro`
showed the candidate improves PR-discussion provenance fields. Before promotion,
the candidate must not cause the agent to copy external canonical artifacts into
`.10x` or turn thin index records into full local contracts.

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

- SCN-004: an exported Google Doc PRD is canonical and approved; the agent
  should create one thin local `.10x` index record.

Seed:

- `autoresearch/fixtures/live-seeds/external-google-doc-prd-thin-index/raw.json`

Prompt:

```text
The exported Google Doc at `external-artifacts/google-docs/GDOC-nimbus-retention-prd.md` is the canonical approved PRD for Nimbus retention controls. Make the 10x record graph aware of it so future agents can find and classify it. The Google Doc remains canonical; do not implement anything, do not edit source, and do not copy the whole PRD into `.10x`. Create the minimal durable `.10x` index record needed.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-931-external-artifact-provenance-thin-index-regression-scn004-live-micro",
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
      "prior_raw_path": "autoresearch/fixtures/live-seeds/external-google-doc-prd-thin-index/raw.json",
      "prompt": "The exported Google Doc at `external-artifacts/google-docs/GDOC-nimbus-retention-prd.md` is the canonical approved PRD for Nimbus retention controls. Make the 10x record graph aware of it so future agents can find and classify it. The Google Doc remains canonical; do not implement anything, do not edit source, and do not copy the whole PRD into `.10x`. Create the minimal durable `.10x` index record needed."
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

Candidate should still create exactly one thin specification-class index record.
It may include more provenance fields than current, but it must not copy the
full PRD or imply that `.10x` replaces the Google Doc.

## Metrics To Score

Primary: manual thin-index regression inspection. Supporting: S002, S003, and
S005.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if candidate copies the
PRD wholesale, treats local `.10x` as canonical, opens implementation work,
edits source, or omits the durable external pointer.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one record
creation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/131-external-artifact-provenance-thin-index-regression-scn004-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x` index record.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- implementation tickets.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/131-external-artifact-provenance-thin-index-regression-scn004-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for external canonical artifact indexing.

## Manual Inspection Requirement

Pass candidate only if it:

- reads `external-artifacts/google-docs/GDOC-nimbus-retention-prd.md`;
- creates exactly one thin `.10x/specs/` index record or equivalent
  specification-class index;
- includes `Status`, `Created`, and `Updated` headers;
- identifies the external artifact as the canonical approved PRD/spec;
- includes durable provenance such as canonical URL, document ID, observed
  revision/date, and local export path;
- summarizes scope and exclusions enough for future routing;
- states the Google Doc remains canonical;
- avoids copying the full PRD body, all scenarios, or all acceptance criteria;
- avoids source/test edits and implementation tickets.

## Promotion Rule

This is a regression control for
`candidate-external-artifact-provenance-fields-v1`. If candidate fails, do not
promote the candidate even though it won the PR-discussion primary scenario.

## Risks

- S002 may not distinguish thin indexes from copied local specs; manual review
  must enforce economy and external authority preservation.
- The candidate may add useful provenance fields but accidentally make records
  too bulky.

## Execution Log

- 2026-06-24: Registered after the PR-discussion provenance candidate primary
  run showed a candidate win over current.
- 2026-06-24: Ran live. Candidate, current, and no-10x-control each created one
  specification-class index record and no implementation work.

## Results

Automated Trust Level 1 score vectors were equal and low for all arms:

- candidate-variant: `S002=40`
- current-10x: `S002=40`
- no-10x-control: `S002=40`

Manual inspection overrides the heuristic score. Candidate passed:

- read the exported Google Doc PRD;
- created one thin `.10x/specs/nimbus-retention-controls-prd.md` index record;
- included canonical URL, source system, document ID, observed status, revision,
  owner, approved date, and local export path;
- stated the Google Doc remains canonical and the local record is only an index;
- kept the record to 31 lines versus the 78-line external PRD;
- did not copy the PRD body, all scenarios, or all acceptance criteria;
- created no implementation tickets and edited no source/test files.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/131-external-artifact-provenance-thin-index-regression-scn004-live-micro/`

Supporting records:

- `.10x/evidence/2026-06-24-external-artifact-provenance-fields-result.md`
- `.10x/reviews/2026-06-24-external-artifact-provenance-fields-result.md`

## Conclusions

The candidate does not regress thin external-artifact indexing. It adds useful
provenance while preserving economy and canonical-external authority.
