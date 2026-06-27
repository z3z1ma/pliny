Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-860-invalid-request-no-ticket-economy-scn010-live-micro

## Experiment ID

EXP-20260624-860-invalid-request-no-ticket-economy-scn010-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-invalid-request-no-ticket-economy-v1` improves record
economy when active records/source already prove the requested implementation is
invalid and the current turn adds no new durable work.

## Motivation

EXP-857 showed current 10x correctly challenged an invalid client-side CSV
framework request, but current opened a blocked ticket to preserve the conflict
while candidate answered from existing authority with no new records. This MICRO
isolates that narrower record-economy behavior.

## Method Tier

MICRO using a tracked invalid-request/no-ticket-economy seed.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-invalid-request-no-ticket-economy.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-010: active records reject client-side report CSV generation, source
  already exposes `reportExportUrl(filters)`, and the user asks for the planning
  record or implementation ticket for a client-side CSV framework.

Seed:

- `autoresearch/trial-seeds/invalid-request-no-ticket-economy/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-860-invalid-request-no-ticket-economy-scn010-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-invalid-request-no-ticket-economy-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-invalid-request-no-ticket-economy.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-010",
      "prior_raw_path": "autoresearch/trial-seeds/invalid-request-no-ticket-economy/raw.json",
      "prompt": "Add the planning record needed for a reusable client-side CSV export framework for the Reports dashboard so filtered results export correctly. Use PapaParse or a similar dependency later if needed. Do not edit source code. Do not ask questions; open the implementation ticket if you need a ticket first."
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

Current may open a blocked ticket despite existing active records/source already
owning the rejection. Candidate should cite the existing authority, recommend
`reportExportUrl(filters)` / `/api/reports/export.csv`, create no records, and
avoid source/dependency edits.

## Metrics To Score

Primary: manual record-economy inspection, S002, with S005 and S007 as
supporting signals.

## Quality Floors

S005 active floor 75. Manual inspection is authoritative for redundant-record
economy.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
request-validity/no-ticket-economy turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/060-invalid-request-no-ticket-economy-scn010-live-micro/`;
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

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/060-invalid-request-no-ticket-economy-scn010-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for redundant-record economy.

## Manual Inspection Requirement

Pass an arm only if it:

- reads the active decision/knowledge and `src/reports/exportUrl.js`;
- states the client-side CSV framework request conflicts with server-owned
  report export authority;
- recommends the smaller valid path: use `reportExportUrl(filters)` and
  `/api/reports/export.csv`;
- creates no new `.10x` record when the current turn adds no new durable fact or
  actionable work;
- makes no source or dependency edits.

Fail if it opens a blocked ticket solely to preserve the already-owned invalid
request, opens an executable implementation ticket, duplicates existing durable
authority, edits source, adds a CSV dependency, or rejects the request without
citing inspected authority.

## Promotion Criteria

Positive candidate-over-current signal should trigger promotion review for a
narrow invalid-request no-ticket-economy rule. Null versus current should
discard.

## Known Risks And Confounders

- The prompt explicitly asks for a planning record, which may pressure compliant
  agents toward unnecessary record creation.
- A no-record answer is correct only because the turn adds no distinct durable
  requirement, supersession intent, defect, missing wiring, or approved
  follow-up.
- The no-10x control has inherited `.10x` removed, but source still exposes the
  server export URL helper.

## Execution Log

- 2026-06-24: Registered after EXP-859 promotion to test the queued record
  economy hypothesis from EXP-857.
- 2026-06-24: Ran the experiment with one live Codex sample per arm. Manual
  inspection found current-10x opened a redundant blocked ticket while the
  candidate answered from existing authority and created no record.

## Results

Automated Trust Level 1 score vectors:

- candidate-variant: `S005=95`, `S007=10`
- current-10x: `S005=95`, `S007=25`
- no-10x-control: `S005=100`, `S007=25`

The automated scorer did not emit S002 for this SCN-010 run, so manual
record-economy inspection is authoritative.

Manual inspection:

- candidate-variant read the active decision, knowledge record, and source
  helper; cited the conflict; recommended the existing server export URL path;
  and created no new `.10x` record.
- current-10x read the same authority but opened
  `.10x/tickets/2026-06-24-plan-client-side-csv-export-framework.md` as a
  blocked ticket solely to preserve the already-owned rejected request.
- no-10x-control had inherited `.10x` removed by control isolation and created a
  speculative client-side CSV planning ticket.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/060-invalid-request-no-ticket-economy-scn010-live-micro/`

## Conclusions

Promote `candidate-invalid-request-no-ticket-economy-v1` narrowly. The winning
behavior is not "under-record more"; it is "do not create a blocked memorial
ticket for an invalid or redundant request already owned by active records or
source when the current turn adds no distinct durable work."
