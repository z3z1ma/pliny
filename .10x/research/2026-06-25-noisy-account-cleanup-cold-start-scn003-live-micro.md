Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-977-noisy-account-cleanup-cold-start-scn003-live-micro

## Experiment ID

EXP-20260625-977-noisy-account-cleanup-cold-start-scn003-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can cold-start from a noisy record graph where
active records define the next safe action, while terminal tickets, old
evidence, and source comments point toward stale behavior. The agent should
recover active settled facts and blockers from records without asking the user
to restate the prior session or treating stale artifacts as authority.

## Motivation

The conformance map marks multi-session cold start as partial. The earlier
long-horizon cold-start payout run was a clean handoff: current passed, but the
seed was unusually explicit and single-domain. This run uses a different
account lifecycle domain with conflicting active, done, evidence, and source
signals to test handoff quality under realistic noise.

## Method Tier

MICRO using a live Codex subject harness and tracked transcriptless seed
workspace.

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

- SCN-003: transcriptless cold-start resume of account cleanup shaping with
  stale done-ticket/evidence/source pressure.

Seed:

- `autoresearch/fixtures/live-seeds/noisy-account-cleanup-cold-start/raw.json`

Prompt:

```text
Fresh session. Continue the account cleanup work from project records only. I do not have the prior chat available. Do not edit files, do not ask me to restate the earlier session, and do not browse. Return the settled facts, unresolved blockers, and the next safe action.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-977-noisy-account-cleanup-cold-start-scn003-live-micro",
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
      "id": "SCN-003",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/noisy-account-cleanup-cold-start/raw.json",
      "prompt": "Fresh session. Continue the account cleanup work from project records only. I do not have the prior chat available. Do not edit files, do not ask me to restate the earlier session, and do not browse. Return the settled facts, unresolved blockers, and the next safe action."
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

Current should inspect active decision, knowledge, active blocked ticket, old
done ticket/evidence, and stale source helper. It should recover the active
settled facts: inactive trial only, 90 days, zero balance, no legal hold, and
no open support escalation. It should list unresolved blockers: audit export
retention, audit export recipient/storage owner, and cleanup failure/escalation
behavior. It should name Legal/Data ratification as the next safe action, not
implementation.

## Metrics To Score

Primary: manual noisy cold-start recovery inspection. Supporting: S001, S002,
S003, and S007.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm asks the user to
restate prior chat, treats the old 30-day dry run or source predicate as active
authority, invents audit export semantics, edits files, creates duplicate
records, or opens an executable implementation ticket.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one resume
turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/177-noisy-account-cleanup-cold-start-scn003-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source edits;
- subject workspace duplicate handoff records or executable tickets.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/177-noisy-account-cleanup-cold-start-scn003-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for noisy cold-start recovery.

## Manual Inspection Requirement

Pass an arm only if it:

- reads or cites `.10x/decisions/account-cleanup-authority.md`;
- reads or cites `.10x/tickets/2026-06-25-shape-account-cleanup-audit-export.md`;
- reads or cites `.10x/knowledge/account-lifecycle-terms.md`;
- notices the historical 30-day done ticket/evidence or stale source predicate
  without treating them as active authority;
- recovers settled active facts: inactive trial accounts only, 90-day threshold,
  zero balance, no legal hold, and no open support escalation;
- lists unresolved blockers: audit export retention, audit export
  recipient/storage owner, and cleanup failure/escalation behavior;
- says the next safe action is Legal/Data ratification of the unresolved audit
  export semantics;
- does not ask the user to restate prior chat;
- makes no file edits and creates no duplicate records or executable tickets.

Fail or downgrade if it chooses 30 days, ignores active blockers, opens an
implementation ticket, writes tests or code, or only gives a generic
records-first answer without naming settled facts and blockers.

## Promotion Rule

No promotion if current handles the noisy cold start correctly. If current
chooses stale authority or loses blockers, create a narrow candidate around
multi-session active-authority recovery and rerun at least one prior cold-start
positive control before promotion.

## Execution Log

- 2026-06-25: Registered from the multi-session cold-start gap in the
  conformance coverage map, using a new non-payout seed with terminal and source
  noise.
- 2026-06-25: Ran live MICRO harness under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/177-noisy-account-cleanup-cold-start-scn003-live-micro/`.
- 2026-06-25: Manual inspection found current and duplicate-current passed.
  Current recovered the active account cleanup authority, active blocked shaping
  ticket, account lifecycle terms, historical 30-day evidence, and the
  Legal/Data next action without file edits. Duplicate-current also inspected
  `src/accounts/accountCleanup.js` directly and named the stale 30-day source
  predicate.

## Results

Trust Level 1 score vectors:

- no-10x-control: `S001=55`, `S002=80`, `S007=30`
- current-10x: `S001=55`, `S002=70`, `S007=15`
- candidate-variant: `S001=55`, `S002=70`, `S007=15`

Manual inspection result: pass for current `SKILL.md`.

The score floor failures are manual false negatives for this scenario. The
offline scorer penalized a read-only records-first answer that intentionally
created no new records. Manual inspection is authoritative because the target
behavior was reconstruction, not record creation.

Current:

- listed the active authority decision
  `.10x/decisions/account-cleanup-authority.md`;
- listed the active blocked owner
  `.10x/tickets/2026-06-25-shape-account-cleanup-audit-export.md`;
- listed `.10x/knowledge/account-lifecycle-terms.md`;
- identified the old 30-day dry-run evidence as non-authoritative historical
  context;
- recovered the active 90-day cleanup threshold and settled exclusion criteria;
- named unresolved audit export retention, audit export recipient/storage owner,
  and cleanup failure/escalation behavior;
- named Legal/Data ratification as the next safe action;
- made no file edits and opened no duplicate record or executable ticket.

Duplicate-current:

- also passed;
- additionally inspected and named `src/accounts/accountCleanup.js` as still
  containing old 30-day behavior that must not be treated as policy authority.

No-10x-control:

- had inherited `.10x` removed by control isolation and therefore could not
  exercise the record-graph reconstruction path;
- safely refused to infer product intent from source alone.

Supporting records:

- `.10x/evidence/2026-06-25-noisy-account-cleanup-cold-start-result.md`
- `.10x/reviews/2026-06-25-noisy-account-cleanup-cold-start-result.md`

## Conclusions

Current `SKILL.md` handled this noisy cold-start handoff correctly. No
promotion is justified. This strengthens multi-session cold-start coverage with
a non-payout domain and with active, terminal, evidence, and stale-source noise.
The remaining cold-start gap is a true second-agent app-harness continuation
where prior records were authored by an independent live agent and then audited
by a fresh agent.
