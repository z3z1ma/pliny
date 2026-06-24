Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-886-mechanical-default-action-gate-scn006-live-micro

## Experiment ID

EXP-20260624-886-mechanical-default-action-gate-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-mechanical-default-action-gate-v1` improves ticket
readiness behavior when behavior is settled and the only missing details are
mechanical artifact choices such as ticket filename and title.

## Motivation

Recent promoted mutations strongly protect against unratified semantic
assumptions. This MICRO checks the complementary risk: agents should not turn
that strictness into needless user interrogation when the remaining choice is a
repo-conventional artifact default, not product behavior.

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
  user asks for one executable child ticket and leaves title/filename/placement
  to repo convention.

Seed:

- `autoresearch/fixtures/live-seeds/ticket-readiness-real-source/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-886-mechanical-default-action-gate-scn006-live-micro",
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
      "prior_raw_path": "autoresearch/fixtures/live-seeds/ticket-readiness-real-source/raw.json",
      "prompt": "We approved the enterprise billing exceptions CSV export slice. Prepare execution for a subagent, but do not implement. Use the active records and source as authority. Behavior, scope, non-goals, acceptance criteria, and verification are already settled there. I do not care what the ticket filename or title is; use repo conventions for those mechanical details. Create the one executable 10x child ticket a subagent should execute, and do not ask me naming or placement questions."
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

Control may implement directly or create an underspecified note. Current may
already create the ticket correctly due the ticket-readiness gate. Candidate
should create one bounded executable child ticket, use repo-conventional naming
and placement, avoid semantic questions, and avoid implementation.

## Metrics To Score

Primary: S003 and manual mechanical-default inspection. Supporting: S005 and
S007.

## Quality Floors

S003 active floor 75. Manual inspection is authoritative for whether any
"default" chosen was mechanical rather than semantic.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one ticket
creation turn unless a subject asks a material question that requires a
continuation.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/086-mechanical-default-action-gate-scn006-live-micro/`;
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

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/086-mechanical-default-action-gate-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is required because the target behavior is differentiating mechanical
defaults from semantic defaults.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects the active enterprise billing CSV export decision/spec/source;
- creates exactly one bounded executable child ticket;
- includes scope, explicit exclusions, acceptance criteria, evidence
  expectations, and references;
- chooses ticket filename/title/placement from repo convention without asking;
- makes no implementation source/test edits;
- does not invent product behavior beyond active records.

Fail or downgrade if it asks naming/placement questions, blocks on mechanical
details, creates an underspecified ticket, writes implementation code, or treats
a product behavior as a mechanical default.

## Promotion Rule

Promote only if candidate materially improves over current on mechanical-default
decisiveness without weakening ticket quality or semantic-default discipline.

## Risks

- Current canonical may already pass because the ticket-readiness gate is strong.
- Automated S003 may miss mechanical-default over-questioning.
- The prompt explicitly says naming is mechanical, so future variants may need a
  subtler prompt if this nulls out.

## Execution Log

- 2026-06-24: Registered after `candidate-no-ticket-ratification-checkpoint-v1`
  promotion to test the complementary positive action rule for mechanical
  defaults.
- 2026-06-24: Ran live with `run_once.py` using `--require-clean-canonical`.
  Canonical guard reported no `SKILL.md` or `autoresearch/program.md` changes
  during the run.
- 2026-06-24: Logged `keep` in untracked `results.tsv`. Candidate remains
  experimental pending a subtler follow-up or ablation.

## Results

Artifacts:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/086-mechanical-default-action-gate-scn006-live-micro/summary.json`
- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/086-mechanical-default-action-gate-scn006-live-micro/report.md`
- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/086-mechanical-default-action-gate-scn006-live-micro/canonical_guard.json`

Score vector:

- no-10x-control: `S003=100`
- current-10x: `S003=85`
- candidate-variant: `S003=100`

Manual inspection:

- no-10x-control created one ticket despite having inherited `.10x` removed,
  but its ticket stated no active `.10x` records existed and relied on source
  only.
- current-10x created exactly one executable child ticket, made no
  implementation edits, preserved active spec/decision references, and asked no
  mechanical naming or placement questions.
- candidate-variant created exactly one executable child ticket, made no
  implementation edits, preserved active spec/decision dependencies, included
  explicit exclusions and evidence expectations, and recorded that filename and
  title were mechanical repo-conventional defaults rather than semantic choices.

## Conclusions

Keep `candidate-mechanical-default-action-gate-v1` for follow-up, but do not
promote yet.

The candidate improved the measured ticket shape and had lower wall time/tool
count than current, but the prompt explicitly named filename/title as mechanical
details. The result supports the hypothesis that positive mechanical-default
guidance may improve ticket quality, but does not yet prove the instruction is
needed when the model must infer the mechanical/semantic boundary itself.

Next useful test: a subtler SCN-006 or SCN-005 prompt where records/source imply
the remaining default is mechanical, but the user does not label it as such.
Promotion should require candidate-over-current improvement there without any
semantic default leakage.
