Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-942-external-google-doc-stale-thin-index-revision-scn004-live-micro

## Experiment ID

EXP-20260624-942-external-google-doc-stale-thin-index-revision-scn004-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can maintain an existing active thin index when a
newer approved export of the same canonical external Google Doc appears, without
copying the full document or converting the local record into canonical
implementation authority.

## Motivation

External artifact coverage now includes first-time thin indexing and external
design-doc supersession of a full local spec. The remaining gap is revision
maintenance after a local thin index already exists: future agents must not
continue using stale revision A metadata when approved revision B is available.

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

- SCN-004: active local thin index points to Google Doc revision A; newer
  approved revision B export is now available and the Google Doc remains
  canonical.

Seed:

- `autoresearch/trial-seeds/external-google-doc-stale-thin-index-revision/raw.json`

Prompt:

```text
The local `.10x/specs/nimbus-retention-controls.md` record is an active thin index to Google Doc revision A. A newer exported Google Doc revision is now available at `external-artifacts/google-docs/GDOC-nimbus-retention-prd-rev-b.md`, with the same canonical document ID and status Approved. Maintain the local `.10x` record graph so future agents do not rely on the stale revision A index. The external Google Doc remains canonical; do not make the local record the implementation contract, do not copy the whole doc, do not edit source, do not create implementation tickets, and do not run tests.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-942-external-google-doc-stale-thin-index-revision-scn004-live-micro",
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
      "prior_raw_path": "autoresearch/trial-seeds/external-google-doc-stale-thin-index-revision/raw.json",
      "prompt": "The local `.10x/specs/nimbus-retention-controls.md` record is an active thin index to Google Doc revision A. A newer exported Google Doc revision is now available at `external-artifacts/google-docs/GDOC-nimbus-retention-prd-rev-b.md`, with the same canonical document ID and status Approved. Maintain the local `.10x` record graph so future agents do not rely on the stale revision A index. The external Google Doc remains canonical; do not make the local record the implementation contract, do not copy the whole doc, do not edit source, do not create implementation tickets, and do not run tests."
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

Current should read the existing local thin index and new rev B export, detect
that revision A is stale, leave exactly one active thin index for rev B, preserve
available provenance, keep the external Google Doc canonical, avoid copying the
full PRD, avoid source/test edits, avoid tests, and avoid implementation
tickets.

## Metrics To Score

Primary: manual external revision-maintenance inspection. Supporting: S002,
S003, and S005.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm leaves revision
A as the active index, copies the full external document, treats local `.10x` as
canonical without explicit authority transfer, opens executable implementation
work, treats external approval as implementation completion, edits source/tests,
or runs tests.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
external revision-maintenance turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/142-external-google-doc-stale-thin-index-revision-scn004-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x` thin index maintenance records.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- implementation tickets;
- test execution.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/142-external-google-doc-stale-thin-index-revision-scn004-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for external revision-maintenance quality.

## Manual Inspection Requirement

Pass current only if it:

- reads `.10x/specs/nimbus-retention-controls.md`;
- reads `external-artifacts/google-docs/GDOC-nimbus-retention-prd-rev-b.md`;
- detects revision A is stale relative to approved revision B;
- leaves exactly one active local index for revision B;
- preserves canonical URL, document id, observed status, revision, approval and
  export timestamps, local export path, and external-canonical statement;
- keeps the local record thin and does not copy the full PRD;
- avoids source/test edits, test execution, implementation tickets, and local
  canonical authority transfer.

## Promotion Rule

No promotion from registration alone. If current and duplicate-current fail,
create a narrow external revision-maintenance candidate and rerun with thin
index, local-canonical, PR-discussion, Jira delivery-state, and design-doc
supersession regressions.

## Risks

- Updating the existing active thin index in place and moving revision A to a
  superseded index are both acceptable if only one active rev B index remains.
- The scenario uses exported files, not a live connector status check.

## Execution Log

- 2026-06-24: Registered from external status/revision maintenance scout after
  external design-doc supersession passed.
- 2026-06-24: Ran live Codex subject harness with three arms. Manual inspection
  passed current and duplicate-current despite low S002 heuristic telemetry:
  both updated the active thin index to revision B, preserved external
  provenance and canonical authority, avoided copying the full PRD, and avoided
  source/test/ticket work. no-10x-control also updated to revision B but with a
  thinner provenance set, so this is positive conformance coverage rather than
  a promotion signal.

## Result

Pass for current `SKILL.md`. No `SKILL.md` promotion is justified.

Supporting records:

- `.10x/evidence/2026-06-24-external-google-doc-stale-thin-index-revision-result.md`
- `.10x/reviews/2026-06-24-external-google-doc-stale-thin-index-revision-result.md`
