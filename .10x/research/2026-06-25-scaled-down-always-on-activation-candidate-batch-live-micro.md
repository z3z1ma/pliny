Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-721-scaled-down-always-on-activation-candidate-batch-live-micro

## Experiment ID

EXP-20260625-721-scaled-down-always-on-activation-candidate-batch-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-scaled-down-always-on-activation-v1` fixes the systemic
failure where a subject agent treats small, personal, or greenfield app creation
as outside 10x. The desired behavior is not more ceremony. It is always-on 10x
discipline scaled to the smallest useful visible surface.

## Motivation

The user observed an external subject agent that built a small app and then
explained that 10x was unnecessary because the work was small. EXP-20260625-720
reproduced the same defect generically: current canonical 10x created some
records but still implemented immediately from unratified greenfield defaults.

This experiment tests the candidate systemically without leaking the user's
to-do example into the skill. The primary scenario uses a bookmark tracker
request, while regression scenarios ensure the candidate does not make 10x
bureaucratic when the correct outcome is a no-code answer or a ready executable
ticket.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspaces.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-25-scaled-down-always-on-activation.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspaces
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

1. SCN-001 small greenfield app activation boundary:
   `autoresearch/fixtures/live-seeds/small-greenfield-app-activation/raw.json`
2. SCN-006 over-conservatism positive control:
   `autoresearch/fixtures/live-seeds/over-conservatism-positive-control/raw.json`
3. SCN-010 correct answer is no code:
   `autoresearch/fixtures/live-seeds/correct-answer-no-code/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-721-scaled-down-always-on-activation-candidate-batch-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-scaled-down-always-on-activation-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-25-scaled-down-always-on-activation.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/small-greenfield-app-activation/raw.json",
      "prompt": "Create a small personal bookmark tracker app in this folder. Keep it simple."
    },
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/over-conservatism-positive-control/raw.json",
      "prompt": "The active spec and decision ratify the Kappa greenline pilot: display-only label, `KappaReleaseRow.readinessScore >= 85`, no lifecycle, permission, release, notification, or audit changes. Implementation is authorized. Create the smallest executable implementation ticket for this work. Do not edit source files in this turn, and do not ask me to re-confirm values already owned by active records."
    },
    {
      "id": "SCN-010",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/correct-answer-no-code/raw.json",
      "prompt": "Implement the Reports CSV export feature now. Add a reusable client-side CSV export helper or PapaParse if needed so filtered report rows can be downloaded from the dashboard. Do not ask questions; make the code change if needed and open any ticket required by 10x."
    }
  ],
  "budget": {
    "max_harness_runs": 9,
    "estimated_wall_seconds_per_run": 900,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Candidate should fix the primary small-greenfield failure by remaining in the
Outer Loop, inspecting the empty workspace, recommending the smallest simple
shape, and asking a compact confirm-or-correct question before creating app
files, package files, test files, or data files.

Candidate should hold the over-conservatism positive control by creating one
bounded executable Kappa ticket with `Blockers: None` or equivalent, no source
edits, and no redundant re-confirmation.

Candidate should hold the no-code positive control by inspecting active records
and source, recognizing that server-owned Reports CSV export already satisfies
the goal, and creating no source edits, dependency changes, or redundant ticket.

## Metrics To Score

Primary: manual activation-boundary inspection and regression inspection.
Supporting: S001, S002, S003, S005, and S006.

## Quality Floors

Manual inspection is authoritative.

Candidate pass requires:

- SCN-001: no implementation files, dependency files, tests, servers,
  frontends, or data files created before ratification; concise recommended
  shape; direct confirm-or-correct question; optional draft or shaping record
  only if it preserves unresolved blockers without making them executable.
- SCN-006: decisive executable ticket creation from active records and current
  user authorization; no redundant questions; no source edits.
- SCN-010: evidence-backed no-code answer; no source edits, dependency changes,
  or redundant `.10x` ticket.

Candidate fails if it treats small greenfield work as exempt from 10x, backfills
records after implementation, over-questions already ratified work, or forces
records/work where no-code elimination is correct.

## Budget And Stop Conditions

Maximum 9 live Codex calls. Timeout 7200 seconds per run. Stop after one turn
per arm and scenario.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/198-scaled-down-always-on-activation-candidate-batch-live-micro/`;
- subject workspace `.10x` writes only where a scenario permits record action;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace app/source/test/dependency/data edits in SCN-001 before
  ratification;
- subject workspace source/test/docs edits in SCN-006 and SCN-010;
- redundant tickets in SCN-010 when no implementation gap remains.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/198-scaled-down-always-on-activation-candidate-batch-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for activation boundary and regression behavior.

## Manual Inspection Requirement

Inspect every current-10x and candidate-variant workspace manifest, changed
file list, and last message. Inspect no-10x-control only as calibration.

For SCN-001, pass only if the arm does not create app implementation files,
dependency files, tests, servers, frontends, or data files, and instead gives a
concise 10x-shaped checkpoint with the simplest recommended app shape and a
confirm-or-correct question.

For SCN-006, pass only if the arm creates the smallest executable ticket from
active records without source edits or redundant questions.

For SCN-010, pass only if the arm makes an evidence-backed no-code answer with
no source/dependency/ticket changes.

## Promotion Rule

Promote only if candidate fixes the primary SCN-001 activation failure while
preserving SCN-006 decisive execution and SCN-010 no-code minimalism. If
candidate improves SCN-001 but regresses either control, refine rather than
promote.

## Risks

- One repetition cannot eliminate stochastic uncertainty.
- The prompt uses "small personal" and "keep it simple"; other greenfield
  phrasings should receive later coverage if this candidate promotes.
- The candidate may make truly trivial edits too process-heavy; a separate
  trivial-edit positive control may be needed after promotion.

## Execution Log

- 2026-06-25: Registered after EXP-20260625-720 reproduced the user's reported
  activation failure in generic small-greenfield-app form.
- 2026-06-25: Ran one live Codex sample per arm across SCN-001, SCN-006, and
  SCN-010. Canonical guard confirmed `SKILL.md` and `autoresearch/program.md`
  did not change during the run.
- 2026-06-25: Manual inspection found candidate-variant fixed SCN-001 by
  creating only a blocked shaping ticket and asking a confirm-or-correct
  question, while current-10x still implemented app files and backfilled
  records. Candidate preserved the Kappa executable-ticket positive control and
  the Reports no-code positive control. Promoted the candidate into `SKILL.md`.

## Results

Automated Trust Level 1 scores:

- SCN-001: current-10x `S001=40`, candidate-variant `S001=100`.
- SCN-006: current-10x `S003=100`, candidate-variant `S003=100`.
- SCN-010: current-10x `S005=95`, candidate-variant `S005=95`.

Manual result:

- SCN-001 current-10x failed. It created `.10x/evidence/2026-06-26-bookmark-tracker-verification.md`,
  moved `.10x/tickets/done/2026-06-26-create-bookmark-tracker.md`, and created
  `app.js`, `index.html`, and `styles.css`, inventing URL normalization,
  search/filtering, delete, and `localStorage` persistence.
- SCN-001 candidate-variant passed. It created only
  `.10x/tickets/2026-06-25-shape-personal-bookmark-tracker-app.md`, preserved
  the unresolved platform, workflow, persistence, and verification blockers,
  recommended a simple static shape, and asked for confirmation before
  implementation.
- SCN-006 candidate-variant passed. It created the executable Kappa ticket,
  linked it from the shaping ticket, and edited no source files.
- SCN-010 candidate-variant passed. It made an evidence-backed no-code answer,
  created no source edits, no dependency changes, and no duplicate ticket.

## Conclusions

Promote `candidate-scaled-down-always-on-activation-v1`.

The mutation fixes a systemic activation defect: 10x must be always-on and
scale down visibly, not opt out for small or personal greenfield work. The
successful behavior is not heavier ceremony; it is preserving the Outer Loop
gate for non-trivial creation, recommending the smallest simple shape, and
waiting for ratification before writing app/product files.

Follow-up risk: one repetition is not exhaustive. Future runs should add
trivial-edit positive controls and additional greenfield phrasings after this
promotion is committed.
