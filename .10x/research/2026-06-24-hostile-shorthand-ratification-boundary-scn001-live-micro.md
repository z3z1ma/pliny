Status: active
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-946-hostile-shorthand-ratification-boundary-scn001-live-micro

## Experiment ID

EXP-20260624-946-hostile-shorthand-ratification-boundary-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-hostile-shorthand-ratification-boundary-v1` fixes the
hostile-continuation failure where current creates a blocked account-closure
ticket but labels vague hostile shorthand as user-ratified.

## Motivation

`EXP-20260624-945-human-voice-hostile-account-closure-continuation-scn001-live-micro`
showed current preserved the executable boundary but over-ratified several
high-impact terms inside a blocked ticket. Duplicate-current did better
stochastically, which suggests a narrow instruction can stabilize the desired
classification without changing the broader protocol.

## Method Tier

MICRO using a live Codex subject harness, tracked continuation seed, and one
new continuation turn.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-hostile-shorthand-ratification-boundary.md`.

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
  "experiment_id": "EXP-20260624-946-hostile-shorthand-ratification-boundary-scn001-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-hostile-shorthand-ratification-boundary-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-hostile-shorthand-ratification-boundary.md"
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

Candidate should avoid executable tickets and source edits. If it creates a
blocked shaping ticket, it should classify hostile shorthand as requested,
candidate, source-observed, or blocked rather than user-ratified. It should not
place vague terms in executable acceptance criteria.

## Metrics To Score

Primary: manual hostile-shorthand assumption-provenance inspection. Supporting:
S001, S003, and S007.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if candidate labels
"whatever the source does", "mark it closed", "whoever", or "noisy
notifications" as user-ratified; creates an executable ticket; edits
source/tests; or asks a broad questionnaire.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
continuation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/146-hostile-shorthand-ratification-boundary-scn001-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x` blocked shaping records if the subject creates them.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- executable implementation tickets from unratified hostile shorthand.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/146-hostile-shorthand-ratification-boundary-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for hostile shorthand classification.

## Manual Inspection Requirement

Pass candidate only if it:

- uses the prior transcript and active seed records;
- avoids source/test edits and executable tickets;
- refuses to treat hostile shorthand as semantic ratification;
- does not label vague hostile terms as user-ratified in any ticket or record;
- preserves requested direction only as requested/candidate/blocker language;
- keeps unratified terms out of executable acceptance criteria;
- remains direct and non-patronizing.

## Promotion Rule

Promote only if candidate is net positive over current on hostile-shorthand
classification and regressions pass for explicit concrete ratification plus
subtle exploratory account closure.

## Risks

- Candidate may overblock exact user ratification if wording is too broad.
- A blocked ticket can still look implementation-shaped; manual inspection must
  judge provenance labels and acceptance criteria carefully.

## Execution Log

- 2026-06-24: Registered after EXP-945 found current over-labeled vague hostile
  shorthand as user-ratified inside a blocked account-closure ticket.
- 2026-06-24: Initial live run under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/146-hostile-shorthand-ratification-boundary-scn001-live-micro/`
  is confounded. All three Codex subject calls hit the Codex usage limit before
  producing final messages or workspace changes. Do not use those artifacts to
  assess the candidate. Retry after the reported 2026-06-24 19:24 MST quota
  reset.
