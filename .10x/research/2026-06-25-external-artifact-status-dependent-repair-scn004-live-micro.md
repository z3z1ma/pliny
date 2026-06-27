Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-973-external-artifact-status-dependent-repair-scn004-live-micro

## Experiment ID

EXP-20260625-973-external-artifact-status-dependent-repair-scn004-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can maintain a local `.10x` graph when an
external canonical artifact changes approved revision and dependent ticket,
evidence, and review records still point at the old revision.

## Motivation

Prior external-artifact tests cover first-time thin indexing, local-canonical
transfer, PR discussion decision indexing, Jira delivery-state indexing,
external design-doc supersession, and stale thin-index revision maintenance.
The remaining ranked-push gap is dependent-record repair: active work must move
to the new external authority while historical evidence and reviews for the old
revision remain honest historical artifacts, not proof of the new revision.

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

- SCN-004: approved external Google Doc revision B supersedes revision A. The
  active local thin index, active ticket, evidence, and review still point at
  revision A.

Seed:

- `autoresearch/trial-seeds/external-artifact-status-dependent-repair/raw.json`

Prompt:

```text
The exported Google Doc at `external-artifacts/google-docs/GDOC-atlas-customer-export-prd-rev-b.md` is now Approved and explicitly supersedes revision A of the same canonical document. The current active local index is `.10x/specs/atlas-customer-export-prd-rev-a.md`, and dependent ticket/evidence/review records still point at revision A. Maintain the local `.10x` graph so future agents use revision B as the active external-canonical authority: create or leave exactly one active thin index at `.10x/specs/atlas-customer-export-prd.md`, move or mark revision A as superseded history, repair dependent live records so active work points at revision B, and keep revision A evidence/review historical rather than treating them as proof of revision B. Do not copy the whole Google Doc, do not edit source files, do not create implementation tickets, and do not run tests.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-973-external-artifact-status-dependent-repair-scn004-live-micro",
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
      "prior_raw_path": "autoresearch/trial-seeds/external-artifact-status-dependent-repair/raw.json",
      "prompt": "The exported Google Doc at `external-artifacts/google-docs/GDOC-atlas-customer-export-prd-rev-b.md` is now Approved and explicitly supersedes revision A of the same canonical document. The current active local index is `.10x/specs/atlas-customer-export-prd-rev-a.md`, and dependent ticket/evidence/review records still point at revision A. Maintain the local `.10x` graph so future agents use revision B as the active external-canonical authority: create or leave exactly one active thin index at `.10x/specs/atlas-customer-export-prd.md`, move or mark revision A as superseded history, repair dependent live records so active work points at revision B, and keep revision A evidence/review historical rather than treating them as proof of revision B. Do not copy the whole Google Doc, do not edit source files, do not create implementation tickets, and do not run tests."
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

Current should read the old local index, the new rev B export, the dependent
ticket, evidence, and review. It should leave one active thin index for rev B,
move or mark rev A as superseded, update active work to depend on the rev B
index, preserve rev A evidence/review as historical old-revision artifacts, and
block closure or note that rev B needs fresh evidence/review. It should avoid
copying the full document, source/test edits, tests, and implementation tickets.

## Metrics To Score

Primary: manual external dependent-record repair inspection. Supporting: S002,
S003, and S005.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm leaves rev A as
active authority, copies the full PRD, treats local `.10x` as canonical without
authority transfer, blindly rewrites rev A evidence/review into rev B proof,
opens executable implementation work, edits source/tests, or runs tests.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
external status-change maintenance turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/173-external-artifact-status-dependent-repair-scn004-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x` thin index, supersession, and dependent-record
  maintenance.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- implementation tickets;
- test execution.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/173-external-artifact-status-dependent-repair-scn004-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for external dependent-record repair quality.

## Manual Inspection Requirement

Pass current only if it:

- reads `.10x/specs/atlas-customer-export-prd-rev-a.md`;
- reads
  `external-artifacts/google-docs/GDOC-atlas-customer-export-prd-rev-b.md`;
- inspects the dependent ticket, evidence, and review;
- leaves exactly one active local thin index for revision B at
  `.10x/specs/atlas-customer-export-prd.md` or an equivalent unambiguous active
  path;
- preserves canonical URL, document id, observed status, revision, superseded
  revision, approval/export timestamps, local export path, and external-canonical
  statement;
- moves or marks revision A as superseded history;
- repairs the active ticket dependency and acceptance language so active work
  points at revision B and cannot close on rev A evidence/review;
- preserves revision A evidence/review as historical old-revision artifacts
  rather than proof of revision B;
- avoids source/test edits, test execution, full-doc copying, and implementation
  tickets.

## Promotion Rule

No behavioral candidate is under test. If current fails dependent-record repair,
create a narrow external status-change maintenance candidate. If current passes,
update coverage only.

## Risks

- There is more than one valid record shape for stale evidence/review handling:
  updating their target paths to the superseded rev A record, adding explicit
  stale limits, or both. Manual inspection should judge authority coherence.
- The scenario uses exported files, not live connector refresh.

## Execution Log

- 2026-06-25: Registered as item 4 of the ranked conformance push after
  blocked-run retrospective learning passed.
- 2026-06-25: Ran one live Codex MICRO with no-10x-control, current-10x, and
  duplicate-current candidate arms. Raw artifacts are under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/173-external-artifact-status-dependent-repair-scn004-live-micro/`.
- 2026-06-25: Manual inspection found current `SKILL.md` passed. It created a
  revision B active thin index, superseded revision A, repaired the active
  ticket dependency and acceptance language, kept revision A evidence/review
  historical, and avoided source/test edits plus test execution.

## Findings

- no-10x-control created active/superseded spec records, but control isolation
  removed the seeded dependent ticket, evidence, and review, so it did not
  exercise the dependent-record repair behavior.
- current-10x created `.10x/specs/atlas-customer-export-prd.md` as the single
  active revision B thin index, moved revision A to
  `.10x/specs/superseded/atlas-customer-export-prd-rev-a.md`, and preserved
  external canonical provenance without copying the full document.
- current-10x updated the active ticket to depend on revision B, added `region`
  to the active acceptance language, and stated that revision A evidence/review
  do not prove revision B closure.
- current-10x repointed revision A evidence and review to the superseded
  revision A spec path and preserved their revision-A-only limits.
- duplicate-current produced equivalent passing behavior.
- Trust Level 1 S002 undercounted both canonical arms because the heuristic
  scorer does not model external dependent-record authority repair.

## Conclusions

Current `SKILL.md` passes this external artifact status-change dependent-record
repair MICRO. No candidate or promotion is justified. External artifact
indexing coverage now includes dependent local record repair after a canonical
external revision changes status, with old evidence/reviews preserved as
historical rather than laundered into proof of the new revision.

The remaining external-artifact gap is live connector refresh, not exported-file
record graph maintenance.
