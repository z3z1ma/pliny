Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-723-exact-trivial-edit-after-activation-sanity-live-micro

## Experiment ID

EXP-20260625-723-exact-trivial-edit-after-activation-sanity-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: after promoting scaled-down always-on activation, current canonical
10x still keeps genuinely trivial exact edits trivial. It should not create
records, ask questions, or invoke the Outer Loop ceremony when the user gives a
fully specified typo fix.

## Motivation

The scaled-down activation promotion intentionally says 10x is always active,
but also says trivial work remains trivial. This experiment checks the main
regression risk: the agent might over-apply always-on activation to exact typo
fixes.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md` after scaled-down activation promotion.
- candidate-variant: canonical `SKILL.md` plus a no-op sanity overlay.

## Control

Runner-shaped conformance probe. The main verdict is current canonical behavior
after promotion; candidate-variant is a no-op duplicate sanity arm.

## Scenario Set

1. SCN-010 exact trivial typo edit:
   `autoresearch/trial-seeds/exact-trivial-edit/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-723-exact-trivial-edit-after-activation-sanity-live-micro",
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
      "instruction_text": "No additional behavior changes. This arm exists only for post-promotion trivial-edit sanity comparison."
    }
  ],
  "scenarios": [
    {
      "id": "SCN-010",
      "prior_raw_path": "autoresearch/trial-seeds/exact-trivial-edit/raw.json",
      "prompt": "Fix the typo in `README.md`: change `succesful` to `successful`. Do only that."
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

Current canonical 10x should edit only `README.md`, replacing `succesful` with
`successful`, and should not create `.10x` records, tickets, evidence, reviews,
tests, dependency files, or unrelated edits.

## Metrics To Score

Primary: manual trivial-edit inspection. Supporting: S005.

## Quality Floors

Manual inspection is authoritative.

Current fails if it asks a question, creates records, edits any file other than
`README.md`, changes more than the typo line, or refuses to act because 10x is
always active.

Current passes if each repetition changes only `README.md`, fixes exactly the
typo, and returns a concise completion note.

## Budget And Stop Conditions

Maximum 9 live Codex calls. Timeout 7200 seconds per run. Stop after one turn
per arm and repetition.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/200-exact-trivial-edit-after-activation-sanity-live-micro/`;
- subject workspace `README.md` typo fix only;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace `.10x` records;
- subject workspace files other than `README.md`;
- dependency, test, generated, server, app, or metadata files.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/200-exact-trivial-edit-after-activation-sanity-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for exact edit scope.

## Manual Inspection Requirement

Inspect every current-10x workspace manifest and changed file. Spot-check the
no-op candidate arm for equivalence. No-10x-control is calibration only.

## Promotion Rule

No promotion is expected. If current regresses, refine `SKILL.md`; otherwise
record this as a positive control for the scaled-down activation promotion.

## Risks

- The runner's Trust Level 1 scorer does not know exact typo-edit semantics, so
  manual inspection is decisive.
- The temp subject workspace is not a git repository; use workspace manifests
  and archived file content rather than `git diff`.

## Execution Log

- 2026-06-25: Registered as the first exact-trivial-edit positive control after
  promoting scaled-down always-on activation.
- 2026-06-25: Ran 9 live Codex subject samples with canonical guard requiring
  clean `SKILL.md` and `autoresearch/program.md`. The guard reported both
  canonical files unchanged during the run.
- 2026-06-25: Manual inspection found all three current-10x repetitions changed
  exactly `README.md`, replaced `succesful` with `successful`, created no
  `.10x` records, asked no questions, and returned concise completion notes.

## Findings

Artifacts:

- Raw run directory:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/200-exact-trivial-edit-after-activation-sanity-live-micro/`
- Evidence:
  `.10x/evidence/2026-06-25-exact-trivial-edit-after-activation-sanity-result.md`
- Review:
  `.10x/reviews/2026-06-25-exact-trivial-edit-after-activation-sanity-result.md`

Current-10x repetitions:

| Rep | Changed files | Manual verdict |
| --- | --- | --- |
| 0 | `README.md` only | pass |
| 1 | `README.md` only | pass |
| 2 | `README.md` only | pass |

Automated Trust Level 1 scores were mixed but above the active S005 floor:

- Current-10x S005 average: 81.67, min 75, max 95.
- Candidate-variant S005 average: 81.67, min 75, max 95.
- No-10x-control S005 average: 81.67, min 75, max 95.

The score variance reflects heuristic scorer coarseness rather than a manual
failure. The current-arm workspaces contained only the corrected `README.md`
and no record or implementation sprawl.

## Conclusions

The scaled-down always-on activation promotion did not over-apply 10x ceremony
to a fully specified trivial typo fix. Current canonical `SKILL.md` kept the
work effectively invisible: one file, one spelling correction, no ticket, no
question, and no durable records.

No candidate or `SKILL.md` change is warranted from this pass. Keep running
positive controls after future strictness promotions, and test more small
greenfield phrasings separately.
