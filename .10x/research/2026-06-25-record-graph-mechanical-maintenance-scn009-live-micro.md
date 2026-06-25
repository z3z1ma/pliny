Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-974-record-graph-mechanical-maintenance-scn009-live-micro

## Experiment ID

EXP-20260625-974-record-graph-mechanical-maintenance-scn009-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can handle dense record path maintenance
correctly and economically: move one `Status: done` ticket to `tickets/done/`,
repair many unambiguous live references, preserve historical mentions and
fenced command output, validate the result, and avoid slow record-by-record
manual editing when a simple mechanical operation is safe.

## Motivation

The conformance map marks record graph maintenance correctness as strong, with
remaining upside in efficiency and mechanical-operation quality. Prior runs
proved current can move, rename, delete, and selectively repair records. This
MICRO asks whether the subject uses pragmatic mechanics when the path rewrite is
dense and mostly unambiguous while still protecting historical context.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: duplicate canonical `SKILL.md` conformance-probe arm. No
  candidate overlay is under test.

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
Perform payout export record maintenance only. Move `.10x/tickets/2026-06-25-align-payout-export-csv.md` to `.10x/tickets/done/2026-06-25-align-payout-export-csv.md` because the ticket is already `Status: done`. Repair live `.10x` references that should follow the terminal move across active specs, tickets, evidence, reviews, and knowledge. Preserve historical prose and fenced command-output blocks that mention the old top-level path as history. Use the simplest reliable mechanical workflow you think is appropriate for this many repeated path references, then validate that no stale live references remain. Do not edit source files, do not run tests, do not create implementation tickets, and do not change CSV behavior.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-974-record-graph-mechanical-maintenance-scn009-live-micro",
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
      "instruction_source": "SKILL.md duplicate conformance probe",
      "instruction_path": "SKILL.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-009",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/record-graph-mechanical-maintenance/raw.json",
      "prompt": "Perform payout export record maintenance only. Move `.10x/tickets/2026-06-25-align-payout-export-csv.md` to `.10x/tickets/done/2026-06-25-align-payout-export-csv.md` because the ticket is already `Status: done`. Repair live `.10x` references that should follow the terminal move across active specs, tickets, evidence, reviews, and knowledge. Preserve historical prose and fenced command-output blocks that mention the old top-level path as history. Use the simplest reliable mechanical workflow you think is appropriate for this many repeated path references, then validate that no stale live references remain. Do not edit source files, do not run tests, do not create implementation tickets, and do not change CSV behavior."
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

Current should use direct filesystem move plus `rg`-style discovery and a
targeted mechanical rewrite or equivalently compact workflow for unambiguous
live references. It should then manually preserve or repair the few ambiguous
historical contexts, validate stale references, and avoid creating records or
editing source.

## Metrics To Score

Primary: manual record-maintenance correctness and operation-quality
inspection. Supporting: S002, S005, and S006.

## Quality Floors

Manual inspection is authoritative. Pass only if current:

- moves the child ticket to `.10x/tickets/done/2026-06-25-align-payout-export-csv.md`;
- leaves no done-status child ticket at the top-level path;
- repairs live references in active spec, parent ticket, evidence, review, and
  knowledge records to the terminal path;
- preserves historical prose and fenced command output in the research record;
- validates the remaining old-path references and classifies any survivors as
  historical;
- avoids source/test edits, test execution, implementation tickets, and CSV
  behavior changes.

Operation-quality concern if an arm performs many repetitive individual edits
without using simple search/move/rewrite mechanics for the dense unambiguous
references. That concern is not a behavior failure by itself unless it causes
missed references, broad historical corruption, or materially wasteful process
that a concise `SKILL.md` instruction could prevent.

## Budget And Stop Conditions

Maximum 6 live Codex calls. Timeout 7200 seconds per run. Stop after two
repetitions per arm.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/174-record-graph-mechanical-maintenance-scn009-live-micro/`;
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

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/174-record-graph-mechanical-maintenance-scn009-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for operation quality and selective historical preservation.

## Manual Inspection Requirement

Pass current only if the live graph is coherent after the move and old-path
survivors are exclusively historical prose or fenced command output. Record an
operation-quality concern if current achieves correctness through needless
one-off edits rather than compact mechanical maintenance.

## Promotion Rule

No behavioral candidate is under test. If current repeatedly passes correctness
but shows material operation-quality waste, create a narrow candidate that
recommends direct filesystem moves, `rg` discovery, mechanical replacement for
unambiguous live path strings, and post-rewrite validation while preserving the
existing warning against blind historical rewrites.

## Risks

- The prompt explicitly mentions a mechanical workflow. Future variants can
  reduce assistance if current passes.
- Operation quality is partly subjective. Do not promote unless the transcript
  shows a repeated, concrete inefficiency with likely downstream cost.

## Execution Log

- 2026-06-25: Registered after record graph correctness coverage became strong
  and the researcher backlog identified mechanical-operation quality as the
  remaining record graph maintenance gap.
- 2026-06-25: Ran six live Codex subject samples into
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/174-record-graph-mechanical-maintenance-scn009-live-micro/`.
  `canonical_guard.json` reported `SKILL.md` and `autoresearch/program.md`
  unchanged.
- 2026-06-25: Manual inspection found current `SKILL.md` passed. Both current
  repetitions used compact mechanical maintenance: `rg` discovery, direct
  `mv`, `perl` path rewrites over the unambiguous live-reference file set, and
  post-rewrite `rg` validation.

## Findings

- Current moved the child ticket to
  `.10x/tickets/done/2026-06-25-align-payout-export-csv.md` in both
  repetitions and left no top-level child ticket file behind.
- Current repaired live references in the active spec, parent ticket headers and
  acceptance text, evidence, review, and knowledge records.
- Current preserved old-path mentions in the historical research record and in
  the parent ticket's append-only progress log. Each current repetition also
  appended a completion note or final validation stating that live references
  now use the terminal path.
- Current did not edit source files, did not run tests, did not create
  implementation tickets, and did not change CSV behavior.
- Duplicate-current produced equivalent terminal move and live-reference repair.
  One duplicate-current repetition left the original parent progress note
  without an appended resolution note, which is acceptable as duplicate-current
  telemetry but not a reason to promote.
- Trust Level 1 assigned S004=65 and S006=45 to current because the heuristic
  scorer does not distinguish path-maintenance success plus preserved historical
  references from stale closure references. Manual inspection is authoritative.

## Conclusions

Current `SKILL.md` passes this record graph mechanical-maintenance MICRO. The
remaining record graph maintenance gap named in the conformance map is now
covered for dense terminal-ticket path movement: current used direct filesystem
movement, search, mechanical rewrite, and validation without broad historical
corruption.

No `SKILL.md` promotion is justified. The narrow operational instruction that
might have been promoted is already reflected in current behavior under this
probe.

Supporting records:

- `.10x/evidence/2026-06-25-record-graph-mechanical-maintenance-result.md`
- `.10x/reviews/2026-06-25-record-graph-mechanical-maintenance-result.md`
