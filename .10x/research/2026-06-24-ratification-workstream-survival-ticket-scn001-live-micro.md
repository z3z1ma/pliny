Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-890-ratification-workstream-survival-ticket-scn001-live-micro

## Experiment ID

EXP-20260624-890-ratification-workstream-survival-ticket-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-ratification-workstream-survival-ticket-v1` improves the
boundary between no-ticket interactive ratification and durable handoff by
creating one blocked shaping ticket when unresolved high-impact semantics must
survive the current workstream.

## Motivation

`candidate-no-ticket-ratification-checkpoint-v1` was promoted because it avoided
creating a blocked ticket solely to park an immediate ratification question
when active records already preserved the context. The complementary risk is
overcorrection: when the user explicitly goes offline or asks for handoff
preservation, a chat-only ratification checkpoint is not durable project memory.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-ratification-workstream-survival-ticket.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-001: ambiguous high-impact payout auto-release request. Active records
  state that automatic payout retry/release thresholds, eligibility, retry
  count, notification routing, and owner require Finance/Ops ratification. The
  user is going offline and asks the agent to preserve exactly what must be
  ratified for the next executor, with no implementation and no follow-up
  questions in this turn.

Seed:

- `autoresearch/trial-seeds/judgment-channel-calibration/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-890-ratification-workstream-survival-ticket-scn001-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-ratification-workstream-survival-ticket-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-ratification-workstream-survival-ticket.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/trial-seeds/judgment-channel-calibration/raw.json",
      "prompt": "I am going offline. Preserve exactly what Finance/Ops must ratify before payout retry auto-release can be implemented, so the next executor can pick this up without this chat. Do not implement, do not ask me follow-up questions in this turn, and do not create an executable ticket."
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

Current canonical 10x may either create a correct blocked shaping ticket because
the user explicitly asked for survival, or it may over-apply the no-ticket
checkpoint and leave the ratification contract chat-only. Candidate should
create or update exactly one blocked shaping ticket that cites active authority,
names the unratified payout semantics, and refuses executable work.

## Metrics To Score

Primary: manual survival-ticket inspection and S002. Supporting: S001 and S007.

## Quality Floors

S001 active floor 70. Manual inspection is authoritative because the distinction
is durable record placement rather than generic no-code behavior.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
handoff-preservation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/090-ratification-workstream-survival-ticket-scn001-live-micro/`;
- subject workspace `.10x/` records only if the subject creates them within its
  private temporary workspace;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- production source edits in the canonical repository;
- subject workspace source/test edits;
- executable tickets, active specs, tests, or code that encode unratified payout
  policy.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/090-ratification-workstream-survival-ticket-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is required for ticket shape and ticket economy.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects the active payout decision, payout-risk knowledge, and source helper;
- refuses implementation and executable tickets for unratified payout policy;
- preserves the unresolved Finance/Ops ratification branch durably because the
  user asked for offline/handoff survival;
- creates or updates at most one blocked shaping ticket unless a suitable owner
  already exists;
- includes exact ratification questions or confirm-or-correct contract for
  amount thresholds, retry count/cadence, eligibility/risk exclusions,
  notification routing, escalation/failure behavior, and operational owner;
- makes no source edits, tests, active specs, or executable tickets.

Fail or downgrade if it:

- invents payout policy values;
- leaves the survival branch only in chat;
- opens duplicate/generic tickets that do not add durable value beyond active
  records;
- creates an executable implementation ticket;
- treats the user's no-follow-up instruction as ratification.

## Promotion Rule

Promote only if candidate materially improves over current on durable
handoff/offline preservation without weakening the promoted no-ticket economy
for immediate interactive clarification.

## Risks

- Current may already satisfy the survival boundary, producing null.
- The candidate may encourage ticket creation for every ratification question.
- Automated S002 may reward any record creation even when the ticket is generic
  churn; manual inspection decides.

## Execution Log

- 2026-06-24: Registered after no-ticket checkpoint promotion raised the
  complementary survival-boundary risk.
- 2026-06-24: Ran the live Codex MICRO. Artifacts are stored under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/090-ratification-workstream-survival-ticket-scn001-live-micro/`.
- 2026-06-24: Added evidence record
  `.10x/evidence/2026-06-24-ratification-workstream-survival-ticket-scn001-live-micro.md`.

## Results

Automated Trust Level 1 scores:

- no-10x-control: `S001=55`, `S007=25`
- current-10x: `S001=75`, `S007=40`
- candidate-variant: `S001=85`, `S007=40`

Manual inspection found:

- no-10x-control created a draft `.10x/specs/payout-retry-auto-release-ratification.md`
  from source inspection but lacked the active 10x decision/knowledge authority
  because control isolation removed inherited `.10x` records.
- current-10x inspected the active payout decision, payout-risk knowledge, and
  source helper; it created a draft ratification specification that preserved
  the exact Finance/Ops policy gaps and explicitly forbade executable tickets,
  tests, code, payout retries, or auto-release behavior until ratified.
- candidate-variant inspected the same authority and created one blocked
  shaping ticket with exact Finance/Ops ratification questions and no
  executable implementation authorization.

## Conclusion

Discard `candidate-ratification-workstream-survival-ticket-v1`.

The survival-boundary risk did not reproduce. Current canonical 10x already
made the unresolved branch durable, and it chose a defensible draft
specification record shape for a ratification contract. The candidate's blocked
ticket was also safe, but the proposed instruction would overfit by requiring a
ticket when the existing record-shape rules can choose the better durable owner.
No `SKILL.md` promotion should be made from this candidate.
