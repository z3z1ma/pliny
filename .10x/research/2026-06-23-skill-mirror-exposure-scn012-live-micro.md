Status: done
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-853-skill-mirror-exposure-scn012-live-micro

## Experiment ID

EXP-20260623-853-skill-mirror-exposure-scn012-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-skill-mirror-exposure-gate-v1` improves retrospective
closure by ensuring a newly created skill is exposed in the existing
harness-native `.claude/skills/` directory, not only recorded under
`.10x/skills/`.

## Motivation

`SKILL.md` already says active skills must be exposed to the execution engine,
but recent retrospective extraction work exercises this obligation indirectly.
This MICRO checks whether the current protocol remembers the exposure step when
the skill is created during ticket closure.

## Method Tier

MICRO using a tracked retrospective closure seed.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-skill-mirror-exposure-gate.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-012: retrospective extraction with a reusable operational procedure, a
  naming convention, an out-of-scope follow-up, and an existing
  `.claude/skills/` native skills directory.

Seed:

- `autoresearch/fixtures/live-seeds/skill-mirror-exposure/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-853-skill-mirror-exposure-scn012-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-skill-mirror-exposure-gate-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-skill-mirror-exposure-gate.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-012",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/skill-mirror-exposure/raw.json",
      "prompt": "Finish closure for `.10x/tickets/2026-06-23-ledger-import-parent.md`. The child evidence and review pass. Preserve the retrospective fixture procedure, `sourceRef` naming convention, and archive malformed-currency follow-up in the correct durable record types. The workspace has an existing harness-native skills directory at `.claude/skills/`. Do not modify source files."
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

Current may already pass because `SKILL.md` explicitly requires active skills to
be mirrored to harness-native directories. Candidate should pass only if it
creates a valid `.10x` skill and a coherent `.claude/skills` exposure copy
without speculative mirrors.

## Metrics To Score

Primary: manual skill-source and mirror inspection, S008, S002, and S006.

## Quality Floors

Manual inspection overrides scores. Automated S002/S006/S008 are Trust Level 1
shape checks and may undercount valid skill mirror behavior.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one closure
turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/053-skill-mirror-exposure-scn012-live-micro/`;
- `.10x/skills/`, `.claude/skills/`, `.10x/knowledge/`, `.10x/tickets/`, and
  ticket status updates inside the subject workspace;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- source files.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/053-skill-mirror-exposure-scn012-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for skill source/mirror coherence.

## Manual Inspection Requirement

Pass an arm only if it:

- creates a valid `.10x/skills/<slug>/SKILL.md` source for the repeatable Ledger
  fixture procedure;
- exposes a matching skill under `.claude/skills/<slug>/SKILL.md`;
- does not create speculative mirrors for absent harnesses;
- routes `sourceRef` to knowledge and archive malformed-currency coverage to a
  follow-up ticket;
- closes tickets only if those retrospective obligations are owned and coherent;
- avoids source edits.

Fail if it creates only one skill copy, creates divergent source/mirror content,
leaves procedure learning only in chat/knowledge, or edits source files.

## Promotion Criteria

Positive candidate-over-current signal should trigger promotion review for a
narrow closure-time skill exposure rule. Null versus current should discard.

## Known Risks And Confounders

- Current `SKILL.md` already contains a skill exposure rule, so this may be a
  null regression run.
- The scenario's parent ticket explicitly names the mirror expectation, which
  may help all 10x arms.
- The no-10x control has inherited `.10x` removed and cannot be compared on
  record-graph behavior in the same way.

## Execution Log

- 2026-06-23: Registered after the redacted evidence capture null result. This
  tests whether retrospective skill creation remembers harness-native exposure.
- 2026-06-23: Ran one live Codex sample for each arm. Automated Trust Level 1
  scores: current-10x `S002=85,S006=85`, candidate-variant `S002=85,S006=85`,
  no-10x-control `S002=50,S006=50`.
- 2026-06-23: Manual inspection found current-10x and candidate-variant both
  created a valid `.10x/skills/ledger-import-test-fixtures/SKILL.md` source and
  byte-identical `.claude/skills/ledger-import-test-fixtures/SKILL.md` mirror.
  Both also routed `sourceRef` to knowledge, opened archive malformed-currency
  follow-up tickets, closed the parent and child tickets, and avoided source
  edits.
- 2026-06-23: Discarded `candidate-skill-mirror-exposure-gate-v1` as null
  versus current.

## Results

Automated score vectors:

- current-10x: `S002=85`, `S006=85`
- candidate-variant: `S002=85`, `S006=85`
- no-10x-control: `S002=50`, `S006=50`

Manual result:

- no-10x-control: failed the 10x skill shape. It created a skill-like source at
  `.10x/skills/ledger-import-fixture-procedure.md` instead of
  `.10x/skills/<slug>/SKILL.md`, although it did create a `.claude` mirror.
- current-10x: pass. It created
  `.10x/skills/ledger-import-test-fixtures/SKILL.md`, exposed
  `.claude/skills/ledger-import-test-fixtures/SKILL.md`, and the two files were
  byte-identical. It created knowledge for `sourceRef`, opened the archive
  malformed-currency follow-up, moved parent and child tickets to `done/`, and
  changed no source files.
- candidate-variant: pass. It created the same valid skill source and
  byte-identical `.claude` mirror, created knowledge, opened the follow-up,
  moved parent and child tickets to `done/`, and changed no source files.

Canonical guard:

- `SKILL.md` unchanged during the run.
- `autoresearch/program.md` unchanged during the run.

Evidence:

- `.10x/evidence/2026-06-23-skill-mirror-exposure-scn012-live-micro.md`

## Conclusions

Discard `candidate-skill-mirror-exposure-gate-v1`. Current canonical
`SKILL.md` already remembers the skill exposure obligation during retrospective
closure when a `.claude/skills/` target is present. The run is useful as a
regression check but does not support adding another rule.

The next queued hypothesis should move away from retrospective skill exposure
and test duplicate-ticket prevention under explicit "open a ticket" pressure.
