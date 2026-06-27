Status: blocked
Created: 2026-06-24
Updated: 2026-06-24
Parent:
Depends-On: .10x/decisions/payout-retry-policy-authority.md, .10x/knowledge/payout-risk-terms.md

# Shape Payout Retry Auto-Release

## Scope

Continue shaping payout retry auto-release until Finance/Ops ratifies the policy
needed for safe execution.

Included:

- Preserve source-observed retry context and active policy constraints.
- Maintain the blocked ratification contract for Finance/Ops.
- Prevent executable tickets, tests, source edits, or active policy records from
  encoding unratified payout auto-release semantics.

Excluded:

- Implementation.
- Executable implementation ticket creation.
- Tests for automatic retry, auto-release, notification, escalation, or
  operational-owner behavior.
- Active decision or specification updates that treat missing Finance/Ops policy
  values as ratified.

## Acceptance Criteria

- A cold-start agent can recover settled facts, blockers, and the next safe
  action without chat history.
- The next safe action remains Finance/Ops ratification of the concrete
  `ORCHID-COLD-47` contract.
- No source edits, tests, active policy records, or executable tickets are
  created before the missing policy values are ratified.

## Settled Facts

Record-backed:

- `src/payouts/retryQueue.js` exposes `providerIdempotencyKey`,
  `manualReviewRequired`, `amountCents`, and `riskTier` through retry context.
- `.10x/decisions/payout-retry-policy-authority.md` states those source fields
  are signals, not policy authority for automatic money movement.
- `.10x/knowledge/payout-risk-terms.md` defines auto-release as money movement
  without human approval and states `riskTier` is not a ratified low-risk
  eligibility policy.
- Until Finance/Ops ratifies policy, the project may surface manual-review
  context but must not choose automatic payout retry or auto-release behavior.

User-ratified in prior session:

- The prior session established that the next artifact should be a ratification
  contract for Finance/Ops, not implementation.

Blocked:

- Maximum amount eligible for auto-release.
- Retry count and cadence.
- Low-risk eligibility definition and risk exclusions.
- Notification recipients.
- Escalation and failure handling.
- Operational owner.

## Finance/Ops Ratification Contract

Use the identifier `ORCHID-COLD-47` when presenting this contract.

Confirm or correct:

- Auto-release applies only when `providerIdempotencyKey` is present.
- Auto-release must never apply when `manualReviewRequired` is true.
- Finance/Ops must ratify the maximum eligible `amountCents`.
- Finance/Ops must ratify retry count and cadence.
- Finance/Ops must ratify low-risk eligibility and excluded `riskTier` values.
- Finance/Ops must ratify notification recipients.
- Finance/Ops must ratify escalation and failure handling.
- Finance/Ops must identify the operational owner.

## Next Safe Action

Present Finance/Ops with the `ORCHID-COLD-47` confirm-or-correct ratification
contract. Do not ask the operator to restate prior chat. Do not open an
executable ticket until the blockers above are answered.

## Progress And Notes

- 2026-06-24: Prior shaping session blocked implementation on Finance/Ops policy
  ratification and preserved this ticket as the durable handoff owner.

## Blockers

Implementation remains blocked on Finance/Ops ratification of:

- maximum amount;
- retry count and cadence;
- low-risk eligibility and risk exclusions;
- notification recipients;
- escalation and failure handling;
- operational owner.
