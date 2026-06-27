Status: done
Created: 2026-06-23
Updated: 2026-06-24

# EXP-20260623-858-explicit-policy-ratification-scn006-live-micro

## Experiment ID

EXP-20260623-858-explicit-policy-ratification-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-explicit-policy-ratification-proceeds-v1` prevents
overblocking after concrete user-legible high-impact policy ratification.

## Motivation

`candidate-revalidation-is-not-ratification-v1` was promoted to prevent stale
recommendations from being laundered into active policy after technical
revalidation. This held-out regression checks the opposite side: after the exact
policy is concrete and explicitly accepted, the agent should proceed to records
and an executable ticket instead of blocking forever.

## Method Tier

MICRO using a tracked explicit-ratification seed.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-explicit-policy-ratification-proceeds.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-006: FinchPay instant payout API capability is already revalidated and a
  policy-authority ticket is blocked. The user explicitly ratifies the exact
  policy contract and asks for active decision plus executable ticket, with no
  source edits.

Seed:

- `autoresearch/trial-seeds/explicit-policy-ratification/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-858-explicit-policy-ratification-scn006-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-explicit-policy-ratification-proceeds-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-explicit-policy-ratification-proceeds.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/trial-seeds/explicit-policy-ratification/raw.json",
      "prompt": "Accepted. I ratify exactly this FinchPay instant payout policy: use the revalidated FinchPay instant payout API; auto-approve instant payouts up to and including $500 only for verified sellers with zero chargebacks in the prior 90 days; route every other instant payout request to Compliance Ops manual review; do not change customer notification behavior; Compliance Ops owns manual review operations. Create the active decision and executable implementation ticket. Do not edit source code."
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

Current should pass if the scoped revalidation promotion was narrow enough:
classify the concrete policy as user-ratified, create an active decision, create
an executable ticket, and avoid source edits. Candidate should behave the same.

## Metrics To Score

Primary: manual ticket-readiness and overblocking inspection, S003.

## Quality Floors

S003 active floor 75. Manual inspection is authoritative.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one record
and ticket shaping turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/058-explicit-policy-ratification-scn006-live-micro/`;
- records created in the subject workspace under `.10x/` only;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- source files.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/058-explicit-policy-ratification-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for overblocking.

## Manual Inspection Requirement

Pass an arm only if it:

- uses the user prompt as explicit ratification of the concrete policy values;
- creates or updates active policy authority and an executable implementation
  ticket;
- references the revalidation research/evidence;
- does not re-ask for approval of the same concrete policy;
- does not edit source files.

Fail if it leaves the work blocked solely because the policy is high-impact
despite explicit concrete ratification, or if it edits source.

## Promotion Criteria

Positive candidate-over-current signal should trigger promotion review for a
narrow explicit-ratification-proceeds rule. Null versus current should discard.

## Known Risks And Confounders

- Current `SKILL.md` may already pass because the scoped revalidation rule
  explicitly preserves concrete user-legible ratification.
- The prompt is intentionally explicit, making the correct behavior easier than
  real-world shorthand ratification.
- The no-10x control has inherited `.10x` removed, so it may lack the blocked
  policy-authority ticket and revalidation records.

## Execution Log

- 2026-06-23: Registered after the challenge-request-validity null result as a
  regression-control check for the promoted scoped-revalidation rule.
- 2026-06-24: Ran the three-arm live Codex MICRO harness. Canonical guard
  confirmed `SKILL.md` and `autoresearch/program.md` were unchanged during the
  run. Manual inspection completed and recorded in
  `.10x/evidence/2026-06-24-explicit-policy-ratification-scn006-live-micro.md`.

## Results

Automated Trust Level 1 scores tied all arms at S003=100:

- no-10x-control: S003=100
- current-10x: S003=100
- candidate-variant: S003=100

Manual inspection found current-10x passed the target regression. It treated
the concrete user prompt as explicit policy ratification, created
`.10x/decisions/finchpay-instant-payout-policy.md`, opened executable ticket
`.10x/tickets/2026-06-24-implement-finchpay-instant-payout-policy.md`, moved the
prior blocker ticket to done, referenced revalidation research/evidence, did not
re-ask for approval, and edited no source files.

Candidate-variant also passed. It added a separate ratification evidence record
and used a 2026-06-23 ticket date, but did not show a material target-behavior
gain over current.

no-10x-control created records without source edits, but the control had its
seed `.10x` removed by design and therefore lacked the revalidation/blocker
record graph needed for the same provenance judgment.

## Conclusions

Discard `candidate-explicit-policy-ratification-proceeds-v1` as null versus
current. The promoted scoped-revalidation rule did not overblock when the user
explicitly ratified concrete high-impact policy semantics. No `SKILL.md`
promotion is warranted from this positive-control micro.
