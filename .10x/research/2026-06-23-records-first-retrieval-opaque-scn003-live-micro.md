Status: done
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-829-records-first-retrieval-opaque-scn003-live-micro

## Experiment ID

EXP-20260623-829-records-first-retrieval-opaque-scn003-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-records-first-retrieval-v1` improves SCN-003 behavior on
an opaque seed where exact arbitrary tokens and phrases can only come from
reading `.10x` records.

## Motivation

`EXP-20260623-828` was confounded because checkout retry behavior was too
guessable after the no-10x control removed `.10x`. This run keeps the fresh seed
structure but uses opaque exact content: `PAX-17-HALCYON`, `halcyon-blue`, and a
required sentinel copy string.

## Method Tier

MICRO continuation with a tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-records-first-retrieval.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root, `--disable
plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-003: existing-records-answer-the-question.

Seed:

- `autoresearch/trial-seeds/records-first-opaque/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-829-records-first-retrieval-opaque-scn003-live-micro",
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
      "prior_raw_path": "autoresearch/trial-seeds/records-first-opaque/raw.json",
      "prompt": "Using only records already in this workspace, answer three questions: what is the settled release token, what exact sentinel behavior applies to Kappa amber-hold orders, and which next implementation ticket owns it? Do not ask me to restate context already in records."
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

Codex CLI live subject runner with tracked seed workspace and explicit
instruction injection per arm.

## Scenario And Workspace Procedure

The runner copies the tracked seed workspace into a private temporary execution
workspace, suppresses inherited control instructions/record graph as applicable,
injects the scenario prompt, captures raw transcripts and command metadata, then
archives the completed workspace under this experiment's output directory.

## Repetition Count

One repetition per arm.

## Prediction

Candidate should answer with the exact release token `PAX-17-HALCYON`, exact
ledger note `halcyon-blue`, exact sentinel copy, and the open ticket path.
Current may also retrieve these records but may be less explicit about paths.
No-10x control should fail, state that the records are missing, or omit exact
opaque content because `.10x` is removed before execution.

Backfire: candidate invents a token, asks for restated context, or creates
duplicate records for the seeded context.

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
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/029-records-first-retrieval-opaque-scn003-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/029-records-first-retrieval-opaque-scn003-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required because retrieval quality and exact opaque content are not
fully represented by automated scores.

## Manual Inspection Requirement

Inspect combined transcripts, file outputs, seed/archive workspace manifests,
and report.

## Promotion Criteria

No promotion from this single MICRO without manual inspection and review. If the
candidate beats current and control on exact opaque retrieval, open a narrow
promotion review for records-first retrieval.

## Known Risks And Confounders

- The seed workspace is synthetic, not a full app repo.
- Automated S002 may remain conservative for retrieval continuations.
- One sample cannot distinguish stable retrieval discipline from stochastic
  response style.

## Execution Log

- 2026-06-23: Registered before execution with tracked opaque seed fixture.
- 2026-06-23: Ran live. Automated score vector:
  `candidate:S001=70,S002=50,S007=10 current:S001=70,S002=50,S007=10 control:S001=70,S002=70,S007=10`.
- 2026-06-23: Canonical guard reported `unchanged_during_run: true`.
- 2026-06-23: Manual inspection found candidate and current both retrieved the
  exact opaque token `PAX-17-HALCYON`, ledger note `halcyon-blue`, sentinel
  copy, and owning ticket path from seeded `.10x` records.
- 2026-06-23: Manual inspection found no-10x control removed inherited `.10x`
  before execution and correctly reported that the records were absent.
- 2026-06-23: Regenerated report with campaign metadata and appended
  `results.tsv` with status `review`.

## Score Artifacts

- report:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/029-records-first-retrieval-opaque-scn003-live-micro/report.md`
- campaign:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/029-records-first-retrieval-opaque-scn003-live-micro/campaign.json`
- canonical guard:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/029-records-first-retrieval-opaque-scn003-live-micro/canonical_guard.json`
- candidate score:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/029-records-first-retrieval-opaque-scn003-live-micro/scores/sha256-894b390a0db048453683289dfc8be2069c566cdf9fddb9c724ccc462c56c3481.score.json`
- current score:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/029-records-first-retrieval-opaque-scn003-live-micro/scores/sha256-633f5a085b2c6f152930b641c90576c243daeec4bfe49926a892842904985999.score.json`
- control score:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/029-records-first-retrieval-opaque-scn003-live-micro/scores/sha256-c5f9a7873efeb294780913b4b51212dfbe89da7dab4aa9097d76267645a44ae5.score.json`

## Manual Inspection Findings

- Candidate answered from `.10x` records and cited:
  `.10x/decisions/orion-release-token.md`,
  `.10x/specs/kappa-amber-hold-sentinel.md`, and
  `.10x/tickets/2026-06-23-add-kappa-amber-hold-sentinel.md`.
- Current also retrieved and cited the same record set, using absolute temporary
  workspace links.
- Candidate and current both included the exact opaque token, exact ledger note,
  exact sentinel copy, and owning ticket.
- No-10x control had `.10x` removed before execution, created no files, and did
  not invent the opaque facts. It reported that only `workspace-manifest.json`
  existed and that no `.10x` records were available.
- Automated S002 incorrectly treated seeded record files as duplicate records.
  Workspace manifests showed no extra files beyond the seeded `.10x` records for
  current and candidate.

## Final Verdict

Review/keep-testing. This is a valid discriminator proving 10x record retrieval
against an isolated no-10x control, but it is neutral on the candidate overlay
because current 10x matched candidate on the opaque seed. Aggregate promotion
review must weigh this tie against EXP-826 and EXP-827, where candidate was
clearer than current.
