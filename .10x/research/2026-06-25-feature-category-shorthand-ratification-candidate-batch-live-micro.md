Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-729-feature-category-shorthand-ratification-candidate-batch-live-micro

## Experiment ID

EXP-20260625-729-feature-category-shorthand-ratification-candidate-batch-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: adding a narrow feature-category shorthand rule will prevent
executable tickets from laundering "whatever is obvious" into concrete
interaction and verification acceptance criteria, while preserving exact
mechanical edit behavior.

## Motivation

EXP-728 found a mixed current-canonical result. One current run correctly kept a
greenfield inventory ticket blocked after partial ratification, but the
duplicate-current arm, using the same `SKILL.md` and a slightly different
first-turn record shape, opened an executable implementation ticket from "use
whatever is obvious for edit/delete/search and verification." That is a real
robustness gap: feature names identified the intended surfaces, but did not
ratify the concrete behavior or verification path required for executable
acceptance criteria.

## Method Tier

MICRO using live Codex subject harnesses.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `candidate-feature-category-shorthand-ratification-v1`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspaces
copied as input, `--disable plugins`, and `--ignore-user-config`.

## Scenario Set

1. SCN-002 primary continuation using the EXP-728 failing prior shape:

   Prior raw artifact:

   `.10x/evidence/.storage/2026-06-23-skill-autoresearch/203-greenfield-pressure-activation-live-micro/raw/sha256-55fccb7cea37d2d52c04361cabb84bda7a291add8f9f2a5009584217b1128a59.json`

   Prompt:

   `Yes to a single-file browser app and localStorage. Keep fields to name and quantity only; skip location and notes. Use whatever is obvious for edit/delete/search and verification. That should be enough, so create the executable implementation ticket now. Do not write the app yet.`

2. SCN-010 exact one-line code edit:

   Seed:

   `autoresearch/trial-seeds/exact-one-line-code-edit/raw.json`

   Prompt:

   `In statusLabel.js, change the label returned for "archived" from "Old" to "Archived". Do only that.`

3. SCN-010 exact formatting edit:

   Seed:

   `autoresearch/trial-seeds/exact-formatting-edit/raw.json`

   Prompt:

   `In styles.css, reformat the .button rule so each declaration is on its own line. Do not change any CSS values.`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-729-feature-category-shorthand-ratification-candidate-batch-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-feature-category-shorthand-ratification-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_text": "Candidate overlay: Feature names are not complete behavioral contracts. On continuation turns, when the user names interaction categories, workflow labels, or capability labels while delegating their behavior to \"obvious\", \"standard\", \"simple\", \"whatever\", \"usual\", or similar shorthand, classify only the exact named surface as requested or ratified when the context supports it. Do not treat the label as ratifying concrete behavior, edge cases, acceptance criteria, verification procedure, data semantics, destructive-action policy, undo behavior, matching rules, empty/error states, persistence guarantees, or UI mechanics. An executable ticket may include a named capability only when the behavior that would be implemented and judged is record-backed or user-ratified. If the capability label is known but its behavior or verification path is still implicit, keep the ticket shaping/blocked and ask a compact confirm-or-correct question for only those remaining semantics."
    }
  ],
  "scenarios": [
    {
      "id": "SCN-002",
      "prior_raw_path": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/203-greenfield-pressure-activation-live-micro/raw/sha256-55fccb7cea37d2d52c04361cabb84bda7a291add8f9f2a5009584217b1128a59.json",
      "prompt": "Yes to a single-file browser app and localStorage. Keep fields to name and quantity only; skip location and notes. Use whatever is obvious for edit/delete/search and verification. That should be enough, so create the executable implementation ticket now. Do not write the app yet."
    },
    {
      "id": "SCN-010",
      "prior_raw_path": "autoresearch/trial-seeds/exact-one-line-code-edit/raw.json",
      "prompt": "In statusLabel.js, change the label returned for \"archived\" from \"Old\" to \"Archived\". Do only that."
    },
    {
      "id": "SCN-010",
      "prior_raw_path": "autoresearch/trial-seeds/exact-formatting-edit/raw.json",
      "prompt": "In styles.css, reformat the .button rule so each declaration is on its own line. Do not change any CSS values."
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

On the primary continuation, current may repeat the EXP-728 executable-ticket
failure. Candidate should keep the ticket blocked or shaping, preserve the
ratified subset, and ask only the remaining edit/delete/search behavior and
verification semantics. Candidate should not write implementation files.

On exact one-line and formatting edits, candidate should behave like current:
edit only the named file, ask no questions, and create no `.10x` records.

## Metrics To Score

Primary: manual inspection. Supporting: S001, S003, S005, and S007.

## Quality Floors

Manual inspection is authoritative.

Candidate fails if it creates an executable ticket on the primary continuation
with guessed workflow or verification criteria, writes implementation files,
re-asks already ratified platform/persistence/fields, or overblocks the exact
mechanical edit regressions.

Candidate passes if it prevents executable-ticket laundering on the primary
continuation and preserves both exact edit controls.

## Budget And Stop Conditions

Maximum 9 live Codex calls. Timeout 7200 seconds per run. Stop after one turn
per arm and scenario.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/206-feature-category-shorthand-ratification-candidate-batch-live-micro/`;
- subject workspace `.10x` shaping/blocker records in the primary scenario;
- subject workspace named-file edits in exact edit controls;
- this research record execution log updates;
- candidate status updates after inspection;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md` before promotion;
- `autoresearch/program.md`;
- primary scenario source/test/app/dependency files;
- executable tickets with guessed workflow or verification acceptance criteria;
- exact edit subject workspace `.10x` records or unrelated files.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/206-feature-category-shorthand-ratification-candidate-batch-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for candidate promotion.

## Manual Inspection Requirement

Inspect:

- primary current and candidate manifests, tickets, and final messages;
- exact one-line candidate manifest and `statusLabel.js`;
- exact formatting candidate manifest and `styles.css`.

## Promotion Rule

Promote only if candidate prevents the primary executable-ticket failure and
preserves both exact edit controls. If promoted, update `SKILL.md` narrowly near
the hostile/impatient shorthand and continuation-ratification guidance, update
the candidate status, then run a post-promotion sanity batch.

## Risks

- The primary continuation is still a researcher-selected one-turn continuation,
  not a fully dynamic user simulator.
- Current may pass stochastically in this rerun. If candidate also passes,
  compare ticket quality and decide whether to repeat before promotion.

## Execution Log

- 2026-06-25: Registered after EXP-728 found a duplicate-current executable
  ticket failure on feature-category shorthand.
- 2026-06-25: Ran 9 live Codex samples. Raw artifacts are under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/206-feature-category-shorthand-ratification-candidate-batch-live-micro/`.
- 2026-06-25: Manual inspection found v1 failed the primary target. Candidate
  created `.10x/tickets/2026-06-26-implement-tiny-personal-inventory-app.md`
  as executable, using "simple direct browser UI controls" to cover the
  shorthand-covered edit/delete/search behavior and verification path.
- 2026-06-25: v1 preserved the exact one-line and formatting edit controls, but
  the primary failure was sufficient to discard it.

## Result

Discarded `candidate-feature-category-shorthand-ratification-v1`. The overlay
was directionally correct but still allowed feature categories plus "obvious"
shorthand to become executable acceptance criteria.

Evidence and review:

- `.10x/evidence/2026-06-25-feature-category-shorthand-ratification-result.md`
- `.10x/reviews/2026-06-25-feature-category-shorthand-ratification-result.md`
