Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-861-ticket-readiness-real-source-scn006-live-micro

## Experiment ID

EXP-20260624-861-ticket-readiness-real-source-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-ticket-readiness-gate-v1` improves ticket readiness when
the source tree and active records are present by creating one bounded,
source-aware executable ticket with explicit evidence expectations.

## Motivation

The prior ticket-readiness run showed candidate improvement, but the generated
workspace lacked the referenced source tree and the no-10x control also created
a passable ticket. This run uses a seeded workspace with actual source and
active records so manual inspection can judge source-aware ticket quality.

## Method Tier

MICRO using a tracked real-source SCN-006 seed.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-ticket-readiness-gate.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-006: approved non-trivial implementation direction with source and active
  records present; the next safe action should be ticket creation, not another
  question and not implementation.

Seed:

- `autoresearch/trial-seeds/ticket-readiness-real-source/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-861-ticket-readiness-real-source-scn006-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-ticket-readiness-gate-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-ticket-readiness-gate.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/trial-seeds/ticket-readiness-real-source/raw.json",
      "prompt": "We approved the enterprise billing exceptions CSV export decision. Prepare execution for a subagent, but do not implement and do not ask questions. Use the existing source and records. Required behavior: add CSV export to `src/features/billing/ExceptionsPage.tsx`; export only currently visible rows from `usePricingExceptions()`; CSV columns are `customer_id`, `account_name`, `exception_reason`, `requested_discount_pct`, `status`, `requested_by`, and `created_at`; no backend, auth, permissions, email, notification, or data-model changes; empty visible row set disables the export button with existing disabled-button styling; tests must cover CSV escaping/content and empty-state disabled behavior. Create the one executable 10x ticket a subagent should execute."
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

Candidate should create exactly one bounded executable ticket with scope,
non-goals, acceptance criteria, evidence expectations, source/record references,
and honest blockers. It should not ask questions or edit source. Current may
create a usable ticket but omit evidence expectations or source-specific
verification details.

## Metrics To Score

Primary: S003 and manual ticket-quality inspection. Supporting: S007 and S005.

## Quality Floors

S003 active floor 75. Manual inspection is authoritative for source-aware ticket
quality and evidence-expectation completeness.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
ticket-readiness turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/061b-ticket-readiness-real-source-scn006-live-micro/`;
- records created in the subject workspace under `.10x/` only;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- source files;
- dependency additions.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/061b-ticket-readiness-real-source-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for created tickets.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects the active decision/spec and source files;
- creates exactly one executable ticket;
- creates no source or dependency edits;
- does not ask questions;
- includes scope and explicit non-goals;
- includes acceptance criteria tied to visible rows, the exact columns, empty
  state, and CSV escaping/content;
- names source references;
- names evidence expectations, including the relevant test command or test
  evidence shape;
- records blockers honestly, with none acceptable only if the source and records
  are sufficient.

Fail if it implements, asks unnecessary questions, creates a parent plan without
an executable child, omits source/record references, omits evidence
expectations, invents backend/auth/data-model scope, or claims source is missing
when the seed includes it.

## Promotion Criteria

Promote only if candidate materially improves source-aware executable ticket
quality over current while preserving no-implementation and no-extra-question
discipline. Null versus current should discard or leave experimental.

## Known Risks And Confounders

- This tests ticket authoring, not implementation quality.
- The no-10x control may still create a reasonable ticket from the prompt alone;
  manual inspection should focus on 10x-specific record/source/evidence
  discipline.

## Execution Log

- 2026-06-24: Registered after EXP-860 promotion to retest the older
  ticket-readiness candidate with a stronger real-source seed.
- 2026-06-24: First run to `061-ticket-readiness-real-source-scn006-live-micro`
  was interrupted and marked confounded. The seed manifest used `"workspace":
  "."`, and the runner resolved it relative to the canonical repository instead
  of the manifest directory, causing the subject workspace to include the whole
  10x repository. Fixed the runner/validator resolver and moved the clean rerun
  target to `061b-ticket-readiness-real-source-scn006-live-micro`.
- 2026-06-24: Reran to `061b-ticket-readiness-real-source-scn006-live-micro`
  after the resolver fix. Clean workspaces contained only the seed source,
  active records, and subject-created ticket records.

## Results

Automated Trust Level 1 score vectors:

- candidate-variant: `S003=100`
- current-10x: `S003=80`
- no-10x-control: `S003=65`, below the active S003 floor

Manual inspection:

- candidate-variant inspected the active decision/spec, source files, and
  package script; created exactly one executable ticket; included scope,
  exclusions, acceptance criteria, governing context, source references, evidence
  expectations, implementation notes, and supported `Blockers: None`.
- current-10x inspected the active decision/spec and source files and created
  exactly one executable ticket, but omitted a dedicated evidence-expectations
  section and was less explicit about closure evidence shape.
- no-10x-control had inherited `.10x` removed, created a ticket from source and
  prompt alone, and lacked record dependencies.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/061b-ticket-readiness-real-source-scn006-live-micro/`

## Conclusions

Promote `candidate-ticket-readiness-gate-v1` narrowly. The validated behavior is
not broader ticket ceremony; it is recognizing when enough source/record context
exists to stop asking questions and create one executable ticket with evidence
expectations, source/record references, and honest blockers.
