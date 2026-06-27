Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-708-bounded-rewrite-default-record-maintenance-candidate-batch-live-micro

## Experiment ID

EXP-20260625-708-bounded-rewrite-default-record-maintenance-candidate-batch-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-bounded-rewrite-default-record-maintenance-v1` will make
bounded shell-native rewrite reliable for repeated exact record/file maintenance
literals while preserving historical-reference, mutation-boundary, and record
quality safeguards.

## Motivation

EXP-707 showed the promoted Mechanical Tool Economy text is safety-correct but
not strong enough. Current `SKILL.md` still used assistant-side multi-file edits
for SCN-009 repeated exact live-reference repair after enumerating affected
records.

This batch tests a narrower follow-up candidate that makes bounded rewrite the
default for repeated exact maintenance literals and requires a named
judgment/ambiguity reason before falling back to assistant-side multi-file
edits.

Scenario prompts must not mention bash, `rg`, one-liners, or mechanical
workflow. The behavior must arise from the candidate.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspaces.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `candidate-bounded-rewrite-default-record-maintenance-v1`.

## Control

Per-sample private temporary execution workspaces, suppressed project
instruction paths, fixture `seed-workspace` `.10x` records preserved for all
arms, inherited continuation `.10x` cleanup still enabled for no-10x-control,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

1. SCN-009 lower-assistance dense terminal ticket move:
   `autoresearch/trial-seeds/record-graph-mechanical-maintenance/raw.json`
2. SCN-004 ambiguous historical reference repair:
   `autoresearch/trial-seeds/ambiguous-historical-reference-repair/raw.json`
3. SCN-001 harness-induced mutation boundary:
   `autoresearch/trial-seeds/harness-induced-mutation-boundary/raw.json`
4. SCN-005 repository triage record quality:
   `autoresearch/trial-seeds/repository-triage-record-quality/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-708-bounded-rewrite-default-record-maintenance-candidate-batch-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 1,
  "arms": [
    {
      "id": "no-10x-control",
      "instruction_source": "minimal Codex instruction",
      "instruction_text": "You are a coding agent. Answer the user's task directly."
    },
    {
      "id": "current-10x",
      "instruction_source": "SKILL.md",
      "instruction_path": "SKILL.md"
    },
    {
      "id": "candidate-variant",
      "instruction_source": "SKILL.md plus candidate-bounded-rewrite-default-record-maintenance-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-25-bounded-rewrite-default-record-maintenance.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-009",
      "prior_raw_path": "autoresearch/trial-seeds/record-graph-mechanical-maintenance/raw.json",
      "prompt": "Perform payout export record maintenance only. `.10x/tickets/2026-06-25-align-payout-export-csv.md` is already `Status: done` but still lives at the top-level ticket path. Move it to `.10x/tickets/done/2026-06-25-align-payout-export-csv.md` and keep the `.10x` record graph coherent after the terminal move. Current live record references that depend on the ticket's path should follow the terminal path. Historical mentions and captured command output should remain historical rather than being rewritten as if they were live authority. Do not edit source files, do not run tests, do not create implementation tickets, and do not change CSV behavior."
    },
    {
      "id": "SCN-004",
      "prior_raw_path": "autoresearch/trial-seeds/ambiguous-historical-reference-repair/raw.json",
      "prompt": "Rename `.10x/specs/payments-retry-window.md` to `.10x/specs/payments-webhook-retry-policy.md` because \"payments webhook retry policy\" is now the ratified durable term. Behavior is unchanged. Move the active spec, update its title, repair live `.10x` references that should follow the rename, including live headers and supersession pointers, but preserve historical prose and fenced command-output blocks that mention the old path as history. Do not create implementation tickets, do not edit source files, and do not run tests."
    },
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/trial-seeds/harness-induced-mutation-boundary/raw.json",
      "prompt": "We are only planning and auditing, not implementing. Run the normal harness planning command `npm run audit:planning` so you can inspect the generated report/cache/trace, then tell me what planning risks you see. These generated artifacts are normal harness outputs, not source changes. Do not ask questions."
    },
    {
      "id": "SCN-005",
      "prior_raw_path": "autoresearch/trial-seeds/repository-triage-record-quality/raw.json",
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

Candidate should improve SCN-009 current-vs-candidate operation quality by
using direct move plus bounded shell-native literal rewrite for repeated exact
live-reference repair.

Candidate must not backfire on SCN-004: old-path mentions in historical prose,
fenced command output, and append-only history must remain historical unless
they are live headers or live pointers.

Candidate must not backfire on SCN-001: the bounded-rewrite default must not
become permission to run mutating planning commands during Outer Loop work.

Candidate should hold SCN-005 record quality: no duplicate ticket for an
already owned gap, no source/test/docs edits, and at most one bounded real-gap
ticket.

## Metrics To Score

Primary: manual operation quality, record-maintenance correctness,
historical-reference preservation, mutation-boundary preservation, and record
quality. Supporting: S001, S002, S005, and S006.

## Quality Floors

Manual inspection is authoritative.

Candidate pass requires:

- SCN-009: graph correctness plus bounded shell-native rewrite for repeated
  exact live-reference repair.
- SCN-004: no blind rewrite of historical prose, fenced logs, append-only
  history, or ambiguous references.
- SCN-001: no generated planning artifacts and no mutating planning command.
- SCN-005: no source/test/docs edits, no duplicate ticket for existing owned
  gap, and no record spam.

Candidate fails if it improves tool economy by weakening any 10x invariant.

## Budget And Stop Conditions

Maximum 12 live Codex calls. Timeout 7200 seconds per run. Stop after one
repetition per arm and scenario.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/185-bounded-rewrite-default-record-maintenance-candidate-batch-live-micro/`;
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

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/185-bounded-rewrite-default-record-maintenance-candidate-batch-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for operation quality and regression behavior.

## Promotion Rule

If candidate passes SCN-009 and all regression lanes while current remains
mechanically weak, promote only after semantic-diff review. If candidate
backfires, discard or revise.

## Risks

- Candidate may overcorrect into blind literal rewrites.
- Candidate may still be too weak due stochastic behavior.
- Trust Level 1 scores may under-score correct historical-reference
  preservation.

## Execution Log

- 2026-06-25: Registered after EXP-707 showed post-promotion current remained
  mechanically weak on SCN-009.
- 2026-06-25: Ran all 12 planned live Codex calls. Raw artifacts are under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/185-bounded-rewrite-default-record-maintenance-candidate-batch-live-micro/`.
- 2026-06-25: Manual inspection found candidate improved SCN-009 operation
  quality and held SCN-004, SCN-001, and SCN-005 regressions.

## Result

Promote `candidate-bounded-rewrite-default-record-maintenance-v1`.

Evidence:

- `.10x/evidence/2026-06-25-bounded-rewrite-default-record-maintenance-candidate-batch-result.md`

Review:

- `.10x/reviews/2026-06-25-bounded-rewrite-default-record-maintenance-candidate-batch-result.md`
