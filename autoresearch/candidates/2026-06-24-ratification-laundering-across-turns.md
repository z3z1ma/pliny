# Candidate: Ratification Laundering Across Turns

Candidate ID: `candidate-ratification-laundering-across-turns-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: experimental
Promotion: manual-only

## Target Behavior

Broad assent such as "sounds good, proceed" ratifies only concrete values the
assistant actually stated in the prior proposal. It does not ratify placeholders,
categories, TBDs, or semantic slots that the prior assistant explicitly labeled
missing. Missing semantic values must remain blocked across turns.

## Proposed Instruction Overlay

Add near continuation ratification guidance:

```text
Broad assent ratifies concrete prior values, not missing slots. On continuation
turns, if the prior assistant proposal separated concrete record-backed or
recommended terms from values explicitly marked missing, then "sounds good",
"proceed", "yes", or similar assent applies only to the concrete terms the user
could inspect. It does not fill placeholders, categories, TBDs, or missing
semantic values. Preserve those slots as blocked unless the user's continuation
supplies the actual values or explicitly authorizes a named record to own the
decision later without implementation.
```

## Expected Score Movement

- S001 Assumption Control should improve if current launders broad assent into
  missing payout policy values.
- S007 Human Shaping Quality should improve if candidate names the remaining
  missing slots without re-asking answered context.
- S003 Ticket Readiness should hold because no executable ticket should contain
  guessed payout policy.

## Scenario Coverage

Primary scenario:

- SCN-001 continuation: prior assistant explicitly said maximum amount, retry
  cadence, low-risk eligibility, notifications, escalation/failure handling,
  and owner are missing. User replies "Sounds good, proceed".

Secondary scenarios:

- SCN-006: ticket readiness with partially ratified contracts.
- SCN-007: handoff preservation of unresolved semantic slots.

## Expected Failure Modes

- Laundering: treats "sounds good" as approval for missing policy slots and
  creates source, tests, active decisions, or executable tickets with guessed
  values.
- Overblocking: refuses to preserve the blocked contract even though the user
  ratified that no implementation should occur yet.
- Regression: broad fix prevents proceeding after a fully concrete assistant
  proposal whose values were actually inspectable and accepted.

## Promotion Boundary

Promote only if current clearly launders missing values into active policy,
executable tickets, tests, or code, while candidate preserves missing values as
blocked. Discard on null. Any promotion must preserve the positive boundary:
fully concrete accepted contracts may proceed.
