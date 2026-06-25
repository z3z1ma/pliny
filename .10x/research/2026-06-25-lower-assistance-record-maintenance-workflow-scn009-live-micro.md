Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-700-lower-assistance-record-maintenance-workflow-scn009-live-micro

## Experiment ID

EXP-20260625-700-lower-assistance-record-maintenance-workflow-scn009-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` should induce economical mechanical record
maintenance even when the subject prompt does not explicitly recommend a
mechanical workflow. If current tailspins through many repetitive
assistant-side edits or misses references, the candidate command-line economy
overlay should improve operation quality without weakening selective historical
preservation.

## Motivation

The previous dense record-maintenance run passed, but the prompt explicitly
said to use the simplest reliable mechanical workflow. That is not the behavior
we ultimately need. 10x itself should teach agents to use shell-native mechanics
for safe bulk mechanical maintenance because repeated read/write edit loops are
slow and error-prone on dense path maintenance.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `candidate-record-maintenance-command-line-economy-v1`.

## Control

Per-sample private temporary execution workspaces, suppressed project
instruction paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed
workspace copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

The no-10x-control arm is retained for runner consistency but is not meaningful
for the record-maintenance verdict because control isolation removes the seed
`.10x` graph.

## Scenario Set

- SCN-009: dense payout export terminal ticket move. A done child ticket still
  lives at a top-level active path. Active spec, parent, evidence, review, and
  knowledge records have live references to that old path. A research record
  contains historical prose and fenced command output that should preserve the
  old path.

Seed:

- `autoresearch/fixtures/live-seeds/record-graph-mechanical-maintenance/raw.json`

Prompt:

```text
Perform payout export record maintenance only. `.10x/tickets/2026-06-25-align-payout-export-csv.md` is already `Status: done` but still lives at the top-level ticket path. Move it to `.10x/tickets/done/2026-06-25-align-payout-export-csv.md` and keep the `.10x` record graph coherent after the terminal move. Current live record references that depend on the ticket's path should follow the terminal path. Historical mentions and captured command output should remain historical rather than being rewritten as if they were live authority. Do not edit source files, do not run tests, do not create implementation tickets, and do not change CSV behavior.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-700-lower-assistance-record-maintenance-workflow-scn009-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 2,
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
      "instruction_source": "SKILL.md plus candidate-record-maintenance-command-line-economy-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-25-record-maintenance-command-line-economy.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-009",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/record-graph-mechanical-maintenance/raw.json",
      "prompt": "Perform payout export record maintenance only. `.10x/tickets/2026-06-25-align-payout-export-csv.md` is already `Status: done` but still lives at the top-level ticket path. Move it to `.10x/tickets/done/2026-06-25-align-payout-export-csv.md` and keep the `.10x` record graph coherent after the terminal move. Current live record references that depend on the ticket's path should follow the terminal path. Historical mentions and captured command output should remain historical rather than being rewritten as if they were live authority. Do not edit source files, do not run tests, do not create implementation tickets, and do not change CSV behavior."
    }
  ],
  "budget": {
    "max_harness_runs": 6,
    "estimated_wall_seconds_per_run": 900,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Current may already use `rg`, `mv`, and a bounded rewrite because the canonical
skill contains Operational Minimalism and record-reference repair rules. If it
does, the candidate should be discarded as null. If current instead performs
many repetitive assistant-side edits or misses references, candidate should use
the simpler mechanical workflow while preserving historical references.

## Metrics To Score

Primary: manual operation-quality and record-maintenance correctness
inspection. Supporting: S002, S005, and S006.

## Quality Floors

Manual inspection is authoritative. Pass only if current:

- moves the child ticket to
  `.10x/tickets/done/2026-06-25-align-payout-export-csv.md`;
- leaves no done-status child ticket at the top-level path;
- repairs live references in active spec, parent ticket, evidence, review, and
  knowledge records to the terminal path;
- preserves historical prose and fenced command output in the research record;
- validates or otherwise accounts for remaining old-path references;
- avoids source/test edits, test execution, implementation tickets, and CSV
  behavior changes.

Operation-quality failure if current performs materially wasteful repeated
assistant-side read/write/edit loops where a bounded shell-native move and
literal rewrite would be safe, especially if that produces missed references or
unnecessary churn. Operation-quality pass if current uses `rg`/direct move/
bounded rewrite/validation or an equivalently compact mechanical workflow.

## Budget And Stop Conditions

Maximum 6 live Codex calls. Timeout 7200 seconds per run. Stop after two
repetitions per arm.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/176-lower-assistance-record-maintenance-workflow-scn009-live-micro/`;
- subject workspace `.10x` terminal-ticket move and reference repair;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- implementation tickets;
- test execution.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/176-lower-assistance-record-maintenance-workflow-scn009-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for operation quality and selective historical preservation.

## Manual Inspection Requirement

Pass current only if the live graph is coherent after the move and old-path
survivors are exclusively historical prose, append-only progress history, or
fenced command output. Record an operation-quality concern if current achieves
correctness through needless one-off edits rather than compact mechanical
maintenance.

## Promotion Rule

Promote the candidate only if current fails operation quality or correctness and
candidate passes, then rerun relevant historical-reference and closure/reference
repair regressions. If current passes without the explicit prompt hint, discard
or keep the candidate as null; do not add token cost for already-induced
behavior.

## Risks

- Current may already pass, making the candidate null.
- Candidate may overfit to shell one-liners and corrupt historical context.
- Automated S002/S006 may under-score correct preservation of historical old
  paths.

## Execution Log

- 2026-06-25: Registered in direct response to the prompt-assistance concern in
  EXP-974. The key question is whether command-line economy comes from 10x
  itself rather than from scenario wording.
- 2026-06-25: Ran two live Codex repetitions for no-10x-control, current-10x,
  and candidate-variant arms. Raw artifacts are stored under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/176-lower-assistance-record-maintenance-workflow-scn009-live-micro/`.
- 2026-06-25: Manual inspection found current `SKILL.md` passed correctness but
  did not consistently satisfy operation quality. Current repaired the graph in
  both repetitions, but used assistant-side file-change edits for repeated live
  reference updates in both repetitions, and one repetition appears to have
  performed the ticket move through file-change rather than direct `mv`.
- 2026-06-25: Manual inspection found candidate improved the core mechanical
  workflow. Candidate used direct `mv` plus a bounded `perl` literal rewrite
  for live-reference files in both repetitions, excluded the historical research
  record, and then patched ambiguous or stale prose deliberately.

## Results

Current `SKILL.md`:

- moved the ticket to
  `.10x/tickets/done/2026-06-25-align-payout-export-csv.md` in both
  repetitions;
- repaired live references in spec, parent ticket, evidence, review, and
  knowledge records;
- preserved historical old-path mentions in the maintenance research record;
- avoided source edits, tests, implementation tickets, `SKILL.md`, and
  `autoresearch/program.md`;
- did not consistently use shell-native mechanics for the repeated reference
  maintenance.

Candidate:

- performed the move with `mv` and repeated literal reference repair with
  bounded `perl -0pi` replacements in both repetitions;
- preserved the historical research record;
- detected and deliberately patched stale or ambiguous parent/review prose after
  the mechanical replacement;
- avoided source edits, tests, implementation tickets, `SKILL.md`, and
  `autoresearch/program.md`.

No-10x-control changed no workspace files because the control environment
suppressed inherited `.10x`; it is not meaningful for this record-maintenance
verdict.

Trust Level 1 scoring gave current and candidate S004=65/S006=45 in all
canonical arms. Manual inspection overrides those false negatives because the
scorer cannot classify terminal path maintenance plus preserved historical
old-path references.

## Conclusions

Current `SKILL.md` is correct but mechanically inconsistent on the
lower-assistance version of this task. The user concern is valid: without an
explicit scenario hint, current can fall back to repetitive assistant-side
file-change edits for dense record maintenance.

`candidate-record-maintenance-command-line-economy-v1` is promising and should
advance to regression testing. It should not be promoted from this run alone
because the new rule encourages mechanical rewrite, which must prove it does
not corrupt ambiguous historical references, closure repairs, or semantic
content.

Supporting records:

- `.10x/evidence/2026-06-25-lower-assistance-record-maintenance-workflow-result.md`
- `.10x/reviews/2026-06-25-lower-assistance-record-maintenance-workflow-result.md`
