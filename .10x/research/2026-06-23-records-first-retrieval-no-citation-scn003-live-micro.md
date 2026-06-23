Status: done
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-827-records-first-retrieval-no-citation-scn003-live-micro

## Experiment ID

EXP-20260623-827-records-first-retrieval-no-citation-scn003-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-records-first-retrieval-v1` improves SCN-003 retrieval
even when the user does not explicitly ask for record-path citations, by
answering from `.10x` records and making the source record paths visible.

## Motivation

`EXP-20260623-826-records-first-retrieval-scn003-live-micro` kept this
candidate for more testing, but the prompt explicitly requested cited record
paths. This follow-up removes that wording to test whether citation and
records-first behavior come from the overlay rather than the benchmark prompt.

## Method Tier

MICRO continuation. One record-retrieval turn seeded from the upstream-gated
continuation workspaces.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-records-first-retrieval.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, prior workspaces copied as
seeds but archived under this experiment's output root, `--disable plugins`, and
`--ignore-user-config`.

## Scenario Set

- SCN-003: existing-records-answer-the-question.

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-827-records-first-retrieval-no-citation-scn003-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-records-first-retrieval-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-records-first-retrieval.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-003",
      "prior_raw_paths": {
        "current-10x": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/017-upstream-gated-blockers-scn001-continuation-live-micro/raw/sha256-36251b36d7e4da0fcd428f70410d8262286c1fef66cc7d7b194e4a8ad003ebdc.json",
        "candidate-variant": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/017-upstream-gated-blockers-scn001-continuation-live-micro/raw/sha256-85b19f3399e5f04f32786d2d23bbf419648fd806d0fa15021ee2144d9fa6543f.json",
        "no-10x-control": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/017-upstream-gated-blockers-scn001-continuation-live-micro/raw/sha256-9486ee932a7b5d7d49ca3eabea7d5989540a587a48d591cd64391a0b2e48e29e.json"
      },
      "prompts_by_arm": {
        "current-10x": "Using the records already in this workspace, summarize the enterprise billing dashboard pricing-exception workflow we captured, the remaining blockers, and the next ticket. Do not ask me to restate context that is already in the records.",
        "candidate-variant": "Using the records already in this workspace, summarize the enterprise billing dashboard pricing-exception workflow we captured, the remaining blockers, and the next ticket. Do not ask me to restate context that is already in the records.",
        "no-10x-control": "Using the records already in this workspace, summarize the enterprise billing dashboard pricing-exception workflow we captured, the remaining blockers, and the next ticket. Do not ask me to restate context that is already in the records."
      }
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

Codex CLI live subject runner with generated workspaces, seed workspaces from
prior raw artifacts, and explicit instruction injection per arm.

## Scenario And Workspace Procedure

The runner copies the prior workspace into a private temporary execution
workspace, suppresses inherited control instructions/record graph as applicable,
injects the scenario prompt, captures raw transcripts and command metadata, then
archives the completed workspace under this experiment's output directory.

## Repetition Count

One repetition per arm.

## Prediction

Candidate should still cite or otherwise name the `.10x` records used and
separate record-backed facts from gaps. Current may answer from records but is
less likely to make the paths visible without prompt pressure.

Backfire: candidate adds citation theater, overtrusts stale records, or creates
duplicate records.

## Metrics To Score

Primary: S001, S002, and S007, with manual SCN-003 retrieval inspection.

## Quality Floors

S001 active floor 80. S002 active floor 80. S007 has no active floor but is a
manual shaping-quality target.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
retrieval turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/027-records-first-retrieval-no-citation-scn003-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/027-records-first-retrieval-no-citation-scn003-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required because retrieval quality and citation usefulness are not
fully represented by automated scores.

## Manual Inspection Requirement

Inspect combined transcripts, file outputs, seed/archive workspace manifests,
and report.

## Promotion Criteria

No promotion from this single MICRO. If this repeats the positive SCN-003
retrieval pattern, the next step is either a fresh-record SCN-003 seed or a
narrow canonical promotion review.

## Known Risks And Confounders

- The same seed records were used in EXP-826, so this is a prompt-ablation
  rather than a fresh-context generalization test.
- Automated S002 may remain conservative for retrieval continuations.
- One sample cannot distinguish stable retrieval discipline from stochastic
  response style.

## Execution Log

- 2026-06-23: Registered before execution.
- 2026-06-23: Ran live. Score vector:
  `candidate:S001=100,S002=60,S007=80 current:S001=100,S002=50,S007=60 control:S001=40,S002=50,S007=20`.
- 2026-06-23: Canonical guard reported `unchanged_during_run: true`.
- 2026-06-23: Manual inspection confirmed candidate named both source records
  without explicit citation wording in the prompt. Current answered from
  `.10x` records but was less explicit about the source set.
- 2026-06-23: Regenerated report with campaign metadata and appended
  `results.tsv` with status `keep`.

## Score Artifacts

- report:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/027-records-first-retrieval-no-citation-scn003-live-micro/report.md`
- campaign:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/027-records-first-retrieval-no-citation-scn003-live-micro/campaign.json`
- canonical guard:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/027-records-first-retrieval-no-citation-scn003-live-micro/canonical_guard.json`
- candidate score:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/027-records-first-retrieval-no-citation-scn003-live-micro/scores/sha256-f566bcafd2dcad32e57f3c792eaabea61c622cc38a925a69ef8bf9310fb089b9.score.json`
- current score:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/027-records-first-retrieval-no-citation-scn003-live-micro/scores/sha256-472f27ca7f5308146b73a48fa1fb57fb37dda70ada4741f422ef1e69ced2585f.score.json`
- control score:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/027-records-first-retrieval-no-citation-scn003-live-micro/scores/sha256-542f6d9b0afefddf52fc4bbac1954905661409f20cbb03624cacf9d53d0edfdd.score.json`

## Manual Inspection Findings

- Candidate named both records it used:
  `.10x/specs/enterprise-billing-dashboard-sales-validation.md` and
  `.10x/tickets/2026-06-23-shape-enterprise-billing-dashboard-improvements.md`.
- Candidate preserved blockers and did not ask the user to restate context.
- Current answered from `.10x` records and linked the next ticket but did not
  make the source record set as explicit.
- No-10x control answered from a non-`.10x` ad hoc record and again moved toward
  implementation-ticket scope.
- No new duplicate records were created by current or candidate.

## Final Verdict

Keep testing, not promoted. The prompt ablation supports that records-first path
citation came from the candidate overlay rather than explicit prompt wording.
Fresh-record retrieval is still needed before a promotion review.
