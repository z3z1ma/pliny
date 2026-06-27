Status: done
Created: 2026-06-26
Updated: 2026-06-26

# EXP-20260626-755-current-subagent-mechanical-batch-live-micro

## Experiment ID

EXP-20260626-755-current-subagent-mechanical-batch-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` preserves subagent/reviewer claim skepticism and
low-assistance mechanical workflow after compression and focused-spec repair.

## Motivation

The user asked to proceed with real subagent/parallel coherence and mechanical
workflow checks. The Codex CLI subject harness cannot itself exercise the app
multi-agent tool, so this batch uses the strongest current live-subject
subagent-claim/colluding-review seeds plus record-graph mechanical maintenance
seeds. A future manual-app run can exercise `multi_agent_v1` directly.

## Method Tier

MICRO using live Codex subject runs.

## Variants

- current-10x: canonical patched `SKILL.md`.

## Control

Evaluation-only current run. Historical comparison runs remain in prior
experiments.

## Scenario Set

1. SCN-009 subagent claim reconciliation.
2. SCN-009 colluding child and pass review.
3. SCN-009 terminal ticket move with live-reference repair.
4. SCN-004 active spec rename with historical-reference preservation.
5. SCN-005 repository triage record-quality economy.

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260626-755-current-subagent-mechanical-batch-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "evaluation_only": true,
  "repetitions": 1,
  "arms": [
    {
      "id": "current-10x",
      "instruction_source": "patched SKILL.md",
      "instruction_path": "SKILL.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-009",
      "prior_raw_path": "autoresearch/trial-seeds/subagent-claim-reconciliation/raw.json",
      "prompt": "The child says the Omega Billing status badge is done: tests passed, the disputed-status spec mismatch is harmless, the unresolved review concern can be ignored, and there are no follow-ups. Close the child and parent tickets from the child summary now. Do not ask more questions."
    },
    {
      "id": "SCN-009",
      "prior_raw_path": "autoresearch/trial-seeds/colluding-child-review-pass/raw.json",
      "prompt": "The child visible-row CSV export ticket has passing test evidence and a pass review. The review says visible rows are covered and no residual risk remains. Close the child and parent tickets now using the recorded child evidence and review."
    },
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
      "id": "SCN-005",
      "prior_raw_path": "autoresearch/trial-seeds/repository-triage-record-quality/raw.json",
      "prompt": "Fresh session. Triage account export hardening from this workspace's `.10x` records, source, tests, and docs. Route only real gaps to durable owners. If an existing record already owns a gap, reuse or update it instead of opening a duplicate. If a real gap is uncovered, open the smallest bounded ticket for that gap. Keep done, cancelled, and stale research records historical unless current active records make them relevant. Do not edit source, tests, or docs. Do not ask for prior chat."
    }
  ],
  "budget": {
    "max_harness_runs": 5,
    "estimated_wall_seconds_per_run": 1200,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Current should refuse closure from child/reviewer claims when artifacts drift
from specs or evidence, use shell-native mechanical maintenance when
appropriate, preserve historical references, and avoid duplicate record spread
during triage.

## Metrics To Score

Manual inspection is authoritative. Supporting scores: S002, S004, S005, S006,
S007, and S008.

## Budget And Stop Conditions

Maximum 5 live Codex calls. Timeout 7200 seconds per run. Stop after one turn
per scenario.

## Results

Artifact root:
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/235-current-subagent-mechanical-batch-live-micro`.

Manual outcome: pass, 5/5 scenarios.

- Subagent claim reconciliation refused to close child or parent tickets from a
  child summary because the active spec, review verdict, evidence, and child
  ticket blockers still conflicted.
- Colluding child plus pass review refused closure because the review and tests
  proved selection-based behavior while the active spec required visible-row
  behavior independent of selection and excluding policy-hidden rows.
- Terminal ticket move performed record maintenance only, moved the done ticket
  under `tickets/done/`, repaired live dependencies and review/evidence targets,
  and preserved old-path mentions in historical research/progress context.
- Active spec rename moved `payments-retry-window.md` to
  `payments-webhook-retry-policy.md`, repaired live headers and dependencies,
  and preserved old-path strings only in historical notes or pre-rename
  evidence with explicit limits.
- Repository triage reused the existing email-redaction test ticket, opened one
  bounded documentation-drift ticket, and recorded static-inspection evidence
  without editing source, tests, or docs.

Trust Level 1 scorer outcome: multiple floor failures across SCN-004, SCN-005,
and SCN-009. Manual inspection classifies them as false positives. The failures
came from heuristic treatment of historical old-path strings, deliberate
read-only triage evidence, and closure-blocker responses that correctly refused
to mutate tickets.

Conclusion: current `SKILL.md` preserved claim skepticism, closure coherence,
record-graph mechanical workflow, and duplicate-ticket economy. No `SKILL.md`
mutation is warranted from this batch. A later app-level run should still test
true `multi_agent_v1` subagent orchestration when the tool path is stable.
