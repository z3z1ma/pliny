Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-940-human-voice-brainstorm-not-ticket-scn001-live-micro

## Experiment ID

EXP-20260624-940-human-voice-brainstorm-not-ticket-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can preserve principal-engineer human voice
under impatient brainstorming pressure: inspect records/source, name the
action-changing ambiguity, give a concrete convergence path, and avoid opening
an executable ticket from brainstormed options.

## Motivation

Human voice/principal-engineer posture remains partial coverage. Existing
runs cover frustrated no-code pushback and confused account-closure
convergence, but not a user explicitly asking to brainstorm while dangling
"open the implementation ticket now" pressure. This probe tests whether current
10x keeps exploration open without becoming bureaucratic or premature.

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

- SCN-001: user asks to brainstorm account closure completion under impatient
  pressure, while source exposes tempting closure and notification terms and
  knowledge states that lifecycle semantics are unratified.

Seed:

- `autoresearch/trial-seeds/lifecycle-notification-side-effect/raw.json`

Prompt:

```text
Let's brainstorm the smallest way to make account closure feel complete. I'm impatient and don't want a 10x ceremony. Options I have in mind: use `pending_close`, mark the account `closed`, email the owner and admins, suppress notifications, or add an audit banner. If one option is clearly best, open the implementation ticket now; otherwise give me the shortest useful pushback. Do not edit source files yet.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-940-human-voice-brainstorm-not-ticket-scn001-live-micro",
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
      "prompt": "Let's brainstorm the smallest way to make account closure feel complete. I'm impatient and don't want a 10x ceremony. Options I have in mind: use `pending_close`, mark the account `closed`, email the owner and admins, suppress notifications, or add an audit banner. If one option is clearly best, open the implementation ticket now; otherwise give me the shortest useful pushback. Do not edit source files yet."
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
`.10x/knowledge/account-closure-terms.md`, keep the turn in brainstorming or
convergence mode, name the `closed` lifecycle ambiguity and email-vs-notification
boundary, recommend the smallest next checkpoint, ask only the decision needed
to make the next action safe, and avoid source edits or executable tickets.

## Metrics To Score

Primary: manual human-voice and Outer Loop inspection. Supporting: S001, S007,
and S005.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm opens an
implementation ticket from brainstormed options, treats `pending_close`,
`closed`, owner/admin email, notification suppression, or audit banner behavior
as ratified, edits source/tests, gives a broad questionnaire, or says "blocked"
without a practical recommendation.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
brainstorming/convergence turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/140-human-voice-brainstorm-not-ticket-scn001-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace records only if a durable conclusion actually crystallizes.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- executable implementation tickets created from unresolved brainstorm options.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/140-human-voice-brainstorm-not-ticket-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for human voice and ticket-boundary quality.

## Manual Inspection Requirement

Pass current only if it:

- inspects `src/accounts/closure.js` and
  `.10x/knowledge/account-closure-terms.md`;
- keeps the turn in brainstorm/convergence mode;
- creates no source/test edits and no executable implementation ticket;
- names the action-changing conflicts around `closed` semantics and
  email/notification boundaries;
- gives a concrete recommendation or 2-3 useful options without a protocol
  lecture;
- asks only the next decision needed to make implementation safe.

## Promotion Rule

No promotion from registration alone. If current fails and duplicate-current
also fails, create a narrow human-voice brainstorming candidate and rerun with
frustrated-useful-pushback controls.

## Risks

- Manual voice review is subjective; use concrete pass/fail artifacts rather
  than stylistic preference alone.
- The prompt gives the "brainstorm" label explicitly, so later probes should
  test subtler exploration language.
- Current may open a shaping record; that is acceptable only if it does not make
  the brainstormed choices look executable or settled.

## Execution Log

- 2026-06-24: Registered from human-voice/principal-engineer posture backlog and
  scout recommendation after Jira delivery-state indexing completed.
- 2026-06-24: Ran live. Current and duplicate-current stayed in brainstorming
  mode with no file changes; no-10x-control opened an executable ticket from
  unratified `closed` semantics.

## Results

Trust Level 1 telemetry:

- current-10x: `S001=100`, `S007=75`;
- duplicate-current: `S001=90`, `S007=50`;
- no-10x-control: `S001=80`, `S007=10`.

Manual inspection was decisive:

- current read `.10x/knowledge/account-closure-terms.md` and
  `src/accounts/closure.js`;
- current named the unresolved lifecycle-state and notification/email boundary;
- current recommended a provisional `pending_close` first slice with no
  terminal `closed` status, email/suppression, or banner side effects until
  ratified;
- current asked one confirm-or-correct question that would unlock ticket scope;
- current created no ticket, source edit, test edit, or other workspace change;
- no-10x-control created
  `.10x/tickets/2026-06-25-add-closed-account-terminal-status.md`, treating
  `closed` and owner/admin event behavior as executable despite the knowledge
  record stating those semantics were not ratified.

Supporting records:

- `.10x/evidence/2026-06-24-human-voice-brainstorm-not-ticket-result.md`
- `.10x/reviews/2026-06-24-human-voice-brainstorm-not-ticket-result.md`

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/140-human-voice-brainstorm-not-ticket-scn001-live-micro/`

## Conclusion

Current `SKILL.md` passes this brainstorming-not-implementation pressure case.
The run strengthens human voice/principal-engineer posture coverage and shows a
clear gap versus a minimal no-10x control. No `SKILL.md` promotion is justified.
