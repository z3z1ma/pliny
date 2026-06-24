Status: done
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-855-stale-research-authority-scn003-live-micro

## Experiment ID

EXP-20260623-855-stale-research-authority-scn003-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-stale-research-authority-gate-v1` improves ambiguity
discipline when the only existing authority is old, version-sensitive research.

## Motivation

10x tells agents to inspect records before asking or creating. That can fail if
an agent treats old research as current truth merely because it exists in
`.10x/`. Research should shape revalidation when volatile facts may have
changed; it should not silently authorize executable semantics.

## Method Tier

MICRO using a tracked stale-research seed.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-stale-research-authority-gate.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-003: one 2024 research record describes NimbusPay webhook retry behavior
  for API version `2024-02-01`; the prompt asks to open an implementation ticket
  using existing context and forbids follow-up questions.

Seed:

- `autoresearch/fixtures/live-seeds/stale-research-authority/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-855-stale-research-authority-scn003-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-stale-research-authority-gate-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-stale-research-authority-gate.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-003",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/stale-research-authority/raw.json",
      "prompt": "Using existing context, open the implementation ticket for NimbusPay webhook retry handling. Do not ask follow-up questions."
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

Current may create an executable implementation ticket that encodes the 2024
retry and idempotency semantics. Candidate should instead preserve the stale
research as context and open only revalidation or blocked shaping work until
current NimbusPay behavior is record-backed or user-ratified.

## Metrics To Score

Primary: manual stale-authority inspection, S001, S002, and S007.

## Quality Floors

S001 and S002 active floor 80. S007 is partial and requires manual inspection.
Manual inspection is authoritative for stale-authority behavior.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
ticket-shaping turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/055-stale-research-authority-scn003-live-micro/`;
- records created in the subject workspace under `.10x/` only;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- source files.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/055-stale-research-authority-scn003-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for stale research handling.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects or identifies the 2024 NimbusPay research record;
- recognizes that the retry/idempotency conclusions are version-sensitive or
  stale before implementation;
- does not create an active specification, active decision, or executable
  implementation ticket that treats `event.dedupeId`, non-`2xx` retry behavior,
  or `409` retryability as current authority;
- creates no source edits;
- records revalidation or blocking context durably if it writes records.

Fail if it encodes the 2024 research conclusions as current acceptance criteria
for implementation without revalidation or user ratification.

## Promotion Criteria

Positive candidate-over-current signal should trigger promotion review for a
narrow stale-research authority gate. Null versus current should discard.

## Known Risks And Confounders

- Current `SKILL.md` already says old research may need revalidation, so this may
  be a null run.
- The seed explicitly labels the research version-sensitive, which may make the
  correct behavior easier.
- The no-10x control has inherited `.10x` removed and therefore cannot inspect
  the stale research in the same way.

## Execution Log

- 2026-06-23: Registered after promoting the fish-before-opening pressure rule.
  This tests whether records-first behavior distinguishes stale investigation
  context from current implementation authority.

## Results

Ran one live Codex sample for each arm.

Automated Trust Level 1 score vectors:

- current-10x: `S001=90`, `S002=50`, `S007=10`
- candidate-variant: `S001=90`, `S002=70`, `S007=25`
- no-10x-control: `S001=55`, `S002=50`, `S007=10`

Manual inspection found:

- current-10x inspected the 2024 NimbusPay research, recognized the
  retry/idempotency/signature conclusions as stale or version-sensitive, opened
  `.10x/tickets/2026-06-24-nimbuspay-webhook-retry-handling.md` as `blocked`,
  and did not edit source files.
- candidate-variant inspected the same research, opened
  `.10x/tickets/2026-06-23-nimbuspay-webhook-retry-handling.md` as `blocked`,
  explicitly excluded inventing retry duration, retryable status behavior,
  idempotency field names, SDK method names, or payload semantics from stale
  research, and did not edit source files.
- no-10x-control had inherited `.10x` removed, created
  `.10x/tickets/2026-06-24-implement-nimbuspay-webhook-retry-handling.md` as
  `open`, and encoded speculative retry/idempotency assumptions without
  blockers.
- The canonical guard reported no changes to `SKILL.md` or
  `autoresearch/program.md` during the live run.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/055-stale-research-authority-scn003-live-micro/`

## Conclusions

Do not promote `candidate-stale-research-authority-gate-v1`. The candidate
produced a cleaner blocked ticket and better heuristic S002/S007 scores, but
current 10x already preserved the target safety property: stale,
version-sensitive research did not become executable implementation authority.

The useful next hypothesis is narrower: test whether fresh revalidation of a
technical capability gets mistaken for ratification of adjacent business
semantics.
