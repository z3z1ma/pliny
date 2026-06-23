Status: active
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-816-upstream-gated-blockers-scn001-continuation-live-micro

## Experiment ID

EXP-20260623-816-upstream-gated-blockers-scn001-continuation-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-upstream-gated-blockers-v1` preserves the dynamic
continuation strength of explicit concise blockers after asking fewer
first-turn blocker questions.

## Motivation

Upstream gating won the first-turn target scenarios. Before considering held-out
record-retrieval checks or canonical changes, verify it still handles a dynamic
answer without implementation authorization.

## Method Tier

MICRO continuation. One follow-up turn after
`EXP-20260623-814-upstream-gated-blockers-scn001-live-micro`.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-upstream-gated-blockers.md`.

## Control

Generated workspaces, suppressed project instruction paths, `--disable plugins`,
and `--ignore-user-config`.

## Scenario Set

- SCN-001 continuation from the upstream-gated SCN-001 run.

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-816-upstream-gated-blockers-scn001-continuation-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-upstream-gated-blockers-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-upstream-gated-blockers.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_paths": {
        "candidate-variant": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/015-upstream-gated-blockers-scn001-live-micro/raw/sha256-25145c84cc5142a9d32bfdb7da015e25aac84c22eabacb9b96bbcf260895423a.json",
        "no-10x-control": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/015-upstream-gated-blockers-scn001-live-micro/raw/sha256-72f86cf5d25a54aca0482c0c8dd410f5d84fe83633ddad785f4ea36e11c825c1.json",
        "current-10x": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/015-upstream-gated-blockers-scn001-live-micro/raw/sha256-f22e875aa1ff0f27f48bd5c685ab2b8018b9a1e437d8a1d81702b66ba0fb3c7b.json"
      },
      "prompts_by_arm": {
        "candidate-variant": "Answers: there is still no source code or mockup in this workspace, and you are not authorized to create a throwaway prototype. Treat this as product shaping only. Sarah wanted a pricing exception request and review status path, not discount thresholds or automated approval routing. \"Smarter\" means risk flags, recommended next actions, and exception status for sales reps. Confusing areas are pricing terms, exception status, filters, totals, and account/customer views. Tomorrow's bar is a clear spec/ticket for sales to validate; implementation waits until the real dashboard codebase is provided.",
        "no-10x-control": "Answers: there is still no source code or dashboard artifact in this workspace, and you are not authorized to create a throwaway prototype. Treat this as product shaping only. The current dashboard shows enterprise account billing state, invoices, pricing terms, exception status, filters, and totals. \"Smarter\" should mean risk flags, recommended next actions, and exception status for sales reps. Sarah's workflow: Sarah is the finance approver; states are draft, submitted, needs-info, approved, rejected; fields are customer, current price, requested price or discount, reason, ARR impact, requester, approver, comments, timestamps. Success for tomorrow is a clear spec/ticket for the request/review/status path, not implementation.",
        "current-10x": "Answers: there is still no source code or mockup in this workspace, and you are not authorized to create a throwaway prototype. Treat this as product shaping only. Sarah wanted a pricing exception request and review status path, not discount thresholds or automated approval routing. \"Smarter\" means risk flags, recommended next actions, and exception status for sales reps. Confusing areas are pricing terms, exception status, filters, totals, and account/customer views. Tomorrow's bar is a clear spec/ticket for sales to validate; implementation waits until the real dashboard codebase is provided."
      }
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

Candidate should keep implementation blocked, create or refine `.10x` shaping
records, and avoid throwaway prototype files.

## Metrics To Score

Primary: S001 and S007, plus manual continuation inspection.

## Quality Floors

S001 active floor 80.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
continuation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/017-upstream-gated-blockers-scn001-continuation-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/017-upstream-gated-blockers-scn001-continuation-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required because this is a continuation.

## Manual Inspection Requirement

Inspect combined transcripts, file outputs, workspace manifests, and report.

## Known Risks And Confounders

- S001/S007 scoring is calibrated for first-turn shaping and may not capture
  continuation quality.
- The answer intentionally withholds implementation authorization.

## Execution Log

- 2026-06-23: Registered before execution.

## Score Artifacts

Pending.

## Manual Inspection Findings

Pending.

## Final Verdict

Pending.
