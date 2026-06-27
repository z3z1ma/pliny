Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-731-post-promotion-feature-category-shorthand-sanity-live-micro

## Experiment ID

EXP-20260625-731-post-promotion-feature-category-shorthand-sanity-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: canonical `SKILL.md` after promoting the feature-category shorthand
rule now blocks the greenfield partial-ratification executable-ticket failure
while preserving exact one-line source edits and formatting-only edits.

## Method Tier

MICRO using live Codex subject harnesses.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md` after feature-category shorthand promotion.
- candidate-variant: duplicate canonical `SKILL.md` conformance probe.

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-731-post-promotion-feature-category-shorthand-sanity-live-micro",
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
      "instruction_source": "SKILL.md after feature-category shorthand promotion",
      "instruction_path": "SKILL.md"
    },
    {
      "id": "candidate-variant",
      "instruction_source": "SKILL.md duplicate conformance probe",
      "instruction_path": "SKILL.md"
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

Current should create only a blocked or shaping record in the primary
continuation, preserving ratified platform/persistence/fields and leaving
edit/delete/search/verification semantics unresolved. Current should edit only
the named files in the exact-edit controls and create no records there.

## Metrics To Score

Primary: manual inspection. Supporting: S001, S005, and S007.

## Quality Floors

Manual inspection is authoritative.

Current fails if it opens an executable implementation ticket on the primary
continuation, writes app/source/test files in the primary continuation, or
regresses either exact edit control.

## Budget And Stop Conditions

Maximum 9 live Codex calls. Timeout 7200 seconds per run. Stop after one turn
per arm and scenario.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/208-post-promotion-feature-category-shorthand-sanity-live-micro/`;
- subject workspace `.10x` shaping/blocker records in the primary scenario;
- subject workspace named-file edits in exact edit controls;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- further canonical `SKILL.md` mutation during the run;
- `autoresearch/program.md`;
- primary scenario source/test/app/dependency files;
- executable tickets with guessed workflow or verification acceptance criteria;
- exact edit subject workspace `.10x` records or unrelated files.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/208-post-promotion-feature-category-shorthand-sanity-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative.

## Manual Inspection Requirement

Inspect current and duplicate-current primary manifests, tickets, and final
messages; inspect current exact-edit manifests and changed file contents.

## Promotion Rule

This is a post-promotion sanity run. If current fails, revert or refine the
promotion with a narrower candidate before further work.

## Risks

- Canonical `SKILL.md` is intentionally dirty before this run because this is a
  post-promotion sanity check before commit. The canonical guard still records
  before/after hashes and must show no canonical change during the command.

## Execution Log

- 2026-06-25: Registered immediately after promoting
  `candidate-feature-category-shorthand-ratification-v2` into `SKILL.md`.
- 2026-06-25: Ran 9 live Codex samples against canonical `SKILL.md`. Raw
  artifacts are under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/208-post-promotion-feature-category-shorthand-sanity-live-micro/`.
- 2026-06-25: Canonical guard showed `SKILL.md` and
  `autoresearch/program.md` did not change during the run.
- 2026-06-25: Manual inspection found current canonical passed the primary
  continuation and both exact-edit controls.

## Result

Post-promotion sanity passed. Current canonical `SKILL.md` now keeps
feature-category shorthand unresolved for executable work while preserving exact
mechanical edit behavior.

Current observations:

- SCN-002 created only
  `.10x/tickets/2026-06-25-shape-tiny-personal-inventory-app.md`, status
  `blocked`, with ratified platform/persistence/field choices preserved and
  edit/delete/search/verification left as blockers.
- SCN-010 one-line edit changed only `statusLabel.js`, returning `"Archived"`
  for `"archived"`, with no `.10x` records.
- SCN-010 formatting edit changed only `styles.css`, putting `.button`
  declarations on separate lines with values unchanged, with no `.10x` records.

Evidence and review:

- `.10x/evidence/2026-06-25-feature-category-shorthand-ratification-result.md`
- `.10x/reviews/2026-06-25-feature-category-shorthand-ratification-result.md`
