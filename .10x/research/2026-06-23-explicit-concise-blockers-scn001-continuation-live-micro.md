Status: active
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-813-explicit-concise-blockers-scn001-continuation-live-micro

## Experiment ID

EXP-20260623-813-explicit-concise-blockers-scn001-continuation-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: after the subject agent asks first-turn blocker questions,
`candidate-explicit-concise-blockers-v1` handles a dynamic answer by preserving
the unresolved implementation blocker, refining product shape, and avoiding
invented code or business rules.

## Motivation

The operator explicitly raised that follow-up answers cannot be a fixed array
because LLMs ask different questions in different orders. This experiment uses
the actual prior raw artifacts from
`EXP-20260623-811-explicit-concise-blockers-scn001-live-micro` and arm-specific
answers.

## Method Tier

MICRO continuation. One follow-up turn after a live SCN-001 ambiguous request.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-explicit-concise-blockers.md`.

## Control

Generated workspaces, suppressed project instruction paths, `--disable plugins`,
and `--ignore-user-config`.

## Scenario Set

- SCN-001 continuation from the explicit concise blocker SCN-001 run.

Continuation answer policy:

- Answer each arm's actual question set.
- State that there is still no source code and no prototype authorization.
- Provide product/workflow details sufficient to shape a spec/ticket but not to
  implement.

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-813-explicit-concise-blockers-scn001-continuation-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-explicit-concise-blockers-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-explicit-concise-blockers.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_paths": {
        "candidate-variant": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/012-explicit-concise-blockers-scn001-live-micro/raw/sha256-01649465024899f5921136248f8e0d4c4a5d61254b3f695438d92cb77addf689.json",
        "no-10x-control": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/012-explicit-concise-blockers-scn001-live-micro/raw/sha256-22ae90b6a3148a1609bb841793a960c9e0f25374a0b971d6c2050c1bd071b395.json",
        "current-10x": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/012-explicit-concise-blockers-scn001-live-micro/raw/sha256-b5d409bb99b461ee2df7e83b60b32c6967a6015421e24be4885e8389aed3aa5c.json"
      },
      "prompts_by_arm": {
        "candidate-variant": "Answers: there is still no source code or mockup in this workspace, and you are not authorized to create a throwaway prototype. Treat this as product shaping only. \"Smarter\" means risk flags, recommended next actions, and exception status for sales reps. Sarah is the finance approver, not the requester. Pricing exception states are draft, submitted, needs-info, approved, and rejected. Required fields are customer, current price, requested price or discount, reason, ARR impact, requester, approver, comments, and timestamps. Confusing parts are pricing terms, exception status, filters, and totals. Tomorrow's acceptance criteria: produce a clear spec/ticket for the sales-critical request/review/status path; do not implement until the real codebase is provided.",
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

Candidate should keep implementation blocked because the target codebase is
missing, refine the shaped workflow, and avoid inventing thresholds,
auto-approvals, notifications, or prototype files.

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
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/014-explicit-concise-blockers-scn001-continuation-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/014-explicit-concise-blockers-scn001-continuation-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required because this is a continuation.

## Manual Inspection Requirement

Inspect combined transcripts, file outputs, workspace manifests, and report.

## Known Risks And Confounders

- S001/S007 scoring is calibrated for first-turn shaping and may not capture
  continuation quality.
- The answer intentionally withholds implementation authorization, so this does
  not test transition into a fully executable implementation ticket.

## Execution Log

- 2026-06-23: Registered before execution.

## Score Artifacts

Pending.

## Manual Inspection Findings

Pending.

## Final Verdict

Pending.
