Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Payout Risk Terms

## Glossary

- **Auto-release** means moving a failed payout out of manual review and
  authorizing another money-movement attempt without a human approving the
  specific payout.
- **Retryable transport failure** means the provider response indicates a
  technical failure that may be safe to attempt again only after policy confirms
  eligibility, cadence, and escalation behavior.
- **Low-risk account** is not currently defined for automatic payout decisions.
  Existing `riskTier` source values are operational signals, not ratified
  eligibility policy.

## Convention

Treat payout retry policy as high-impact semantics. Source fields may identify
candidate signals, but they do not authorize thresholds, retry counts,
notification routing, or automatic money movement.
