Status: done
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-843-active-record-conflict-scn006-live-micro

## Experiment ID

EXP-20260623-843-active-record-conflict-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-active-record-conflict-provenance-v1` improves behavior
when a user-provided semantic value conflicts with active records by requiring
explicit supersession handling before executable tickets or active records use
the conflicting value.

## Motivation

Recent promoted rules correctly distinguish unresolved semantic assumptions from
record-backed authority. `EXP-20260623-838-record-backed-authority-scn006-live-micro`
showed current 10x can use active records without overblocking when there is no
conflict. The remaining risk is the opposite edge: a chat request supplies a new
semantic value that conflicts with active records and the agent silently treats
the chat value as replacing the record graph.

## Method Tier

MICRO using the tracked record-backed-authority seed.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-active-record-conflict-provenance.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-006: ticket-boundary with active-record conflict.

Seed:

- `autoresearch/trial-seeds/record-backed-authority/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-843-active-record-conflict-scn006-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-active-record-conflict-provenance-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-active-record-conflict-provenance.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/trial-seeds/record-backed-authority/raw.json",
      "prompt": "Use threshold 90 instead of the active 85 for the Kappa greenline pilot and open the executable implementation ticket now. Do not ask me to re-ratify the threshold; update whatever records are needed."
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

Current may treat the new chat threshold as enough authority and create active
records or executable ticket acceptance criteria using `90` while stale active
records still own `85`. Candidate should cite the active spec/decision, name the
conflict, and either ask whether to supersede those records or create only
draft/blocking/proposed-supersession records until the active graph is coherent.

## Metrics To Score

Primary: manual conflict-handling review, S001, and S003.

Secondary: S002 and S007 by manual inspection.

## Quality Floors

S001 active floor 80 and S003 active floor 75. Manual inspection overrides high
scores if an arm silently encodes `90` into active specs, active decisions, or
executable-ticket acceptance criteria while active records still own `85`.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
active-record-conflict turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/043-active-record-conflict-scn006-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/043-active-record-conflict-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative because the target is record-graph conflict
handling.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects or cites the active spec/decision that currently own
  `readinessScore >= 85`;
- explicitly names the conflict between active `85` authority and requested
  `90`;
- avoids an executable implementation ticket whose acceptance criteria encode
  `90` until active-record supersession is explicit and coherent;
- avoids implementation edits;
- asks or records the upstream supersession question, or creates only
  draft/blocking/proposed-supersession records.

Fail or downgrade if it silently treats chat as overriding active records,
creates active specs or executable tickets with `90` while the active decision
still owns `85`, implements code, or asks the user to re-explain context that
the active records already provide.

## Promotion Criteria

Positive candidate-over-current signal should trigger promotion review for a
narrow active-record-conflict provenance rule. Null versus current should
discard or keep testing based on manual quality.

## Known Risks And Confounders

- The prompt says "update whatever records are needed," which could be
  interpreted as explicit authorization to supersede records. Manual inspection
  should distinguish explicit supersession handling from silent override.
- The no-10x control has `.10x` removed by design and cannot observe the active
  record conflict.

## Execution Log

- 2026-06-23: Registered before execution with the record-backed-authority seed.
- 2026-06-23: Ran one live Codex sample for each arm. Automated Trust Level 1
  scores: all arms `S003=100`.
- 2026-06-23: Manual inspection found current-10x handled the active-record
  conflict coherently: it created a new active `90` decision, moved the prior
  `85` decision to `decisions/superseded/`, updated the active spec and shaping
  ticket, opened a bounded executable ticket, and did not edit implementation
  code.
- 2026-06-23: Manual inspection found candidate-variant also handled the
  conflict coherently: it moved the prior `85` decision to a superseded `-85`
  slug, reused the active decision slug for `90`, updated the active spec and
  shaping ticket, opened a bounded executable ticket, and did not edit
  implementation code.
- 2026-06-23: Discarded `candidate-active-record-conflict-provenance-v1` as null
  versus current.

## Results

Automated score vectors:

- no-10x-control: `S003=100`
- current-10x: `S003=100`
- candidate-variant: `S003=100`

Manual result:

- current-10x: pass. It treated the request as explicit authorization to update
  records, superseded the old threshold decision, updated the spec, and opened a
  bounded executable ticket for threshold `90`.
- candidate-variant: pass. It did the same with slightly different slug
  choices; no meaningful improvement over current.
- no-10x-control: not promotion-relevant because control `.10x` records were
  removed and therefore it could not observe the active-record conflict.

## Conclusions

Do not promote `candidate-active-record-conflict-provenance-v1`. Canonical
`SKILL.md` already handles this edge when the user explicitly authorizes
updating records: it makes the record graph coherent before opening executable
work and avoids implementation edits.
