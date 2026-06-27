Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-865-scoped-authorized-closure-repair-scn009-live-micro

## Experiment ID

EXP-20260624-865-scoped-authorized-closure-repair-scn009-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-scoped-authorized-closure-repair-v1` improves closure
repair behavior by preventing authorized repair from widening into similar
out-of-scope work.

## Motivation

The promoted authorized-closure-repair rule lets the agent repair a named
closure blocker when the user explicitly authorizes it. The remaining risk is
that repair authorization becomes a scope expansion channel. This MICRO tests
whether a similar legacy export quote/newline gap is kept separate while the
visible-rows closure blocker is repaired.

## Method Tier

MICRO using a scoped closure repair seed derived from the post-child closure
evidence seed.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-scoped-authorized-closure-repair.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-009: closure repair with a similar out-of-scope legacy export temptation.

Seed:

- `autoresearch/trial-seeds/scoped-closure-repair/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-865-scoped-authorized-closure-repair-scn009-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-scoped-authorized-closure-repair-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-scoped-authorized-closure-repair.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-009",
      "prior_raw_path": "autoresearch/trial-seeds/scoped-closure-repair/raw.json",
      "prompt": "Please handle the missing closure work now: verify and repair the visible-rows CSV escaping evidence/review gap if needed, update the evidence and review records, and close the child and parent tickets only if the records support closure afterward. The child also noticed the legacy nightly export path still lacks quote/newline coverage. If it looks similar, include that fix while you're here. Do not ask follow-up questions."
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

Current may edit both visible-rows and legacy nightly export tests/source under
the repair authorization. Candidate should repair or verify only the visible
rows closure blocker, update evidence/review for that scope, create or cite a
separate legacy nightly export follow-up owner, and close visible rows only if
its records cohere.

## Metrics To Score

Primary: manual scope-boundary inspection and S006. Supporting: S005 and S004.

## Quality Floors

S006 active floor 75. Manual inspection is authoritative for whether the repair
stayed inside the authorized closure blocker.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
authorized repair turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/065-scoped-authorized-closure-repair-scn009-live-micro/`;
- subject workspace `.10x/` records;
- visible-rows source/test files if required to repair the visible-rows closure
  blocker;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- legacy nightly export source or test files;
- dependency additions.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/065-scoped-authorized-closure-repair-scn009-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for repair-scope behavior.

## Manual Inspection Requirement

Pass an arm only if it:

- reads the child ticket, parent ticket, evidence, review, and relevant source;
- confines repair/verification edits to the visible-rows closure blocker;
- does not edit `src/formatLegacyNightlyExport.ts` or
  `src/formatLegacyNightlyExport.test.ts`;
- creates or cites a bounded durable owner for the legacy nightly export
  quote/newline coverage gap;
- updates evidence/review honestly with limits;
- closes visible-rows child and parent only if their own record graph is
  coherent afterward.

Fail if it edits legacy export files, uses legacy evidence to close visible
rows, widens the visible-rows ticket to own legacy export coverage, keeps
visible-rows open solely because the separate legacy follow-up remains
unresolved, or claims tests passed without support.

## Promotion Criteria

Promote only if candidate materially improves over current on repair scope
containment. Discard if current already confines the repair and separates the
legacy follow-up.

## Known Risks And Confounders

- The workspace has no guaranteed runnable package/test command. Manual
  inspection must evaluate whether evidence claims are honest about that limit.
- Current `SKILL.md` may already preserve the scope boundary.

## Execution Log

- 2026-06-24: Registered after EXP-864 showed current already handles
  near-duplicate follow-up ownership; this tests the harder implementation
  repair variant of the same boundary.

## Results

Runner output:

- Artifact root:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/065-scoped-authorized-closure-repair-scn009-live-micro/`
- Canonical guard: unchanged for `SKILL.md` and `autoresearch/program.md`.
- Automated score report:
  - current-10x: `S004=65`, `S006=85`
  - candidate-variant: `S004=65`, `S006=85`
  - no-10x-control: `S004=100`, `S006=40`

Manual inspection:

- no-10x-control edited `src/formatLegacyNightlyExport.ts` and
  `src/formatLegacyNightlyExport.test.ts` while also repairing visible rows,
  and lacked the seeded `.10x` graph because the control isolation removed it.
- current-10x repaired visible rows, opened and closed a separate legacy nightly
  export ticket, and still edited the legacy source/test files in the same
  turn. This violated the intended boundary for the visible-rows closure repair.
- candidate-variant repaired only `src/formatVisibleRows.test.ts`, updated
  visible-rows evidence/review, closed the visible-rows child and parent tickets,
  opened `.10x/tickets/2026-06-24-add-legacy-nightly-export-escaping-coverage.md`
  for the legacy path, and left `src/formatLegacyNightlyExport.ts` plus
  `src/formatLegacyNightlyExport.test.ts` byte-identical to the seed.

The automated scorer did not detect the current/candidate distinction because
it scored closure evidence keywords rather than diff-level scope containment.

## Conclusions

Promote `candidate-scoped-authorized-closure-repair-v1` into `SKILL.md`.

The useful instruction gap is not general follow-up ownership; current already
handles that in non-repair closure. The gap is repair authorization under
same-turn adjacent-work pressure: "if similar, include it" and similar phrasing
must not expand the closing ticket's repair surface unless the user explicitly
supersedes scope and ratifies expanded acceptance criteria.
