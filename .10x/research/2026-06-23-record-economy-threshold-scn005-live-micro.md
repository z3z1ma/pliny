Status: done
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-822-record-economy-threshold-scn005-live-micro

## Experiment ID

EXP-20260623-822-record-economy-threshold-scn005-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-record-economy-threshold-v1` improves record minimalism
on SCN-005 by preserving a lightweight durable convention in one coherent
record owner instead of creating a multi-record spread or placeholder ticket.

## Motivation

Canonical `SKILL.md` strongly requires durable context and autonomous follow-up
ticket creation. That is useful, but it may overproduce records when a small
convention or observation only needs one owner. The candidate adds a threshold
for deciding whether to create a new record, update an existing owner, or leave
a progress note.

## Method Tier

MICRO. One narrow SCN-005 live record-spam prompt.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-record-economy-threshold.md`.

## Control

Generated archived workspaces, per-sample private temporary execution
workspaces, suppressed project instruction paths, `--disable plugins`, and
`--ignore-user-config`.

## Scenario Set

- SCN-005: record-spam-trap.

Live prompt:

```text
We are not implementing anything right now.

Please preserve this lightweight convention for future billing-dashboard work:
small table CSV exports should stay client-side and reuse existing button/download patterns. Do not add backend export endpoints unless product explicitly requires server-generated exports.

There is no active feature ticket yet. Capture the durable context in the right `.10x` place so a future agent does not overbuild export work.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-822-record-economy-threshold-scn005-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-record-economy-threshold-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-record-economy-threshold.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-005",
      "prompt": "We are not implementing anything right now.\n\nPlease preserve this lightweight convention for future billing-dashboard work: small table CSV exports should stay client-side and reuse existing button/download patterns. Do not add backend export endpoints unless product explicitly requires server-generated exports.\n\nThere is no active feature ticket yet. Capture the durable context in the right `.10x` place so a future agent does not overbuild export work."
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

## Subject Agent And Model

Codex CLI default model as configured by the local subscription-backed harness.

## Harness Target

Codex CLI live subject runner with generated workspaces and explicit instruction
injection per arm.

## Scenario And Workspace Procedure

The runner executes each subject in a private temporary workspace, suppresses
project-level instruction files, injects the scenario prompt, captures raw
transcripts and command metadata, then archives the completed workspace under
the configured output directory for inspection.

## Repetition Count

One repetition per arm.

## Prediction

Candidate should create at most one focused knowledge or decision record and
avoid tickets, specs, evidence records, and placeholder parent plans. Current
10x may also pass, but is more exposed to the "if worth mentioning, worth
tracking" and "externalize context" pressure.

## Metrics To Score

Primary: S002 and S005, with manual record-count and record-owner inspection.

## Quality Floors

S002 active floor 80. S005 active floor 75.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one first
turn unless transcript inspection shows a continuation is necessary.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/022-record-economy-threshold-scn005-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/022-record-economy-threshold-scn005-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for record-count and record-owner quality.

## Manual Inspection Requirement

Inspect all raw transcripts, file outputs, workspace manifests, and report.

## Promotion Criteria

No promotion from this single MICRO. A promotion would require repeated live
evidence, manual inspection, review, and explicit human approval.

## Known Risks And Confounders

- A no-10x control may follow the prompt's "lightweight" wording without record
  graph discipline.
- Current `SKILL.md` may already choose a single knowledge record.
- One sample cannot distinguish stochastic record economy from candidate effect.

## Execution Log

- 2026-06-23: Registered before execution.
- 2026-06-23: Live run completed with score vector
  `candidate:S002=65,S005=80 current:S002=65,S005=80 control:S002=65,S005=80`.
- 2026-06-23: Generated report at
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/022-record-economy-threshold-scn005-live-micro/report.md`
  and canonical guard at
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/022-record-economy-threshold-scn005-live-micro/canonical_guard.json`.
- 2026-06-23: Manual inspection found all three arms created exactly one
  knowledge record. The prompt was too easy to discriminate the candidate.

## Score Artifacts

- no-10x-control:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/022-record-economy-threshold-scn005-live-micro/scores/sha256-e915269a3cc257dd698af9bce08996b454e71e170861b027de619bccc95bdbc4.score.json`
  scored `S002=65`, `S005=80`.
- current-10x:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/022-record-economy-threshold-scn005-live-micro/scores/sha256-04ff5a823c11ca560f2f26b4c196e0bc85c444a2fa1f0567be271161bdc3a28d.score.json`
  scored `S002=65`, `S005=80`.
- candidate-variant:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/022-record-economy-threshold-scn005-live-micro/scores/sha256-70611509ed503507e0029db22c28a9a4132200ee951499431151a189a6cd9d05.score.json`
  scored `S002=65`, `S005=80`.

## Manual Inspection Findings

- no-10x-control created one knowledge record:
  `.10x/knowledge/billing-dashboard-csv-exports.md`.
- current-10x created one knowledge record:
  `.10x/knowledge/billing-dashboard-csv-export-convention.md`.
- candidate-variant created one knowledge record:
  `.10x/knowledge/billing-dashboard-csv-export-convention.md`.
- Candidate wording was slightly more precise about applicability limits, but
  current and control both avoided record spread. This run does not test the
  candidate's threshold under meaningful pressure.
- The S002 floor failures are scorer-conservative: manual inspection found the
  record count and record type directionally appropriate for the prompt.

## Final Verdict

Null and weak discriminator. Do not promote
`candidate-record-economy-threshold-v1` from this run. The candidate may still
be worth testing against a harder SCN-005 prompt that tempts the agent to create
decision/spec/ticket/evidence spread, but this prompt only proves the simple
case is already handled by current 10x and even by the no-10x control.
