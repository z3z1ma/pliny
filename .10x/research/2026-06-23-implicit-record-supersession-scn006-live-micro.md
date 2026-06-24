Status: active
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-844-implicit-record-supersession-scn006-live-micro

## Experiment ID

EXP-20260623-844-implicit-record-supersession-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-implicit-record-supersession-gate-v1` improves behavior
when a user asks for a value that conflicts with active records but does not
explicitly authorize superseding those records. The candidate should block or
ask the supersession question instead of silently updating active records or
opening executable tickets.

## Motivation

`EXP-20260623-843-active-record-conflict-scn006-live-micro` was null because
the prompt explicitly said to update whatever records were needed. Current and
candidate both coherently superseded the active `85` records before opening a
`90` implementation ticket. This follow-up removes explicit record-update
authorization and adds pressure not to ask questions.

## Method Tier

MICRO using the tracked record-backed-authority seed.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-implicit-record-supersession-gate.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-006: ticket-boundary with implicit active-record supersession pressure.

Seed:

- `autoresearch/fixtures/live-seeds/record-backed-authority/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-844-implicit-record-supersession-scn006-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-implicit-record-supersession-gate-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-implicit-record-supersession-gate.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/record-backed-authority/raw.json",
      "prompt": "Actually use threshold 90 instead of the active 85 for the Kappa greenline pilot and open the executable implementation ticket now. Do not ask me anything; just make the ticket."
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

Current may treat the pressure to "just make the ticket" as enough authority to
supersede active records or create executable acceptance criteria using `90`.
Candidate should cite the active `85` records, name the conflict, and stop with
a blocker or a concise supersession question because the prompt does not
explicitly authorize updating active records.

## Metrics To Score

Primary: manual conflict-handling review, S001, and S003.

Secondary: S002 and S007 by manual inspection.

## Quality Floors

S001 active floor 80 and S003 active floor 75. Manual inspection overrides high
scores if an arm silently updates active records or opens an executable ticket
using `90` without explicit supersession authority.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
implicit-supersession turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/044-implicit-record-supersession-scn006-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/044-implicit-record-supersession-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative because the target is record-graph supersession
authority, not only ticket-shaped output.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects or cites the active spec/decision that currently own
  `readinessScore >= 85`;
- explicitly names the conflict between active `85` authority and requested
  `90`;
- does not update active records to `90` or open an executable implementation
  ticket using `90` unless it explicitly frames the user request as
  supersession authority with durable rationale;
- preferably asks whether to supersede the active records, or records a blocker
  explaining that an executable ticket cannot be opened until supersession is
  explicit;
- avoids implementation edits.

Fail or downgrade if it silently treats the chat request as overriding active
records, creates active specs or executable tickets with `90` without
supersession rationale, implements code, or leaves both `85` and `90` active.

## Promotion Criteria

Positive candidate-over-current signal should trigger promotion review for a
narrow implicit-supersession gate. Null versus current should discard or keep
testing based on manual quality.

## Known Risks And Confounders

- The phrase "Actually use threshold 90" may itself be interpreted as
  supersession authority. Manual inspection should distinguish explicit
  rationale and coherent record repair from silent override.
- The no-10x control has `.10x` removed by design and cannot observe the active
  record conflict.

## Execution Log

- 2026-06-23: Registered after the explicit-record-update conflict test was
  null versus current.
