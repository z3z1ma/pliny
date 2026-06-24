Status: done
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-857-challenge-request-validity-scn010-live-micro

## Experiment ID

EXP-20260623-857-challenge-request-validity-scn010-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-challenge-request-validity-v1` improves minimalism by
challenging requested implementation work when existing code and records show
the requested solution should not exist.

## Motivation

10x should not behave like a ticket machine. The skill already values
minimalism, but this MICRO tests whether the agent challenges the request itself
when the user asks for a broad framework that contradicts existing project
authority.

## Method Tier

MICRO using a tracked request-validity seed.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-challenge-request-validity.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-010: the user asks for a reusable client-side CSV export framework, but
  active records and source say report export is server-owned through
  `/api/reports/export.csv` and client-side CSV builders are explicitly rejected.

Seed:

- `autoresearch/fixtures/live-seeds/challenge-request-validity/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-857-challenge-request-validity-scn010-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-challenge-request-validity-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-challenge-request-validity.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-010",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/challenge-request-validity/raw.json",
      "prompt": "Add a reusable client-side CSV export framework for the Reports dashboard so filtered results export correctly. Use PapaParse or a similar dependency if needed. Do not ask questions; open the implementation ticket if you need a ticket first."
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

Current may already pass because canonical `SKILL.md` includes operational
minimalism and active-record authority rules. Candidate should pass by making
request-validity challenge explicit.

## Metrics To Score

Primary: manual request-validity inspection, S005, and S007.

## Quality Floors

S005 active floor 75. S007 is partial and requires manual inspection.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one shaping
or ticket-opening turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/057-challenge-request-validity-scn010-live-micro/`;
- records created in the subject workspace under `.10x/` only;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- source files;
- dependency additions.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/057-challenge-request-validity-scn010-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for whether the request was challenged correctly.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects records or source before accepting the requested framework;
- identifies that server-owned export already satisfies filtered export;
- does not add dependencies, edit source, or open implementation work for a
  client-side CSV framework;
- recommends the smaller valid path: reuse `/api/reports/export.csv`, possibly
  document or ticket only a missing link if evidence shows one is missing.

Fail if it opens or implements a client-side CSV framework, adds a CSV
dependency, or ignores the active decision rejecting client-side report export.

## Promotion Criteria

Positive candidate-over-current signal should trigger promotion review for a
narrow "challenge whether this work should exist" rule. Null versus current
should discard.

## Known Risks And Confounders

- Current `SKILL.md` already contains strong minimalism and active-record
  authority language, so this may be a null run.
- The seed includes a clear active decision, making the intended challenge
  easier than subtler real-world cases.
- The no-10x control has inherited `.10x` removed, but source still exposes the
  existing server-export URL helper.

## Execution Log

- 2026-06-23: Registered after promoting scoped revalidation. This tests whether
  10x challenges the requested solution itself rather than shaping a ticket for
  unnecessary work.

## Results

Ran one live Codex sample for each arm.

Automated Trust Level 1 score vectors:

- current-10x: `S005=95`, `S007=10`
- candidate-variant: `S005=95`, `S007=10`
- no-10x-control: `S005=55`, `S007=10`

Manual inspection found:

- current-10x inspected active records and source, recognized that the requested
  client-side CSV framework conflicted with
  `.10x/decisions/server-owned-report-export.md` and
  `.10x/knowledge/report-export-conventions.md`, opened
  `.10x/tickets/2026-06-24-client-side-report-csv-export.md` as `blocked`, and
  made no source or dependency changes.
- candidate-variant inspected active records and source, recognized the same
  conflict, created no files, and recommended the smaller valid path:
  use `reportExportUrl(filters)` and `/api/reports/export.csv`.
- no-10x-control had inherited `.10x` removed and implemented a native
  client-side CSV framework in `src/reports/csvExport.js` with tests and a
  `package.json` module change.
- The canonical guard reported no changes to `SKILL.md` or
  `autoresearch/program.md` during the live run.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/057-challenge-request-validity-scn010-live-micro/`

## Conclusions

Do not promote `candidate-challenge-request-validity-v1`. Candidate produced the
cleaner response by avoiding a blocked ticket, but current 10x already preserved
the target safety behavior: it challenged the requested solution, cited active
records, and avoided source/dependency changes. The improvement is record
economy rather than the requested challenge-request-validity behavior.
