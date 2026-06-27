Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-887-mechanical-default-action-gate-subtle-scn006-live-micro

## Experiment ID

EXP-20260624-887-mechanical-default-action-gate-subtle-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-mechanical-default-action-gate-v1` improves ticket
readiness when the model must infer that remaining ticket title/filename choices
are mechanical from repository convention, without the user explicitly naming
them as mechanical.

## Motivation

`EXP-20260624-886-mechanical-default-action-gate-scn006-live-micro` produced a
weak keep: candidate scored higher and named mechanical defaults, but the prompt
itself labeled filename/title as mechanical. This follow-up removes that label.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-mechanical-default-action-gate.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-006: active enterprise billing CSV export records and source establish the
  behavior, scope, non-goals, acceptance criteria, and verification path. The
  user asks for one executable child ticket without specifying title or
  filename.

Seed:

- `autoresearch/trial-seeds/ticket-readiness-real-source/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-887-mechanical-default-action-gate-subtle-scn006-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-mechanical-default-action-gate-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-mechanical-default-action-gate.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/trial-seeds/ticket-readiness-real-source/raw.json",
      "prompt": "We approved the enterprise billing exceptions CSV export slice. Prepare execution for a subagent, but do not implement. Use the active records and source as authority. Behavior, scope, non-goals, acceptance criteria, and verification are already settled there. Create the one executable 10x child ticket a subagent should execute."
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

Current may already create a high-quality ticket from the promoted
ticket-readiness gate. Candidate should only be promoted if it improves the
mechanical-default boundary or ticket quality without adding semantic defaults.

## Metrics To Score

Primary: S003 and manual ticket/default-boundary inspection. Supporting: S005
and S007 if scorer emits them.

## Quality Floors

S003 active floor 75. Manual inspection is authoritative for whether the
candidate adds meaningful behavior beyond current.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one ticket
creation turn unless a subject asks a material question that requires a
continuation.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/087-mechanical-default-action-gate-subtle-scn006-live-micro/`;
- subject workspace `.10x/tickets/` child ticket created by the subject;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace implementation source/test files;
- tickets that encode unratified product behavior beyond active records.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/087-mechanical-default-action-gate-subtle-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is required because ticket naming/default boundary quality is not
fully captured by S003.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects the active enterprise billing CSV export decision/spec/source;
- creates exactly one bounded executable child ticket;
- includes scope, explicit exclusions, acceptance criteria, evidence
  expectations, and references;
- chooses ticket filename/title/placement from repo convention without asking;
- makes no implementation source/test edits;
- does not invent product behavior beyond active records.

Promotion requires candidate-over-current improvement, not merely passing.

## Promotion Rule

Promote only if candidate materially improves over current on ticket/default
quality without prompt-explicit mechanical language. Discard if current already
proceeds with comparable ticket quality or if candidate leaks semantic defaults.

## Risks

- Current canonical may already pass, proving the overlay redundant.
- Automated S003 may reward wording rather than meaningful behavior.
- This still uses the same seed as the first mechanical-default run, so a null
  result should discard or substantially mutate the candidate.

## Execution Log

- 2026-06-24: Registered as the follow-up required by
  `EXP-20260624-886-mechanical-default-action-gate-scn006-live-micro`.
- 2026-06-24: Ran live with `run_once.py` using `--require-clean-canonical`.
  Canonical guard reported no `SKILL.md` or `autoresearch/program.md` changes
  during the run.
- 2026-06-24: Logged `discard` in untracked `results.tsv` and marked
  `candidate-mechanical-default-action-gate-v1` discarded.

## Results

Artifacts:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/087-mechanical-default-action-gate-subtle-scn006-live-micro/summary.json`
- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/087-mechanical-default-action-gate-subtle-scn006-live-micro/report.md`
- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/087-mechanical-default-action-gate-subtle-scn006-live-micro/canonical_guard.json`

Score vector:

- no-10x-control: `S003=100`
- current-10x: `S003=85`
- candidate-variant: `S003=65`, below the active S003 floor

Manual inspection:

- no-10x-control created a broad but executable ticket from source-only context
  because inherited `.10x` records were removed for control isolation.
- current-10x created one executable child ticket, made no implementation edits,
  referenced the active spec/decision, included explicit exclusions, acceptance
  criteria, verification expectations, governing records, source context,
  assumption provenance, and `Blockers: None`.
- candidate-variant created one executable child ticket, made no implementation
  edits, referenced the active spec/decision, and included the mechanical
  filename/title default, but its ticket was thinner than current on source
  context and provenance.

## Conclusions

Discard `candidate-mechanical-default-action-gate-v1`.

The follow-up removed the prompt-explicit mechanical wording and the candidate
regressed below the S003 floor. The useful part of the candidate, naming
filename/title as mechanical, did not compensate for weaker overall ticket
quality. Current canonical 10x already proceeds decisively on this ticket
readiness surface without asking mechanical questions, so adding another
mechanical-default paragraph would increase instruction bulk without a proven
behavioral gain.
