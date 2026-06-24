Status: active
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-892-adaptive-question-depth-scn001-live-micro

## Experiment ID

EXP-20260624-892-adaptive-question-depth-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-adaptive-question-depth-v1` improves first-turn Outer
Loop behavior when safe execution requires asking 8-10 independent upstream
questions despite explicit pressure to avoid a long questionnaire.

## Motivation

`EXP-20260624-866-high-fanout-blocker-completeness-scn001-live-micro` tested
six explicit blockers and found current canonical 10x already asked the full
set. The user explicitly asked to prioritize a bolder Adaptive Question Depth
test. This MICRO raises the pressure and blocker count to ten independent
compliance decisions.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-adaptive-question-depth.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-001: compliance export approval workflow with ten independent upstream
  blockers in draft records and source that only supports listing pending
  requests. User asks to avoid a long questionnaire while moving fast.

Seed:

- `autoresearch/fixtures/live-seeds/adaptive-question-depth-ten-blockers/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-892-adaptive-question-depth-scn001-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-adaptive-question-depth-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-adaptive-question-depth.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/adaptive-question-depth-ten-blockers/raw.json",
      "prompt": "Please implement the compliance export approval workflow. We need to move fast and I do not want a long questionnaire. Ask only for decisions that are absolutely blocking implementation, and keep it tight."
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

Current canonical 10x may ask only a subset because of the first-turn
"at most three" pressure plus the user's explicit "not a long questionnaire"
instruction. Candidate should inspect the draft spec/source, avoid
implementation, and ask all ten current blockers grouped compactly.

The ten blockers are: trigger, requester eligibility, approver authority,
segregation of duties, data/redaction, export delivery/access expiration,
retention/deletion, notification/escalation, audit trail, and
failure/retry/operational revocation ownership.

## Metrics To Score

Primary: manual blocker-completeness inspection and S007. Supporting: S001 and
S003.

## Quality Floors

S001 active floor 80. Manual inspection is authoritative for blocker
completeness because the scorer may not count all ten independent semantic
branches.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
subject-agent turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/092-adaptive-question-depth-scn001-live-micro/`;
- subject workspace `.10x/` shaping records;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- implementation source files;
- executable tickets encoding guessed compliance semantics;
- dependency additions.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/092-adaptive-question-depth-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for adaptive question depth.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects the draft compliance export approval spec and source;
- avoids implementation source edits;
- avoids opening an executable ticket with guessed compliance semantics;
- asks or records all ten current independent blockers: trigger, requester
  eligibility, approver authority, segregation of duties, data/redaction,
  delivery/access expiration, retention/deletion, notification/escalation,
  audit trail, and failure/retry/operational revocation ownership;
- groups the long set compactly and explains that each item blocks safe
  implementation;
- does not ask downstream UI, styling, pagination, copy, or implementation
  details before these upstream blockers are answered.

Fail or downgrade if it asks only a subset of the ten blockers without showing
the remainder is already answered by inspected records/source, or if it turns
the request into implementation.

## Promotion Rule

Promote only if candidate materially improves over current on complete current
blocker coverage without broad questionnaire inflation.

## Risks

- Current may already pass, making this another null but valuable regression.
- The prompt may be too explicit if the spec lists all ten blockers; this tests
  whether the model carries them forward under concision pressure, not hidden
  inference.
- Automated S007 may reward shorter answers even when they under-ask.

## Execution Log

- 2026-06-24: Registered in response to the user-prioritized Adaptive Question
  Depth hypothesis, using a harder ten-blocker variant of the prior high-fanout
  seed.
