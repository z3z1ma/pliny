Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-710-source-code-inspection-economy-live-micro

## Experiment ID

EXP-20260625-710-source-code-inspection-economy-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: canonical `SKILL.md` should induce a simple mechanical workflow for
read-only source inspection without scenario-level prompting. When the user asks
for an answer that requires locating source authority across records and code,
current 10x should use repo-native inventory/search and targeted reads instead
of tailspinning through assistant-side file browsing.

## Motivation

EXP-706 through EXP-709 improved shell-native mechanical workflow economy for
record maintenance. The remaining gap is broader: 10x should encourage the
simple mechanical workflow whenever it is the right tool, including read-only
source questions. This matters because models often waste time and risk missing
authority when they use sequential read/find tool loops instead of a few
bounded shell-native searches.

The scenario prompt must not mention bash, `rg`, one-liners, shell-native tools,
or mechanical workflow. A pass must come from canonical 10x behavior.

## Method Tier

MICRO using a live Codex subject harness and a tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus a no-op sanity overlay.

## Control

Runner-shaped conformance probe. Compare current-10x to the minimal control and
the no-op candidate overlay, but the main verdict is current canonical behavior.

## Scenario Set

1. SCN-003 source-code inspection economy:
   `autoresearch/fixtures/live-seeds/source-code-inspection-economy/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-710-source-code-inspection-economy-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 2,
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
      "instruction_source": "SKILL.md plus no-op sanity overlay",
      "base_instruction_path": "SKILL.md",
      "instruction_text": "No additional behavior changes. This arm exists only for post-promotion sanity comparison."
    }
  ],
  "scenarios": [
    {
      "id": "SCN-003",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/source-code-inspection-economy/raw.json",
      "prompt": "Fresh session. Inspect this workspace's records and source to answer: Which source path owns invoice status summary behavior, what statuses can it return, and which source files define blocked and aging semantics? Also call out any tempting but non-authoritative source you deliberately ignored. Keep the answer concise and cite paths. Do not edit files, run tests, or open records or tickets."
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

Current 10x should:

- inspect `.10x` records before answering;
- locate source authority with repo-native inventory/search plus targeted reads;
- answer that `src/billing/statusSummary.js` owns summary behavior and delegates
  classification to `src/billing/invoiceStatus.js`;
- identify statuses `paid`, `blocked`, `overdue`, `due_soon`, and `open`;
- cite blocked semantics in `src/billing/rules/holdRules.js`;
- cite aging semantics in `src/billing/rules/agingRules.js`;
- call out `src/ui/invoiceLabels.js` as tempting but non-authoritative;
- avoid writes, tests, new records, and tickets.

## Metrics To Score

Primary: manual operation quality and source/record answer correctness.
Supporting: S001, S002, S003, S005, and S006.

## Quality Floors

Manual inspection is authoritative.

Current fails if:

- it edits files, runs tests, or opens records/tickets;
- it answers from fixture names, UI labels, or guesses instead of source and
  records;
- it misses the ownership path, status set, blocked rules, or aging rules;
- it uses a repetitive assistant-side file browsing pattern where a small
  repo-native search would have enumerated the relevant source set.

Using a few targeted reads after repo-native discovery is acceptable. The issue
is not that every read must be shell-based; the issue is using slow sequential
assistant-side navigation when the workspace itself can answer the question
with bounded inventory/search.

## Budget And Stop Conditions

Maximum 6 live Codex calls. Timeout 7200 seconds per run. Stop after two
repetitions per arm.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/187-source-code-inspection-economy-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test/docs edits;
- subject workspace `.10x` record edits;
- tests, build outputs, generated artifacts, new tickets, or new records inside
  the subject workspace.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/187-source-code-inspection-economy-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required.

## Promotion Rule

If current passes both repetitions, keep the coverage-map status as stronger
for read-only source inspection. If current is correct but operation quality is
weak, write a targeted candidate that strengthens source-inspection mechanical
workflow without weakening safety or encouraging blind shell rewrites.

## Risks

- The existing `Mechanical Tool Economy` section may already be enough for
  current but not for no-10x control.
- One source-inspection seed does not prove behavior across large repos.
- Trust Level 1 scores may not capture tool workflow quality; manual inspection
  decides.

## Execution Log

- 2026-06-25: Registered after the user clarified that simple mechanical
  workflow should be encouraged by 10x itself rather than by explicit scenario
  prompting.
- 2026-06-25: Ran 6 live Codex calls. Raw artifacts are under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/187-source-code-inspection-economy-live-micro/`.
- 2026-06-25: Manual inspection found current-10x used shell-native `rg`/`sed`
  source inspection, answered correctly, and produced no subject workspace
  writes. One current repetition over-read fixtures/tests and repeated several
  files with `nl`, which is a residual efficiency issue but not a failure of
  this gate.

## Result

Pass.

Evidence:

- `.10x/evidence/2026-06-25-source-code-inspection-economy-result.md`

Review:

- `.10x/reviews/2026-06-25-source-code-inspection-economy-result.md`
