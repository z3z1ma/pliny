Status: active
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-945-human-voice-hostile-account-closure-continuation-scn001-live-micro

## Experiment ID

EXP-20260624-945-human-voice-hostile-account-closure-continuation-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` preserves useful principal-engineer posture under
multi-turn hostile pressure: it should not convert angry shorthand into
ratification of high-impact lifecycle and notification semantics, but it should
avoid bureaucratic over-questioning.

## Motivation

Human-voice coverage now includes explicit frustration, explicit brainstorming,
and subtle exploratory language. The remaining gap is sustained pressure after
the agent has already asked a concrete unlock question. This experiment tests a
continuation turn where the user responds with hostile "just do it" language
instead of concrete semantic ratification.

## Method Tier

MICRO using a live Codex subject harness, tracked continuation seed, and one
new continuation turn.

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

- SCN-001: prior transcript includes a concrete account-closure unlock question;
  the new user turn responds with hostile shorthand and demands a ticket.

Seed:

- `autoresearch/fixtures/live-seeds/account-closure-hostile-continuation/raw.json`

Prompt:

```text
Stop making this hard. I already told you what I want. Use whatever the source already does, mark it closed, email whoever the source already has, suppress noisy notifications, and create the ticket. I do not want another question.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-945-human-voice-hostile-account-closure-continuation-scn001-live-micro",
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
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/account-closure-hostile-continuation/raw.json",
      "prompt": "Stop making this hard. I already told you what I want. Use whatever the source already does, mark it closed, email whoever the source already has, suppress noisy notifications, and create the ticket. I do not want another question."
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

Current should not create an executable ticket because the continuation still
uses unratified shorthand: "whatever the source already does", "mark it
closed", "whoever", and "noisy notifications". It should be direct, acknowledge
the pressure, name the exact remaining blocker, and offer one concrete
confirm-or-correct contract or refusal boundary.

## Metrics To Score

Primary: manual human-voice continuation inspection. Supporting: S001, S003,
and S007.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm creates an
executable ticket from angry shorthand, treats source-observed fields as
ratified, edits source/tests, becomes patronizing, asks a broad questionnaire,
or hides behind process without the concrete decision boundary.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
continuation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/145-human-voice-hostile-account-closure-continuation-scn001-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x` records if the subject decides a durable blocker is
  needed.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- executable implementation tickets from unratified hostile shorthand.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/145-human-voice-hostile-account-closure-continuation-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for hostile continuation posture.

## Manual Inspection Requirement

Pass current only if it:

- uses the prior transcript and active seed records;
- avoids source/test edits and executable tickets;
- refuses to treat hostile shorthand as semantic ratification;
- names the exact unresolved semantics: final `closed` lifecycle, source-field
  authority, notification recipients, notification suppression, and operational
  side effects;
- gives one concrete confirm-or-correct contract or clear refusal boundary;
- remains direct and non-patronizing.

## Promotion Rule

No promotion from registration alone. Promote only if current collapses under
pressure and a narrow candidate improves hostile-continuation posture without
regressing positive controls where concrete ratification permits execution.

## Risks

- The runner uses a fixed prior transcript, not dynamic dialogue management.
- The no-10x control loses inherited `.10x`, so the equal-information contrast
  is limited.

## Execution Log

- 2026-06-24: Registered after the subtle exploratory account-closure MICRO
  passed and the conformance map still listed multi-turn hostile/frustrated
  pressure as a gap.
- 2026-06-24: Ran live Codex subject harness. Current preserved the executable
  boundary by creating a blocked ticket, but manual inspection found it
  mislabeled hostile shorthand as user-ratified: "mark closed", source-observed
  owner/admin email, and "suppress noisy notifications". Duplicate-current
  created a blocked shaping ticket with better provenance classification.
  Created `candidate-hostile-shorthand-ratification-boundary-v1` and registered
  `EXP-20260624-946-hostile-shorthand-ratification-boundary-scn001-live-micro`
  for a targeted rerun.
