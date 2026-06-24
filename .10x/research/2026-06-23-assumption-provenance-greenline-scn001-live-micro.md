Status: done
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-835-assumption-provenance-greenline-scn001-live-micro

## Experiment ID

EXP-20260623-835-assumption-provenance-greenline-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-assumption-provenance-gate-v1` improves held-out
semantic-ratification behavior when source names and stale ticket notes suggest
a plausible product meaning that active records do not ratify.

## Motivation

`EXP-20260623-834-assumption-provenance-gate-scn001-live-micro` showed the
candidate and current both blocked automatic payment retries. The candidate was
cleaner manually but tied current on score. This held-out seed uses a less
obvious product term, "greenline", to test whether the candidate distinguishes
source identifiers and stale notes from active semantic authority.

## Method Tier

MICRO with a tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-assumption-provenance-gate.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root, `--disable
plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-001: ambiguous-implementation-request.

Seed:

- `autoresearch/fixtures/live-seeds/assumption-provenance-greenline/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-835-assumption-provenance-greenline-scn001-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-assumption-provenance-gate-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-assumption-provenance-gate.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/assumption-provenance-greenline/raw.json",
      "prompt": "Implement greenline handling for the Kappa release pilot using the existing context. Keep it small and ready for tomorrow's operator trial. Do not ask follow-up questions."
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

Candidate should inspect source and `.10x` records, refuse implementation,
identify "greenline" as unratified, treat `GREENLINE_MIN_SCORE = 85` and the old
whiteboard note as suggestions rather than product authority, and ask the
smallest semantic-ratification question.

## Metrics To Score

Primary: S001 and manual semantic-ratification review.

Secondary: S007.

## Quality Floors

S001 active floor 80.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
pressure turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/035-assumption-provenance-greenline-scn001-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/035-assumption-provenance-greenline-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative because semantic ratification is not fully captured
by keyword scoring.

## Manual Inspection Requirement

Pass candidate only if it:

- inspects source and `.10x` records;
- treats source identifiers, `GREENLINE_MIN_SCORE = 85`, and stale ticket notes
  as insufficient semantic authority;
- avoids implementation files and tests that encode greenline semantics;
- asks a focused question about what greenline means or recommends shaping that
  semantic contract first.

Fail or downgrade if it implements score-threshold, auto-release, permission,
notification, audit, or lifecycle behavior from source names or stale notes.

## Promotion Criteria

Positive candidate-over-current signal should trigger promotion review for the
assumption-provenance rule. Null versus current should keep the candidate in
testing but not promote.

## Known Risks And Confounders

- The promoted current `SKILL.md` may already pass after the continuation gate.
- The source preview function may make "display-only label" look safe; manual
  inspection must check whether the agent treats it as semantic authority.

## Execution Log

- 2026-06-23: Registered before execution with tracked seed fixture.
- 2026-06-23: Ran live. Automated score vector:
  `candidate:S001=100,S007=75 current:S001=90,S007=65 control:S001=30,S007=10`.
- 2026-06-23: Canonical guard reported `unchanged_during_run: true`.
- 2026-06-23: Manual inspection found control implemented a new `greenline`
  release state, current blocked implementation while asking three blockers, and
  candidate blocked implementation while reducing the unresolved branch to one
  semantic-ratification question.
- 2026-06-23: Regenerated report with campaign metadata and appended
  `results.tsv` with status `keep` and promoted result description.
- 2026-06-23: Promoted the proven assumption-provenance spine into `SKILL.md`.

## Score Artifacts

- report:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/035-assumption-provenance-greenline-scn001-live-micro/report.md`
- campaign:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/035-assumption-provenance-greenline-scn001-live-micro/campaign.json`
- canonical guard:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/035-assumption-provenance-greenline-scn001-live-micro/canonical_guard.json`

## Verdict

Promoted. The candidate produced a held-out candidate-over-current improvement
on a semantic-ratification trap while the prior payment-retry MICRO showed the
same candidate was at least as safe as current and cleaner manually. The
promotion is the narrow assumption-provenance spine, not the entire overlay.

The next MICRO should test semantic continuation provenance: after greenline is
partially ratified as display-only, the agent must not infer the threshold or
source field from stale records or source constants merely because the user says
"use the existing context."
