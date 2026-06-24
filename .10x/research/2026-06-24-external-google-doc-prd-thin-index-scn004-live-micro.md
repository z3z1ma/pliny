Status: active
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-910-external-google-doc-prd-thin-index-scn004-live-micro

## Experiment ID

EXP-20260624-910-external-google-doc-prd-thin-index-scn004-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-external-artifact-thin-index-v1` improves behavior when
an external artifact remains canonical but should still be discoverable through
the local `.10x` record graph.

## Motivation

The 10x conformance map marks external artifact indexing as weakly covered. The
current skill already says 10x remains the index for outside artifacts, but this
experiment tests whether the agent creates a useful thin index rather than
ignoring a canonical external PRD or copying it wholesale into `.10x`.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-external-artifact-thin-index.md`.

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
  "experiment_id": "EXP-20260624-910-external-google-doc-prd-thin-index-scn004-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-external-artifact-thin-index-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-external-artifact-thin-index.md"
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

Candidate should create exactly one thin `.10x/specs/` record that classifies
the exported Google Doc as the canonical PRD/spec, includes a durable pointer
and observed revision, summarizes the surface enough for routing, and avoids
copying the whole PRD. Current may already do this.

## Metrics To Score

Primary: manual thin-index inspection. Supporting: S002, S003, and S005.

## Quality Floors

S002 active floor 80. Manual inspection overrides automated scores if an arm
copies the PRD wholesale, fails to create a `.10x` index, treats the local index
as canonical, creates implementation work, or omits the external pointer and
revision.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one record
creation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/110-external-google-doc-prd-thin-index-scn004-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x` index record.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- implementation tickets.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/110-external-google-doc-prd-thin-index-scn004-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for external canonical artifact indexing.

## Manual Inspection Requirement

Pass an arm only if it:

- reads `external-artifacts/google-docs/GDOC-nimbus-retention-prd.md`;
- creates exactly one thin `.10x/specs/` index record or an equivalent
  specification-class index;
- includes `Status`, `Created`, and `Updated` headers;
- identifies the external artifact as the canonical approved PRD/spec;
- includes the canonical URL, document ID, observed revision/date, and local
  export path;
- summarizes scope and exclusions enough for future routing;
- states the Google Doc remains canonical;
- avoids copying the full PRD body, all scenarios, or all acceptance criteria;
- avoids source/test edits and implementation tickets.

Fail or downgrade if it ignores the artifact, copies the PRD wholesale, creates
the wrong record type without classification, omits the durable pointer or
revision, treats the local index as canonical, or opens implementation work.

## Promotion Rule

Promote only if current ignores the external artifact, copies it wholesale, or
creates an ambiguous local record while candidate creates a minimal correct thin
index. If candidate wins, run a positive control where the user explicitly says
the local `.10x` spec should become canonical before promotion.

## Risks

- Current likely already passes because `SKILL.md` has explicit external
  artifact indexing instructions.
- S002 may reward longer copied records, so manual inspection must enforce
  economy and external authority preservation.

## Execution Log

- 2026-06-24: Registered from reused Kierkegaard scout recommendation and the
  latest researcher backlog.
