Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-967-continue-stale-spec-repair-scn004-live-micro

## Experiment ID

EXP-20260624-967-continue-stale-spec-repair-scn004-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can continue a previously opened record-graph
repair ticket, perform the actual spec supersession/reference repair, and close
the existing owner without creating duplicate tickets.

## Motivation

The previous reverse source/record drift MICRO tested opening the correct
record-repair owner. The researcher backlog also calls for record graph
maintenance over repeated sessions, not only one-shot owner creation. This MICRO
starts after the repair owner exists and tests whether the agent finishes that
maintenance coherently.

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

- SCN-004: existing open ticket
  `.10x/tickets/2026-06-24-repair-audit-export-spec.md` owns stale spec repair.
  The stale active spec still says CSV-only/no route, newer decision/source/tests
  establish the API route, and evidence/review records still reference the old
  spec path as the failed target.

Seed:

- `autoresearch/trial-seeds/continue-stale-spec-repair/raw.json`

Prompt:

```text
Continue the existing audit export spec repair work. Complete `.10x/tickets/2026-06-24-repair-audit-export-spec.md` if the records support it: supersede or replace the stale CSV-only active spec, repair live references, record verification evidence as needed, and close the repair ticket coherently. Do not create a duplicate ticket. Do not edit source or tests and do not run tests.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-967-continue-stale-spec-repair-scn004-live-micro",
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
      "prior_raw_path": "autoresearch/trial-seeds/continue-stale-spec-repair/raw.json",
      "prompt": "Continue the existing audit export spec repair work. Complete `.10x/tickets/2026-06-24-repair-audit-export-spec.md` if the records support it: supersede or replace the stale CSV-only active spec, repair live references, record verification evidence as needed, and close the repair ticket coherently. Do not create a duplicate ticket. Do not edit source or tests and do not run tests."
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

Current should reuse the existing repair ticket, inspect the governing decision,
stale spec, evidence, review, done implementation ticket, and source/tests. It
should either move the stale CSV-only spec to `specs/superseded/` and create a
new active API-route spec, or replace the stale active spec in place with clear
supersession provenance. It should repair live references, create record-only
verification evidence if useful, close or move the repair ticket to `done/`, and
avoid duplicate tickets, source/test edits, and test execution.

## Metrics To Score

Primary: manual repeated-session record maintenance inspection. Supporting:
S002 and S006.

## Quality Floors

Manual inspection is authoritative. Fail if an arm creates a duplicate ticket,
leaves the stale CSV-only active spec active, leaves live headers pointing at the
wrong authority, edits source/tests, or runs tests.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one record
maintenance turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/167-continue-stale-spec-repair-scn004-live-micro/`;
- subject workspace `.10x` record repair, verification evidence, review updates,
  and repair ticket closure;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- test execution.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/167-continue-stale-spec-repair-scn004-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for repeated-session record maintenance.

## Manual Inspection Requirement

Pass an arm only if it:

- reuses `.10x/tickets/2026-06-24-repair-audit-export-spec.md` rather than
  creating a duplicate owner;
- removes CSV-only/no-route behavior from active specification authority;
- preserves the stale CSV-only behavior as superseded history or clear
  supersession provenance;
- leaves exactly one active audit export spec aligned to
  `.10x/decisions/audit-export-api-route.md`;
- repairs live references after move/rename/replacement;
- closes the repair ticket coherently or leaves a precise blocker only if the
  record graph truly lacks authority;
- avoids source/test edits and test execution.

Fail if it opens a duplicate ticket, leaves conflicting active specs, broad
rewrites historical mentions incorrectly, edits source/tests, runs tests, or
claims closure without evidence of reference repair.

## Promotion Rule

No behavioral candidate is under test. If current fails repeated-session record
maintenance, create a narrow candidate. If current passes, update coverage only.

## Risks

- There are multiple acceptable repair shapes. Manual review should judge graph
  coherence, not require one exact filename.
- The seed directly marks the old spec stale; future variants should make the
  stale relationship subtler.

## Execution Log

- 2026-06-24: Registered after source-backed stale active spec owner creation
  passed for current `SKILL.md`.
- 2026-06-24: Ran live Codex subject harness. Saved artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/167-continue-stale-spec-repair-scn004-live-micro/`.
- 2026-06-24: Manual inspection found current `SKILL.md` passed. It reused the
  existing repair ticket, preserved the stale CSV-only spec under
  `.10x/specs/superseded/`, replaced the active spec with the JSON API route
  contract, repaired references, recorded verification evidence, moved the
  repair ticket to `done/`, and did not edit source/tests or run tests.
- 2026-06-24: Duplicate-current also passed the minimum seed requirements but
  used lower-quality in-place replacement instead of preserving explicit
  superseded history. no-10x-control blocked because isolated control workspaces
  intentionally do not inherit `.10x`.

## Findings

- Current `SKILL.md` can continue a previously opened record graph repair owner
  rather than creating duplicate work.
- Current distinguished active specification authority from superseded
  historical context and avoided source-revert work.
- Current's repair preserved provenance better than the duplicate-current arm by
  keeping an explicit superseded copy of the stale CSV-only contract.
- The Trust Level 1 S002 scorer produced false-negative low scores for the
  10x arms, so manual inspection is authoritative for this repeated-session
  record maintenance case.

## Conclusions

Current `SKILL.md` passes this record graph maintenance MICRO. No `SKILL.md`
promotion is justified. The next useful variants should reduce prompt assistance
by making the stale relationship subtler, introducing a partially wrong prior
repair, or combining stale active record repair with less obvious source-backed
authority.
