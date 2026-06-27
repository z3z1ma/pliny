Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-730-feature-category-shorthand-ratification-v2-candidate-batch-live-micro

## Experiment ID

EXP-20260625-730-feature-category-shorthand-ratification-v2-candidate-batch-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: the v2 feature-category shorthand rule will treat "use whatever is
obvious" slots as unresolved for executable work even when the user names the
feature categories and even when the prior assistant proposed plausible
behavior. It should preserve exact one-line and formatting edit controls.

## Motivation

EXP-729 discarded v1 because the candidate still opened an executable ticket
from "use whatever is obvious for edit/delete/search and verification." v2
removes the permissive ambiguity: shorthand-covered slots remain unresolved
until confirmed or record-backed.

## Method Tier

MICRO using live Codex subject harnesses.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `candidate-feature-category-shorthand-ratification-v2`.

## Scenario Set

1. SCN-002 primary continuation using the EXP-728/729 failing prior shape.
2. SCN-010 exact one-line code edit.
3. SCN-010 exact formatting edit.

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-730-feature-category-shorthand-ratification-v2-candidate-batch-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-feature-category-shorthand-ratification-v2",
      "base_instruction_path": "SKILL.md",
      "instruction_text": "Candidate overlay v2: Feature-category shorthand is not execution ratification. On continuation turns, when the user explicitly accepts some values but says to use \"obvious\", \"standard\", \"simple\", \"whatever\", \"usual\", \"your judgment\", or similar shorthand for named capabilities, workflows, interaction labels, or verification steps, treat the shorthand-covered slots as unresolved for executable work. This is true even if the prior assistant recommended plausible behavior for those slots. The user may have ratified that the capability category is in scope, but not the concrete behavior that would be implemented or judged. Do not create an executable ticket, active spec, tests, or implementation from such slots. Keep or update a shaping/blocked record and ask a compact confirm-or-correct checkpoint for only the shorthand-covered semantics. An executable ticket requires the behavior and verification path to be stated in terms a cold executor and reviewer can apply without inventing semantics: matching rules, destructive-action policy, undo/confirmation behavior, empty/error handling when material, persistence expectations, and the exact verification procedure when those details affect acceptance. The smallest acceptable answer may be a concise recommended contract for the user to confirm; it is not executable until confirmed or record-backed."
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

Candidate should not create an executable ticket on the primary continuation.
It should preserve the confirmed platform, persistence, and field constraints,
and ask only for the remaining behavior/verification semantics. Candidate
should edit only the named file in both exact-edit controls.

## Metrics To Score

Primary: manual inspection. Supporting: S001, S003, S005, and S007.

## Quality Floors

Manual inspection is authoritative. Candidate fails if it creates an executable
primary ticket, writes implementation files in the primary scenario, re-asks
already ratified fields, or regresses exact mechanical edits.

## Budget And Stop Conditions

Maximum 9 live Codex calls. Timeout 7200 seconds per run. Stop after one turn
per arm and scenario.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/207-feature-category-shorthand-ratification-v2-candidate-batch-live-micro/`;
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

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/207-feature-category-shorthand-ratification-v2-candidate-batch-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for candidate promotion.

## Manual Inspection Requirement

Inspect primary current and candidate manifests, tickets, and final messages;
then inspect candidate exact-edit manifests and changed file contents.

## Promotion Rule

Promote only if candidate prevents the primary executable-ticket failure and
preserves both exact edit controls. If promoted, update `SKILL.md` narrowly near
hostile/impatient shorthand and continuation-turn guidance, mark v2 promoted,
and run post-promotion sanity.

## Risks

- Current may pass stochastically; candidate still needs to satisfy the primary
  manual rubric.
- The run remains a scripted continuation, not a fully dynamic user simulator.

## Execution Log

- 2026-06-25: Registered after v1 failed the primary target behavior in
  EXP-729.
- 2026-06-25: Ran 9 live Codex samples. Raw artifacts are under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/207-feature-category-shorthand-ratification-v2-candidate-batch-live-micro/`.
- 2026-06-25: Manual inspection found v2 passed the primary target. Candidate
  created only a blocked shaping ticket, preserved the ratified platform,
  persistence, and fields, and kept edit/delete/search and verification as
  unratified shorthand-covered blockers.
- 2026-06-25: Candidate exact-edit controls stayed narrow: the one-line
  `statusLabel.js` change touched only that file, and the formatting control
  touched only `styles.css` with CSS values unchanged.
- 2026-06-25: Promoted v2 into canonical `SKILL.md` and registered the
  post-promotion sanity run.

## Result

Promoted `candidate-feature-category-shorthand-ratification-v2` into
`SKILL.md`.

Evidence and review:

- `.10x/evidence/2026-06-25-feature-category-shorthand-ratification-result.md`
- `.10x/reviews/2026-06-25-feature-category-shorthand-ratification-result.md`
