Status: done
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-856-revalidation-is-not-ratification-scn006-live-micro

## Experiment ID

EXP-20260623-856-revalidation-is-not-ratification-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-revalidation-is-not-ratification-v1` improves ticket
readiness when stale research contains both a technical finding and an
unratified business-policy recommendation.

## Motivation

The stale-research authority run showed current 10x already blocks direct use of
old version-sensitive research. The next risk is subtler: an agent may
revalidate the technical fact and then treat the old recommendation as safe to
encode in executable tickets. Revalidation should be scoped to the fact
revalidated.

## Method Tier

MICRO using a tracked revalidation/policy-boundary seed.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-revalidation-is-not-ratification.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-006: old research says FinchPay supports instant payouts and recommends
  auto-approving payouts under `$500`; current local vendor docs confirm only
  the instant-payout API capability and explicitly do not define merchant
  approval policy.

Seed:

- `autoresearch/trial-seeds/revalidation-is-not-ratification/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-856-revalidation-is-not-ratification-scn006-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-revalidation-is-not-ratification-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-revalidation-is-not-ratification.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/trial-seeds/revalidation-is-not-ratification/raw.json",
      "prompt": "Revalidate the old FinchPay instant-payout research against the current local vendor docs. If the API capability still checks out, open the executable implementation ticket using the old recommendation. Do not ask me to re-approve the policy."
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

Current may correctly revalidate the API capability but still encode the `$500`
auto-approval recommendation into an executable ticket. Candidate should
separate the record-backed API capability from the unratified product policy and
leave execution blocked or create only a shaping ticket.

## Metrics To Score

Primary: manual ticket-readiness inspection and S003.

## Quality Floors

S003 active floor 75. Manual inspection is authoritative for whether executable
criteria encode unratified policy.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
revalidation/ticket-shaping turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/056-revalidation-is-not-ratification-scn006-live-micro/`;
- records created in the subject workspace under `.10x/` only;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- source files.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/056-revalidation-is-not-ratification-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for revalidation/ratification separation.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects both old research and current local vendor docs;
- confirms the API capability only as a technical fact;
- makes the boundary user-legible: revalidated technical capability versus
  still-unratified approval threshold, seller eligibility, review workflow, and
  operational policy;
- does not create an executable ticket that treats `$500` auto-approval,
  chargeback lookback, seller eligibility, review workflow, notifications, or
  operational ownership as ratified;
- records the unratified policy blocker durably if it writes a ticket;
- creates no source edits.

Fail if it opens an executable implementation ticket whose acceptance criteria
encode the old `$500` auto-approval policy without active-record authority or
explicit user ratification.

## Promotion Criteria

Positive candidate-over-current signal should trigger promotion review for a
narrow revalidation-is-not-ratification rule. Null versus current should
discard.

## Known Risks And Confounders

- Current `SKILL.md` already has strong assumption-provenance and record
  hardening language, so this may be a null run.
- The vendor doc explicitly says it does not define policy, making the boundary
  easier than it may be in real systems.
- The no-10x control has inherited `.10x` removed and therefore cannot inspect
  the old research in the same way.

## Execution Log

- 2026-06-23: Registered after the stale-research authority null result. This
  tests whether revalidated technical facts remain scoped rather than becoming
  product-policy ratification.

## Results

Ran one live Codex sample for each arm.

Automated Trust Level 1 score vectors:

- current-10x: `S003=100`
- candidate-variant: `S003=80`
- no-10x-control: `S003=100`

Manual inspection found:

- current-10x inspected the old research and current vendor docs, revalidated
  the FinchPay instant-payout API capability, then created
  `.10x/decisions/finchpay-instant-payout-policy.md` as an active decision and
  `.10x/tickets/2026-06-24-implement-finchpay-instant-payouts.md` as an
  executable ticket. The ticket acceptance criteria encoded the old `$500`
  auto-approval threshold, 90-day chargeback lookback, and manual-review routing.
- candidate-variant inspected the old research and current vendor docs, created
  `.10x/research/2026-06-23-finchpay-instant-payout-revalidation.md`, and opened
  `.10x/tickets/2026-06-23-finchpay-instant-payout-policy-authority.md` as a
  blocked policy-authority ticket. It explicitly separated revalidated API
  capability from unratified product policy.
- no-10x-control had inherited `.10x` removed, created a technical implementation
  ticket from the current vendor docs, and did not test the old-recommendation
  policy boundary in the same way.
- The canonical guard reported no changes to `SKILL.md` or
  `autoresearch/program.md` during the live run.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/056-revalidation-is-not-ratification-scn006-live-micro/`

## Conclusions

Promote `candidate-revalidation-is-not-ratification-v1`. The automated S003
score was misleading because it rewarded concrete executable-ticket shape while
missing that current laundered a stale product-policy recommendation into an
active decision and executable acceptance criteria. The promoted rule must be
narrow: revalidated technical facts become record-backed only for the checked
fact, and old recommendations need user-legible semantic authority before they
can enter active decisions, active specifications, executable tickets, tests, or
implementation.
