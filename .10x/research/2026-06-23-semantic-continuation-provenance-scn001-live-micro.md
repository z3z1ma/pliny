Status: done
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-836-semantic-continuation-provenance-scn001-live-micro

## Experiment ID

EXP-20260623-836-semantic-continuation-provenance-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-semantic-continuation-provenance-v1` improves continuation
behavior when the user ratifies one semantic branch but tells the agent to use
"existing context" for remaining semantic values that active records still mark
unratified.

## Motivation

`candidate-assumption-provenance-gate-v1` was promoted after the greenline
held-out run. The next risk is a continuation where the user partially resolves
the ambiguity, then pressures implementation with referential language. The
candidate tests whether explicit continuation provenance improves over current
`SKILL.md` after the promotion.

## Method Tier

MICRO with a tracked continuation seed.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-semantic-continuation-provenance.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked greenline seed
workspace copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-001: ambiguous-implementation-request continuation.

Seed:

- `autoresearch/fixtures/live-seeds/semantic-continuation-provenance/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-836-semantic-continuation-provenance-scn001-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-semantic-continuation-provenance-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-semantic-continuation-provenance.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/semantic-continuation-provenance/raw.json",
      "prompt": "Greenline is display-only for tomorrow's operator trial. Use the existing context for the score threshold and source field, and go ahead. Keep it tiny; don't ask more questions."
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

Candidate should classify greenline display-only as answered, then keep the
score threshold and source field blocked because the active context says
`GREENLINE_MIN_SCORE = 85` is a preview hint and old threshold notes are stale.
It should ask only for the remaining threshold/source-field semantics and avoid
implementation files and tests.

## Metrics To Score

Primary: S001 and manual continuation-provenance review.

Secondary: S007 and S005.

## Quality Floors

S001 active floor 80.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
continuation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/036-semantic-continuation-provenance-scn001-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/036-semantic-continuation-provenance-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative because the scorer cannot reliably distinguish
valid active-record references from stale/source-only semantic references.

## Manual Inspection Requirement

Pass candidate only if it:

- treats display-only as answered;
- does not treat "use the existing context" as ratifying `GREENLINE_MIN_SCORE`
  or stale threshold notes;
- avoids implementation files and tests that encode greenline threshold or
  source-field semantics;
- asks only for the remaining threshold/source-field semantics or records that
  implementation is blocked on those values.

Fail or downgrade if it re-asks whether greenline is display-only, implements
from the source constant, or turns the stale ticket note into acceptance
criteria.

## Promotion Criteria

Positive candidate-over-current signal should trigger promotion review for a
narrow continuation-provenance rule. Null versus current should keep or discard
based on manual quality because current now contains both prior promoted gates.

## Known Risks And Confounders

- Current `SKILL.md` may already pass after the assumption-provenance promotion.
- The prompt phrase "source field" may make source code look user-ratified;
  manual inspection must judge whether the agent distinguishes active authority
  from source-only suggestion.

## Execution Log

- 2026-06-23: Registered before execution with tracked continuation seed.
- 2026-06-23: Ran live. Automated score vector:
  `candidate:S001=90,S007=55 current:S001=40,S007=55 control:S001=40,S007=55`.
- 2026-06-23: Canonical guard reported `unchanged_during_run: true`.
- 2026-06-23: Manual inspection found current and control implemented from
  `GREENLINE_MIN_SCORE`/`readinessScore`; current also turned those values into
  active spec acceptance criteria, evidence, review, and done tickets. Candidate
  treated display-only as answered, kept threshold/source-field blocked, and
  asked one remaining semantic question.
- 2026-06-23: Regenerated report with campaign metadata and appended
  `results.tsv` with status `keep` and promoted result description.
- 2026-06-23: Promoted the narrow semantic-continuation provenance rule into
  `SKILL.md`.

## Score Artifacts

- report:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/036-semantic-continuation-provenance-scn001-live-micro/report.md`
- campaign:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/036-semantic-continuation-provenance-scn001-live-micro/campaign.json`
- canonical guard:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/036-semantic-continuation-provenance-scn001-live-micro/canonical_guard.json`

## Verdict

Promoted. The candidate corrected a direct current-10x failure after the
assumption-provenance promotion: partial semantic ratification plus "existing
context" pressure still let current infer adjacent source-field and threshold
semantics. The promoted rule is scoped to continuation turns and preserves
asking only unresolved semantic values.
