Status: recorded
Created: 2026-06-20
Updated: 2026-06-20
Relates-To: .10x/tickets/done/2026-06-20-include-test-refund-adjustments.md

# Legacy Negative Adjustment Export Evidence

## What Was Observed

On 2026-06-20, `npm test` passed for the original export behavior that included
negative test-account rows.

## Procedure

```text
npm test
```

## What This Supports Or Challenges

This supports only the completed 2026-06-20 ticket. It records that the old
all-account negative-adjustment behavior passed tests before the later policy
supersession.

## Limits

This evidence does not prove current desired behavior after
`.10x/decisions/refund-negative-adjustment-policy-supersession.md`. A passing
old test is not authority for current CSV policy.
