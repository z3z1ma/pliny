Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-941-external-design-doc-supersedes-local-spec-scn004-live-micro

## Experiment ID

EXP-20260624-941-external-design-doc-supersedes-local-spec-scn004-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can update the local record graph when an
approved external design document explicitly supersedes an active local spec
while remaining the canonical revised behavior source.

## Motivation

External artifact coverage now includes Google Doc thin indexes, local-canonical
authority transfer, PR-discussion decision indexes, and Jira delivery-state
local context. The remaining external-artifact gap is supersession: future
agents must not keep using an older active local spec after an external
canonical artifact supersedes it.

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

- SCN-004: approved external design revision B supersedes an active local Nimbus
  retention spec, and the external design document remains canonical.

Seed:

- `autoresearch/fixtures/live-seeds/external-design-doc-supersedes-local-spec/raw.json`

Prompt:

```text
The exported design doc at `external-artifacts/google-docs/GDOC-nimbus-retention-design-rev-b.md` is approved and explicitly supersedes the existing local `.10x/specs/nimbus-retention-controls.md` spec. The external design doc remains canonical for the revised behavior. Update the local `.10x` record graph so future agents do not treat the old local spec as active authority. Preserve available provenance, do not copy the whole design doc, do not edit source, do not create implementation tickets, and do not run tests.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-941-external-design-doc-supersedes-local-spec-scn004-live-micro",
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
      "prior_raw_path": "autoresearch/fixtures/live-seeds/external-design-doc-supersedes-local-spec/raw.json",
      "prompt": "The exported design doc at `external-artifacts/google-docs/GDOC-nimbus-retention-design-rev-b.md` is approved and explicitly supersedes the existing local `.10x/specs/nimbus-retention-controls.md` spec. The external design doc remains canonical for the revised behavior. Update the local `.10x` record graph so future agents do not treat the old local spec as active authority. Preserve available provenance, do not copy the whole design doc, do not edit source, do not create implementation tickets, and do not run tests."
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

Current should read both the existing local active spec and the external rev B
design doc, mark or move the old local spec out of active authority, create one
active thin local index for the external canonical rev B design doc, preserve
available provenance, and avoid source/test edits, test execution, and
implementation tickets.

## Metrics To Score

Primary: manual external supersession and record-graph inspection. Supporting:
S002, S003, and S005.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm leaves the old
rev A spec active as authority, treats local `.10x` as canonical without
explicit transfer, copies the whole design doc, opens executable implementation
work, edits source/tests, or runs tests.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
record-graph supersession/indexing turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/141-external-design-doc-supersedes-local-spec-scn004-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x` spec supersession/index records.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- implementation tickets;
- test execution.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/141-external-design-doc-supersedes-local-spec-scn004-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for external supersession quality.

## Manual Inspection Requirement

Pass current only if it:

- reads `.10x/specs/nimbus-retention-controls.md`;
- reads
  `external-artifacts/google-docs/GDOC-nimbus-retention-design-rev-b.md`;
- identifies that rev B supersedes the old local spec;
- ensures the old rev A local spec is no longer active authority;
- creates or updates one active local thin index for rev B rather than a full
  copied local contract;
- preserves canonical URL, document id, status, revision, approval/export
  timestamps, local export path, and external-canonical statement;
- avoids duplicate conflicting active specs, source/test edits, test execution,
  and implementation tickets.

## Promotion Rule

No promotion from registration alone. If current and duplicate-current fail,
create a narrow external supersession candidate and rerun with Google Doc
thin-index, local-canonical, PR-discussion, and Jira delivery-state regressions.

## Risks

- There may be more than one acceptable repair shape: move old spec to
  `specs/superseded/` and create a new active thin index, or update the old
  record in place to become the active rev B index while preserving rev A
  history. Manual inspection should judge authority coherence, not one exact
  file path.
- The seed has no dependent tickets or reviews, so reference repair breadth is
  intentionally narrow.

## Execution Log

- 2026-06-24: Registered from external artifact conformance backlog and
  design-doc/status-change scout recommendation.
- 2026-06-24: Ran live. Current and duplicate-current preserved revision A as
  superseded history and created one active thin local index for canonical
  external revision B. no-10x-control moved the old spec to superseded but left
  no active local index.

## Results

Trust Level 1 automated scoring:

- current-10x: `S002=75`
- duplicate-current: `S002=75`
- no-10x-control: `S002=60`

Manual inspection was decisive:

- current read the old local active spec and external rev B design doc;
- current moved revision A to
  `.10x/specs/superseded/nimbus-retention-controls-rev-a.md`;
- current created `.10x/specs/nimbus-retention-controls.md` as an active thin
  index to the external rev B design doc;
- current preserved canonical URL, document id, revision, approved status,
  owner, approval date, export timestamp, local export path, and supersession
  link;
- current stated that the external design doc remains canonical and that the
  local record is only an index, not a complete implementation specification;
- current avoided copying the whole design doc, source/test edits, test
  execution, and implementation tickets;
- no-10x-control marked the old spec superseded but created no active
  replacement index, leaving future agents without an active local pointer to
  the canonical rev B artifact.

Supporting records:

- `.10x/evidence/2026-06-24-external-design-doc-supersession-result.md`
- `.10x/reviews/2026-06-24-external-design-doc-supersession-result.md`

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/141-external-design-doc-supersedes-local-spec-scn004-live-micro/`

## Conclusion

Current `SKILL.md` handles external design-doc supersession of an active local
spec when the external artifact remains canonical. No `SKILL.md` promotion is
justified. External artifact indexing coverage now includes thin index,
local-canonical transfer, PR decision indexing, Jira delivery-state local
context, and design-doc supersession. Remaining gap: status/revision maintenance
after an existing thin index goes stale.
