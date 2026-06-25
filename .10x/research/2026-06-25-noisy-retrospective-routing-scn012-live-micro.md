Status: active
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-982-noisy-retrospective-routing-scn012-live-micro

## Experiment ID

EXP-20260625-982-noisy-retrospective-routing-scn012-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can route noisy retrospective learning into the
right durable record types without turning one-off execution noise into skills
or knowledge. The agent should identify one operational procedure, two
conceptual vocabulary facts, one separate follow-up, and several non-durable
noise items.

## Motivation

Retrospective coverage is now strong-partial after blocked-run and
lower-assistance ACME cases. The remaining gap is noisier skill-versus-knowledge
routing, where records contain both real durable learning and tempting
one-off/debug observations.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: duplicate canonical `SKILL.md` conformance-probe arm. No
  candidate overlay is under test.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-012: settlement reconciliation preview child has pass evidence and review.
  The retrospective notes contain a true repeatable test procedure, two durable
  vocabulary facts, one out-of-scope follow-up, and local one-off noise. The
  workspace contains `.claude/skills/`, so a real skill should be mirrored there
  but conceptual knowledge should not be mirrored as a skill.

Seed:

- `autoresearch/fixtures/live-seeds/noisy-retrospective-routing/raw.json`

Prompt:

```text
Finish the settlement reconciliation preview closure only if the child evidence, review, and retrospective obligations are coherent. The execution notes are noisy: preserve durable learning in the right 10x record types, expose any real reusable skill to the existing `.claude/skills/` directory, and do not turn one-off local noise into skills or knowledge. Do not edit implementation files.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-982-noisy-retrospective-routing-scn012-live-micro",
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
      "instruction_source": "SKILL.md duplicate conformance probe",
      "instruction_path": "SKILL.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-012",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/noisy-retrospective-routing/raw.json",
      "prompt": "Finish the settlement reconciliation preview closure only if the child evidence, review, and retrospective obligations are coherent. The execution notes are noisy: preserve durable learning in the right 10x record types, expose any real reusable skill to the existing `.claude/skills/` directory, and do not turn one-off local noise into skills or knowledge. Do not edit implementation files."
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

Current should create a settlement replay skill for tracked NDJSON fixtures,
frozen settlement date `2026-04-30`, and offline processor replay adapter; mirror
that skill under `.claude/skills/`; create/update knowledge for `settlementRef`
and `pending_release` vocabulary; open a separate historical FX rounding
follow-up; ignore the local `nr` alias, one-off `--runInBand`, and Mara log
preference; then close child and parent only if those obligations are coherent.

## Metrics To Score

Primary: manual noisy retrospective routing inspection. Supporting: S002, S006,
and S008.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm creates generic
skills for all notes, turns one-off noise into durable knowledge, misses the
procedure skill, misses conceptual knowledge, misses the FX follow-up, mirrors
knowledge as a skill, closes before retrospective obligations have owners, or
edits implementation files.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one closure
and retrospective routing turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/182-noisy-retrospective-routing-scn012-live-micro/`;
- subject workspace `.10x` records for tickets, skills, knowledge, evidence, or
  reviews;
- subject workspace `.claude/skills/` mirror of a real skill;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace implementation files;
- skills or knowledge for local one-off noise.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/182-noisy-retrospective-routing-scn012-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for noisy retrospective routing quality.

## Manual Inspection Requirement

Pass an arm only if it:

- creates or updates a project skill for settlement replay with tracked NDJSON
  fixtures, frozen date `2026-04-30`, and offline processor replay adapter;
- mirrors that real skill under `.claude/skills/`;
- creates or updates knowledge for `settlementRef` and `pending_release`;
- opens a separate follow-up ticket for historical FX rounding tolerance;
- does not create skills or knowledge for the `nr` alias, one-off
  `--runInBand`, or Mara log preference;
- closes child and parent only after those durable owners exist, or leaves them
  active/blocked with a precise missing obligation;
- avoids implementation edits.

Fail if it routes all notes into a generic retrospective note, creates a skill
for conceptual vocabulary, mirrors conceptual knowledge as a skill, omits the
real skill mirror, closes while obligations are missing, or edits source.

## Promotion Rule

No behavioral candidate is under test. If current fails this noisy routing case,
create a narrow candidate around noisy retrospective routing and rerun the
positive skill-vs-knowledge control before promotion. If current passes, update
coverage only.

## Risks

- `.claude/skills/` mirroring has existing coverage; this run is primarily about
  noisy routing rather than native skill exposure.
- no-10x-control is likely weak contrast because `.10x` is stripped.

## Execution Log

- 2026-06-25: Registered after live-authored cold-start coverage moved the next
  runnable gap to noisy retrospective skill-versus-knowledge routing.
