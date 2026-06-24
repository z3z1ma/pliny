Status: done
Created: 2026-06-24
Updated: 2026-06-24

# FinchPay Policy History

## Question

What FinchPay policy path was active before Finance revisited auto-approval?

## Sources And Methods

Historical `rg` sample:

```text
.10x/decisions/finchpay-instant-payout-review-policy.md:Decision: All FinchPay instant payout requests require manual Finance review.
.10x/specs/finchpay-instant-payout-review.md:Governing decision: .10x/decisions/finchpay-instant-payout-review-policy.md
```

## Findings

The path `.10x/decisions/finchpay-instant-payout-review-policy.md` was the
active decision path during the manual-review era.

## Conclusions

This research records historical path usage. If the decision is later
superseded, the fenced `rg` sample above should remain unchanged because it is
quoted historical output, not a live reference.
