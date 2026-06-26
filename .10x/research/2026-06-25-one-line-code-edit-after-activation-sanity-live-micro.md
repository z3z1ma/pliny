Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-725-one-line-code-edit-after-activation-sanity-live-micro

## Experiment ID

EXP-20260625-725-one-line-code-edit-after-activation-sanity-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: after promoting scaled-down always-on activation, canonical 10x
still keeps fully specified one-line mechanical code edits trivial. It should
edit exactly the named line and should not ask questions, create records, run a
ceremonial Outer Loop, or touch unrelated files.

## Motivation

EXP-723 proved exact prose typo edits remain trivial. The next positive control
is a tiny code edit, because always-on activation must not turn exact source
changes into record bureaucracy.

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

1. SCN-010 exact one-line code edit:
   `autoresearch/fixtures/live-seeds/exact-one-line-code-edit/raw.json`

Prompt:

`In statusLabel.js, change the label returned for "archived" from "Old" to "Archived". Do only that.`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-725-one-line-code-edit-after-activation-sanity-live-micro",
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
      "instruction_text": "No additional behavior changes. This arm exists only for one-line code edit activation sanity comparison."
    }
  ],
  "scenarios": [
    {
      "id": "SCN-010",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/exact-one-line-code-edit/raw.json",
      "prompt": "In statusLabel.js, change the label returned for \"archived\" from \"Old\" to \"Archived\". Do only that."
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

Current canonical 10x should edit only `statusLabel.js`, replacing the
`archived` label string from `Old` to `Archived`, and should not create `.10x`
records, tickets, evidence, reviews, tests, dependency files, generated files,
or unrelated edits.

## Metrics To Score

Primary: manual one-line diff inspection. Supporting: S005.

## Quality Floors

Manual inspection is authoritative.

Current fails if it asks a question, creates records, edits any file other than
`statusLabel.js`, changes more than the requested label string, or refuses to
act because 10x is always active.

Current passes if each repetition changes only `statusLabel.js`, changes only
the `archived` label from `Old` to `Archived`, and returns a concise completion
note.

## Budget And Stop Conditions

Maximum 9 live Codex calls. Timeout 7200 seconds per run. Stop after one turn
per arm and repetition.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/202-one-line-code-edit-after-activation-sanity-live-micro/`;
- subject workspace `statusLabel.js` label edit only;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace `.10x` records;
- subject workspace files other than `statusLabel.js`;
- dependency, test, generated, server, app, or metadata files.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/202-one-line-code-edit-after-activation-sanity-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for exact edit scope.

## Manual Inspection Requirement

Inspect every current-10x workspace manifest and `statusLabel.js` content.
Spot-check the no-op candidate arm for equivalence. No-10x-control is
calibration only.

## Promotion Rule

No promotion is expected. If current regresses, refine `SKILL.md`; otherwise
record this as a positive control for scaled-down activation.

## Risks

- The temp subject workspace is not a git repository; use workspace manifests
  and archived file content rather than `git diff`.
- The Trust Level 1 scorer does not know exact one-line code diff semantics, so
  manual inspection is decisive.

## Execution Log

- 2026-06-25: Registered after EXP-724 passed varied greenfield activation
  phrasings.
- 2026-06-25: Ran 9 live Codex subject samples with `--require-clean-canonical`.
  Canonical guard reported `SKILL.md` and `autoresearch/program.md` unchanged.
- 2026-06-25: Manual inspection found all three current-10x repetitions changed
  exactly `statusLabel.js`, changed only the archived label from `Old` to
  `Archived`, created no `.10x` records, and asked no questions.

## Findings

Artifacts:

- Raw run directory:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/202-one-line-code-edit-after-activation-sanity-live-micro/`
- Evidence:
  `.10x/evidence/2026-06-25-one-line-code-edit-after-activation-sanity-result.md`
- Review:
  `.10x/reviews/2026-06-25-one-line-code-edit-after-activation-sanity-result.md`

Current-10x repetitions:

| Rep | Changed files | Manual verdict |
| --- | --- | --- |
| 0 | `statusLabel.js` only | pass |
| 1 | `statusLabel.js` only | pass |
| 2 | `statusLabel.js` only | pass |

Automated Trust Level 1 score summary:

- Current-10x S005 average: 81.67, min 75, max 95.
- Candidate-variant S005 average: 88.33, min 75, max 95.
- No-10x-control S005 average: 81.67, min 75, max 95.

The score variance reflects heuristic scorer coarseness. Manual inspection is
decisive for exact one-line code edit scope.

## Conclusions

The scaled-down always-on activation promotion did not over-apply 10x ceremony
to a fully specified one-line source edit. Current canonical `SKILL.md` kept
the work small: one file, one string literal, no ticket, no question, and no
durable records.

No candidate or `SKILL.md` change is warranted from this pass. Keep formatting-
only and non-Codex mechanical edit controls in the backlog after future
strictness promotions.
