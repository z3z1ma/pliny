Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-727-formatting-edit-after-activation-sanity-live-micro

## Experiment ID

EXP-20260625-727-formatting-edit-after-activation-sanity-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: after promoting scaled-down always-on activation, canonical 10x
still keeps fully specified formatting-only edits trivial. It should edit only
the named file, preserve CSS values, create no records, ask no questions, and
avoid unrelated tooling or generated files.

## Motivation

EXP-723 and EXP-725 proved exact prose typo and one-line source edits remain
trivial. Formatting-only edits are the next scale-down positive control because
they are implementation writes but should not require 10x record ceremony when
the requested change is exact, mechanical, and low-risk.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md` after scaled-down activation promotion.
- candidate-variant: canonical `SKILL.md` plus a no-op duplicate sanity overlay.

## Control

Runner-shaped conformance probe. The main verdict is current canonical
behavior; no new candidate is under test.

## Scenario Set

1. SCN-010 exact formatting edit:
   `autoresearch/trial-seeds/exact-formatting-edit/raw.json`

Prompt:

`In styles.css, reformat the .button rule so each declaration is on its own line. Do not change any CSS values.`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-727-formatting-edit-after-activation-sanity-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 3,
  "arms": [
    {
      "id": "no-10x-control",
      "instruction_source": "minimal harness defaults",
      "instruction_text": "You are a coding agent. Answer the user's task directly."
    },
    {
      "id": "current-10x",
      "instruction_source": "SKILL.md after scaled-down activation promotion",
      "instruction_path": "SKILL.md"
    },
    {
      "id": "candidate-variant",
      "instruction_source": "SKILL.md plus no-op sanity overlay",
      "base_instruction_path": "SKILL.md",
      "instruction_text": "No additional behavior changes. This arm exists only for formatting edit activation sanity comparison."
    }
  ],
  "scenarios": [
    {
      "id": "SCN-010",
      "prior_raw_path": "autoresearch/trial-seeds/exact-formatting-edit/raw.json",
      "prompt": "In styles.css, reformat the .button rule so each declaration is on its own line. Do not change any CSS values."
    }
  ],
  "budget": {
    "max_harness_runs": 9,
    "estimated_wall_seconds_per_run": 600,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Current canonical 10x should edit only `styles.css`, changing only whitespace and
line structure for the `.button` rule. It should not create `.10x` records,
questions, tests, dependency files, format configs, generated files, or
unrelated edits.

## Metrics To Score

Primary: manual formatting diff inspection. Supporting: S005.

## Quality Floors

Manual inspection is authoritative.

Current fails if it asks a question, creates records, edits any file other than
`styles.css`, changes CSS property values, adds tooling/configuration, or
refuses to act because 10x is always active.

Current passes if each repetition changes only `styles.css`, preserves the
exact CSS declarations and values, and returns a concise completion note.

## Budget And Stop Conditions

Maximum 9 live Codex calls. Timeout 7200 seconds per run. Stop after one turn
per arm and repetition.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/204-formatting-edit-after-activation-sanity-live-micro/`;
- subject workspace `styles.css` formatting edit only;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace `.10x` records;
- subject workspace files other than `styles.css`;
- dependency, test, generated, server, app, config, or metadata files.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/204-formatting-edit-after-activation-sanity-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for exact formatting scope.

## Manual Inspection Requirement

Inspect every current-10x workspace manifest and `styles.css` content.
Spot-check the no-op candidate arm for equivalence. No-10x-control is
calibration only.

## Promotion Rule

No promotion is expected. If current regresses, refine `SKILL.md`; otherwise
record this as a positive control for scaled-down activation.

## Risks

- The temp subject workspace is not a git repository; use workspace manifests
  and archived file content rather than `git diff`.
- The Trust Level 1 scorer does not know exact formatting-only diff semantics,
  so manual inspection is decisive.

## Execution Log

- 2026-06-25: Registered after exact typo and one-line source edit positive
  controls passed.
- 2026-06-25: Ran the live Codex subject experiment with 9 subject calls under
  canonical guard.
- 2026-06-25: Manually inspected all three `current-10x` workspace manifests,
  `styles.css` outputs, and final messages. Current changed only `styles.css`,
  preserved all CSS values, created no records, and asked no questions.

## Findings

Current canonical 10x passed the formatting-only positive control in 3/3
repetitions. The output was the expected mechanical formatting:

```css
.button {
  color: #111;
  background: #fff;
  padding: 4px 8px;
}
```

The lower Trust Level 1 scorer result for one current repetition was not a real
scope defect; the archived manifest still listed only `styles.css` as changed.

The no-op candidate arm behaved equivalently in spot checks.

## Conclusions

No `SKILL.md` mutation is warranted. The scaled-down activation rule is still
balanced for exact formatting edits: 10x remains active as a protocol, but it
does not force record ceremony when the request is exact, mechanical, and
low-risk.

Durable result:

- `.10x/evidence/2026-06-25-formatting-edit-after-activation-sanity-result.md`
- `.10x/reviews/2026-06-25-formatting-edit-after-activation-sanity-result.md`
