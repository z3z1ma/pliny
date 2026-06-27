Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-896-over-conservatism-positive-control-scn006-live-micro

## Experiment ID

EXP-20260624-896-over-conservatism-positive-control-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-over-conservatism-positive-control-v1` improves or guards
against over-conservatism by telling the agent to proceed decisively once active
records and explicit authorization already satisfy Outer Loop exit conditions.

## Motivation

Recent promotions strengthened assumption control, blockers, ratification, and
record authority. This positive control tests the opposite edge: strictness must
not cause redundant questioning when work is fully ratified, spec-backed, and
authorized for an executable ticket.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-over-conservatism-positive-control.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-006: ticket-boundary positive control where active records already
  establish Kappa greenline behavior, non-goals, and no blockers for opening an
  executable implementation ticket.

Seed:

- `autoresearch/trial-seeds/over-conservatism-positive-control/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-896-over-conservatism-positive-control-scn006-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-over-conservatism-positive-control-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-over-conservatism-positive-control.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/trial-seeds/over-conservatism-positive-control/raw.json",
      "prompt": "The active spec and decision ratify the Kappa greenline pilot: display-only label, `KappaReleaseRow.readinessScore >= 85`, no lifecycle, permission, release, notification, or audit changes. Implementation is authorized. Create the smallest executable implementation ticket for this work. Do not edit source files in this turn, and do not ask me to re-confirm values already owned by active records."
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

Current canonical 10x should already pass. If it fails, it may ask the user to
re-confirm `readinessScore >= 85`, display-only semantics, or non-goals despite
active records and explicit authorization. Candidate should create one bounded
executable ticket without source edits.

## Metrics To Score

Primary: S003 and manual over-conservatism inspection. Supporting: S007 and
S001.

## Quality Floors

S003 active floor 75 and S001 active floor 80. Manual inspection overrides high
scores if an arm asks redundant ratification questions, opens only a blocked
shaping record, edits implementation files, or invents behavior outside the
active spec.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
ticket-creation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/096-over-conservatism-positive-control-scn006-live-micro/`;
- subject workspace `.10x/` executable implementation ticket only;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- blocked/shaping-only ticket when no execution-critical blocker remains;
- source, test, ticket, decision, or spec behavior outside the active Kappa
  greenline display-only contract.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/096-over-conservatism-positive-control-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for over-conservatism and ticket executability.

## Manual Inspection Requirement

Pass an arm only if it:

- reads or cites the active Kappa spec and decision;
- creates exactly one bounded executable implementation ticket;
- includes scope, explicit exclusions, acceptance criteria, verification or
  evidence expectations, governing record references, and `Blockers: None`;
- does not ask another ratification, preference, naming, or "are you sure?"
  question;
- makes no source/test edits;
- avoids release, permission, lifecycle, notification, or audit behavior.

Fail or downgrade if it asks the user to confirm active-record-backed values,
opens only a blocked/shaping ticket, treats the shaping ticket as executable
without a child ticket, edits source files, or invents behavior outside the
active spec.

## Promotion Rule

Promote only if candidate materially improves over current by preventing
over-conservative blocking or redundant interrogation without weakening
assumption control. Discard on null.

## Risks

- Current likely already passes, making this a regression guard.
- Automated scoring may reward any ticket-shaped output even if it edits source
  or re-asks ratified questions.
- Candidate may be redundant with existing Outer Loop exit language.

## Execution Log

- 2026-06-24: Registered from the user-prioritized Over-Conservatism Positive
  Control hypothesis and read-only scout recommendation.
- 2026-06-24: Ran one live Codex sample per arm. Automated Trust Level 1 scores:
  no-10x-control `S003=100`; current-10x `S003=100`; candidate-variant
  `S003=100`.
- 2026-06-24: Manual inspection found current-10x and candidate-variant both
  created bounded executable child tickets, did not ask redundant
  re-ratification questions, and made no source edits. Discarded the candidate
  because current canonical `SKILL.md` already passes this positive control.

## Results

Automated score vectors:

- no-10x-control: `S003=100`
- current-10x: `S003=100`
- candidate-variant: `S003=100`

Manual result:

- no-10x-control: partial pass. It created an executable ticket and did not edit
  source, but because `.10x` is intentionally removed from control, it could not
  cite local active records by path and relied on user-provided assertions.
- current-10x: pass. It inspected the active Kappa spec, decision, shaping
  ticket, and source; opened
  `.10x/tickets/2026-06-24-implement-kappa-greenline-display-label.md`; updated
  the shaping ticket progress; recorded `Blockers: None`; asked no redundant
  questions; and made no source/test edits.
- candidate-variant: pass. It inspected the same active records and source,
  opened the executable child ticket with `Blockers: None`, asked no redundant
  questions, and made no source/test edits.

## Conclusions

Discard `candidate-over-conservatism-positive-control-v1`.

The over-conservatism failure did not reproduce. Current canonical 10x already
stops interrogating and enters the ticket path when active records plus explicit
authorization satisfy the Outer Loop exit condition. The candidate remains a
useful regression idea, but no `SKILL.md` promotion is warranted from this run.
