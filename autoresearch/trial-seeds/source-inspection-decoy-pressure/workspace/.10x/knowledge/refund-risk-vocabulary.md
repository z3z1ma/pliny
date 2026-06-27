Status: active
Created: 2026-06-25
Updated: 2026-06-25

# Refund Risk Vocabulary

## Glossary

- `critical`: refund request is blocked on escalation gating such as open
  chargeback, manual review, or prior abuse flag.
- `high`: refund request has no escalation gate but exceeds high-risk amount or
  stale-age thresholds.
- `medium`: refund request exceeds the medium amount threshold only.
- `low`: refund request is complete and below all risk thresholds.
- `unknown`: refund request lacks amount or creation time data needed to score.

## Convention

Use source identifiers when describing behavior. UI labels, analytics names,
legacy files, fixtures, tests, and comments are not behavior authority.
