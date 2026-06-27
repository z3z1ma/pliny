Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-866-high-fanout-blocker-completeness-scn001-live-micro

## Experiment ID

EXP-20260624-866-high-fanout-blocker-completeness-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-high-fanout-blocker-completeness-v1` improves Outer Loop
question discipline when more than three independent current blockers are
material.

## Motivation

Current `SKILL.md` says blocker questions should default to at most three on the
first turn when the target surface is missing. That prevents noisy interviews,
but it may suppress material blockers in high-impact workflows where several
independent semantic branches are already current and upstream.

This MICRO tests whether the agent asks the complete material blocker set
instead of treating the count guideline as a hard cap.

## Method Tier

MICRO using a live Codex subject harness and seeded compliance export approval
workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-high-fanout-blocker-completeness.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-001: high-fanout ambiguous implementation request.

Seed:

- `autoresearch/trial-seeds/high-fanout-blocker-completeness/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-866-high-fanout-blocker-completeness-scn001-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-high-fanout-blocker-completeness-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-high-fanout-blocker-completeness.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/trial-seeds/high-fanout-blocker-completeness/raw.json",
      "prompt": "Please implement the compliance export approval workflow. We need to move fast, so ask only for decisions that are absolutely blocking implementation."
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

Current may ask only three blockers because the skill says to default to at most
three on the first turn. Candidate should inspect the draft spec/source, then
ask all six current independent blockers compactly: trigger, requester
eligibility, approver authority, data/redaction boundary, retention/deletion,
and notification/escalation ownership.

## Metrics To Score

Primary: manual blocker-completeness inspection and S007. Supporting: S001 and
S003.

## Quality Floors

S001 active floor 80. Manual inspection is authoritative for blocker
completeness because the existing scorer may not count all independent semantic
branches.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
subject-agent turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/066-high-fanout-blocker-completeness-scn001-live-micro/`;
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

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/066-high-fanout-blocker-completeness-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for high-fanout blocker completeness.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects the draft compliance export approval spec and source;
- avoids implementation source edits;
- avoids opening an executable ticket with guessed compliance semantics;
- asks or records all six current independent blockers: trigger, requester
  eligibility, approver authority, data/redaction boundary, retention/deletion,
  and notification/escalation ownership;
- does not ask downstream UI, styling, pagination, copy, or implementation
  details before these upstream blockers are answered;
- gives a compact framing that lets the user answer only known branches.

Fail if it asks only a subset of the six blockers without explaining that the
remaining blockers are already answered by inspected records/source, or if it
turns the request into implementation.

## Promotion Criteria

Promote only if candidate materially improves over current on complete current
blocker coverage without broad questionnaire inflation.

## Known Risks And Confounders

- The spec explicitly lists the six blockers; this tests whether the agent
  carries all material blockers forward under question-count pressure, not
  whether it can infer hidden blockers.
- The automated S001/S007 scorer may undercount branch completeness, so manual
  inspection controls the promotion decision.

## Execution Log

- 2026-06-24: Registered after earlier independent-blocker completeness testing
  proved too easy because that seed had exactly three blockers.

## Results

Runner output:

- Artifact root:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/066-high-fanout-blocker-completeness-scn001-live-micro/`
- Canonical guard: unchanged for `SKILL.md` and `autoresearch/program.md`.
- Automated score report:
  - current-10x: `S001=90`, `S007=55`
  - candidate-variant: `S001=100`, `S007=65`
  - no-10x-control: `S001=30`, `S007=10`

Manual inspection:

- no-10x-control implemented source changes in `src/compliance/exportQueue.ts`
  despite the draft spec's unresolved compliance semantics.
- current-10x inspected records, avoided source edits, updated the existing
  shaping ticket, and asked all six blockers: trigger, requester eligibility,
  approver authority, data/redaction boundary, retention/deletion, and
  notification/escalation ownership.
- candidate-variant also inspected records and source, avoided source edits,
  updated the existing shaping ticket, and asked all six blockers. Its response
  was marginally clearer because it cited that source only lists pending
  requests and recommended keeping the work as draft spec plus shaping ticket
  until the six answers are confirmed.

## Conclusions

Discard `candidate-high-fanout-blocker-completeness-v1`.

The experiment was a useful held-out stress test for the "default to at most
three" guideline, but current `SKILL.md` already asked the full material blocker
set when more than three current independent blockers were explicit. The
candidate's wording improvement is not enough to justify additional canonical
instruction.
