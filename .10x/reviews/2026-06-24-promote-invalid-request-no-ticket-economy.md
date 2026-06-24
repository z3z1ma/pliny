Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Target: SKILL.md
Verdict: pass

# Promote Invalid Request No-Ticket Economy

## Target

`SKILL.md` ticket-opening guidance, based on
`candidate-invalid-request-no-ticket-economy-v1`.

## Findings

- Significant: Promote narrowly. EXP-860 showed current-10x preserved safety
  but created a blocked ticket with no new durable ownership need. The candidate
  used active records/source as the owner, named the conflict, recommended the
  smallest valid path, and avoided a redundant record.
- Significant: The promoted wording must not weaken the invariant that real
  discoveries become tickets. The inserted text preserves that boundary by
  allowing ticket creation when the turn adds distinct durable context or
  actionable work, including supersession requests, defects, missing wiring,
  missing documentation, or user-approved follow-up.
- Minor: The rule may bias agents away from recording edge cases that are
  genuinely new but superficially resemble an existing rejection. The mitigation
  is the explicit "distinct durable context or actionable work" clause.

## Verdict

Pass. Promote the record-economy rule in the ticket-opening section.

## Residual Risk

The rule relies on the agent correctly distinguishing an already-owned invalid
request from a new supersession or follow-up request. Future SCN-005 and SCN-010
seeds should test that boundary.
