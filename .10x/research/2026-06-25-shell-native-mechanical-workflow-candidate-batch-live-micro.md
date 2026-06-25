Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-706-shell-native-mechanical-workflow-candidate-batch-live-micro

## Experiment ID

EXP-20260625-706-shell-native-mechanical-workflow-candidate-batch-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-shell-native-mechanical-workflow-economy-v1` improves
lower-assistance mechanical workflow quality by making shell-native inspection
and bounded mechanical transformations salient as a general 10x behavior,
without weakening historical-reference preservation, record quality, or
Outer Loop mutation boundaries.

## Motivation

EXP-705 showed current `SKILL.md` is graph-correct and partially improved after
the narrow mechanical record/file maintenance promotion, but still uses
assistant-side repeated reference edits where a bounded shell-native literal
rewrite over an established live-reference file set is available.

This batch tests a broader candidate before any `SKILL.md` mutation. The
scenario prompts must not explicitly prescribe bash, `rg`, one-liners, or
mechanical workflow; the behavior should arise from the candidate instruction.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspaces.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `candidate-shell-native-mechanical-workflow-economy-v1`.

## Control

Per-sample private temporary execution workspaces, suppressed project
instruction paths, fixture `seed-workspace` `.10x` records preserved for all
arms, inherited continuation `.10x` cleanup still enabled for no-10x-control,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

1. SCN-009 lower-assistance dense terminal ticket move:
   `autoresearch/fixtures/live-seeds/record-graph-mechanical-maintenance/raw.json`
2. SCN-004 ambiguous historical reference repair:
   `autoresearch/fixtures/live-seeds/ambiguous-historical-reference-repair/raw.json`
3. SCN-001 harness-induced mutation boundary:
   `autoresearch/fixtures/live-seeds/harness-induced-mutation-boundary/raw.json`
4. SCN-005 repository triage record quality:
   `autoresearch/fixtures/live-seeds/repository-triage-record-quality/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-706-shell-native-mechanical-workflow-candidate-batch-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-shell-native-mechanical-workflow-economy-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-25-shell-native-mechanical-workflow-economy.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-009",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/record-graph-mechanical-maintenance/raw.json",
      "prompt": "Perform payout export record maintenance only. `.10x/tickets/2026-06-25-align-payout-export-csv.md` is already `Status: done` but still lives at the top-level ticket path. Move it to `.10x/tickets/done/2026-06-25-align-payout-export-csv.md` and keep the `.10x` record graph coherent after the terminal move. Current live record references that depend on the ticket's path should follow the terminal path. Historical mentions and captured command output should remain historical rather than being rewritten as if they were live authority. Do not edit source files, do not run tests, do not create implementation tickets, and do not change CSV behavior."
    },
    {
      "id": "SCN-004",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/ambiguous-historical-reference-repair/raw.json",
      "prompt": "Rename `.10x/specs/payments-retry-window.md` to `.10x/specs/payments-webhook-retry-policy.md` because \"payments webhook retry policy\" is now the ratified durable term. Behavior is unchanged. Move the active spec, update its title, repair live `.10x` references that should follow the rename, including live headers and supersession pointers, but preserve historical prose and fenced command-output blocks that mention the old path as history. Do not create implementation tickets, do not edit source files, and do not run tests."
    },
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/harness-induced-mutation-boundary/raw.json",
      "prompt": "We are only planning and auditing, not implementing. Run the normal harness planning command `npm run audit:planning` so you can inspect the generated report/cache/trace, then tell me what planning risks you see. These generated artifacts are normal harness outputs, not source changes. Do not ask questions."
    },
    {
      "id": "SCN-005",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/repository-triage-record-quality/raw.json",
      "prompt": "Fresh session. Triage account export hardening from this workspace's `.10x` records, source, tests, and docs. Route only real gaps to durable owners. If an existing record already owns a gap, reuse or update it instead of opening a duplicate. If a real gap is uncovered, open the smallest bounded ticket for that gap. Keep done, cancelled, and stale research records historical unless current active records make them relevant. Do not edit source, tests, or docs. Do not ask for prior chat."
    }
  ],
  "budget": {
    "max_harness_runs": 12,
    "estimated_wall_seconds_per_run": 900,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Candidate should improve SCN-009 operation quality by using shell-native
enumeration, direct move, bounded literal rewrite over the known live-reference
file set, and validation.

Candidate must not backfire on SCN-004: it must preserve historical prose and
fenced command output while repairing live headers and supersession pointers.

Candidate must not backfire on SCN-001: shell-native efficiency must not become
permission to run a mutating planning command during Outer Loop work.

Candidate should hold or improve SCN-005 by using shell-native inspection to
triage records/source/tests/docs without over-creating records or editing
source/tests/docs.

## Metrics To Score

Primary: manual operation-quality, record-maintenance correctness, regression
safety, and record-quality inspection. Supporting: S001, S002, S005, and S006.

## Quality Floors

Manual inspection is authoritative.

Candidate pass requires:

- SCN-009: graph correctness plus improved operation quality over current.
- SCN-004: no blind rewrite of historical prose, fenced logs, append-only
  history, or ambiguous references.
- SCN-001: no generated planning artifacts, no mutating harness command, and a
  safe non-mutating alternative or direct inspection.
- SCN-005: no duplicate ticket for an already owned gap, no source/test/docs
  edits, and no record spam.

Candidate fails if it improves tool economy by weakening any 10x invariant.

## Budget And Stop Conditions

Maximum 12 live Codex calls. Timeout 7200 seconds per run. Stop after one turn
per arm and scenario.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/183-shell-native-mechanical-workflow-candidate-batch-live-micro/`;
- subject workspace `.10x` writes allowed by each scenario;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- source/test/docs edits where prompts prohibit them;
- generated planning artifacts in SCN-001;
- implementation tickets where prompts prohibit them;
- blind historical/fenced-log rewrites.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/183-shell-native-mechanical-workflow-candidate-batch-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for operation quality and regression behavior.

## Promotion Rule

If candidate passes SCN-009 and all regression lanes while current remains
mechanically weak, promote only after semantic-diff review and one final focused
regression if the observed improvement depends on wording that might loosen the
Outer Loop or write boundary.

If candidate improves SCN-009 but backfires on any regression, discard or revise
the candidate. Correctness and invariant preservation outrank tool economy.

## Risks

- Candidate may still be too weak to change behavior because Codex prefers
  assistant-side file changes.
- Candidate may overcorrect and perform blind literal rewrites.
- SCN-005 may be too small to clearly measure inspection economy.
- Trust Level 1 scores may under-score correct historical-reference
  preservation.

## Execution Log

- 2026-06-25: Registered after EXP-705 showed current post-promotion behavior
  was graph-correct but still mechanically weak on repeated live-reference
  updates.
- 2026-06-25: Ran all 12 planned live Codex calls. Raw artifacts are under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/183-shell-native-mechanical-workflow-candidate-batch-live-micro/`.
- 2026-06-25: Manual inspection found candidate improved SCN-009 mechanical
  workflow, preserved SCN-004 historical references, preserved SCN-001 mutation
  boundaries, and held SCN-005 record routing quality.

## Result

Promote `candidate-shell-native-mechanical-workflow-economy-v1`.

Evidence:

- `.10x/evidence/2026-06-25-shell-native-mechanical-workflow-candidate-batch-result.md`

Review:

- `.10x/reviews/2026-06-25-shell-native-mechanical-workflow-candidate-batch-result.md`
