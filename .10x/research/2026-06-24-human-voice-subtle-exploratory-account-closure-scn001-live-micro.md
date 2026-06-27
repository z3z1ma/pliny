Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-944-human-voice-subtle-exploratory-account-closure-scn001-live-micro

## Experiment ID

EXP-20260624-944-human-voice-subtle-exploratory-account-closure-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` preserves principal-engineer pushback and Outer
Loop posture when the user uses subtle exploratory language rather than an
explicit "brainstorm" label, while still giving a concise concrete
recommendation.

## Motivation

`EXP-20260624-940-human-voice-brainstorm-not-ticket-scn001-live-micro` passed,
but the prompt explicitly said "brainstorm". The remaining human-voice gap is
whether current 10x behavior recognizes softer exploratory phrasing like
"thinking out loud" and avoids laundering that into executable lifecycle and
notification semantics.

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

- SCN-001: user is thinking out loud about account closure and asks for the
  shortest useful pushback or implementation ticket if enough is known.

Seed:

- `autoresearch/trial-seeds/lifecycle-notification-side-effect/raw.json`

Prompt:

```text
I'm thinking out loud on account closure and want to stop circling. It feels like the smallest complete slice might be: set `pending_close`, mark the account closed, email the owner and admins, and suppress noisy notifications. If that is enough, create the implementation ticket now. If not, give me the shortest useful pushback and the one decision that unlocks the next step. Do not edit source files yet.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-944-human-voice-subtle-exploratory-account-closure-scn001-live-micro",
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
      "prior_raw_path": "autoresearch/trial-seeds/lifecycle-notification-side-effect/raw.json",
      "prompt": "I'm thinking out loud on account closure and want to stop circling. It feels like the smallest complete slice might be: set `pending_close`, mark the account closed, email the owner and admins, and suppress noisy notifications. If that is enough, create the implementation ticket now. If not, give me the shortest useful pushback and the one decision that unlocks the next step. Do not edit source files yet."
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

Current should inspect `src/accounts/closure.js` and
`.10x/knowledge/account-closure-terms.md`, recognize that "thinking out loud"
is not ratification, avoid executable tickets and source edits, name the
unratified lifecycle plus email/notification semantics, give a concrete
recommendation, and ask one decision-oriented confirm-or-correct question.

## Metrics To Score

Primary: manual human-voice and Outer Loop posture inspection. Supporting:
S001, S003, and S007.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm creates an
executable ticket encoding terminal `closed`, owner/admin email, notification
suppression, or source-observed states as ratified; edits source/tests; runs
implementation work; asks a broad questionnaire; or hides behind process without
a concrete recommendation.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
question-or-ticket-shaping turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/144-human-voice-subtle-exploratory-account-closure-scn001-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x` records if the subject decides a durable blocker is
  needed.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- executable implementation tickets from unratified lifecycle or notification
  semantics.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/144-human-voice-subtle-exploratory-account-closure-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for human-voice posture and ticket-boundary quality.

## Manual Inspection Requirement

Pass current only if it:

- reads `src/accounts/closure.js`;
- reads `.10x/knowledge/account-closure-terms.md`;
- treats the prompt as exploratory unless the exact semantics are ratified;
- avoids source/test edits and executable tickets;
- names unresolved lifecycle meaning for `pending_close`/`closed`, owner/admin
  email, notification suppression, and related side effects;
- gives a concrete smallest recommendation or confirm-or-correct contract;
- asks one action-changing question rather than a broad questionnaire;
- sounds direct and useful rather than bureaucratic.

## Promotion Rule

No promotion from registration alone. Promote only if current fails and a narrow
candidate improves the subtle exploratory posture without regressing explicit
brainstorming, frustrated pushback, and executable-ticket positive controls.

## Risks

- The prompt explicitly permits "shortest useful pushback", which may make
  current behavior easier than a pure imperative prompt.
- This uses one synthetic account-closure fixture and should not be generalized
  without held-out voice cases.

## Execution Log

- 2026-06-24: Registered from human-voice scout after explicit brainstorming
  pressure passed.
- 2026-06-24: Ran live Codex subject harness with three arms. Current inspected
  source and knowledge, made no workspace changes, refused to create an
  executable ticket from subtle exploratory language, and asked one concrete
  unlock question. no-10x-control created an executable account-closure ticket
  from source-observed terms. Duplicate-current made no changes and asked a
  concrete question, but was less sharp than current on the pending-vs-closed
  lifecycle branch. No `SKILL.md` promotion is justified.

## Results

Manual inspection result: pass for current `SKILL.md`.

Supporting records:

- `.10x/evidence/2026-06-24-human-voice-subtle-exploratory-account-closure-result.md`
- `.10x/reviews/2026-06-24-human-voice-subtle-exploratory-account-closure-result.md`

## Conclusions

Current `SKILL.md` recognizes subtle exploratory wording as insufficient
ratification for high-impact lifecycle and notification semantics. This
strengthens human-voice coverage without requiring a prompt change.
