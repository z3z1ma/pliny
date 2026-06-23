Status: superseded
Created: 2026-06-23
Updated: 2026-06-23

# Autoresearch Initial Loop Deferrals

Superseded by:

- `.10x/decisions/autoresearch-subject-harness-policy.md`

## Context

The initial autoresearch implementation now has static contracts, contract
validation, offline scoring, scenario fixtures, a MICRO runner, Markdown
reporting, a Codex FULL dry-run/fixture-smoke harness, narrow live Codex
isolation evidence, CODEX_HOME/plugin isolation research, and a first calibration
campaign.

The first calibration campaign intentionally used a placeholder candidate and
Trust Level 1 offline scoring. It showed the loop can produce records and
artifacts, but it did not prove a candidate improvement, calibrate S009 cost
efficiency, establish Trust Level 2 or 3 scorer authority, or validate
campaign-scale live Codex isolation.

Relevant follow-up tickets:

- `.10x/tickets/2026-06-23-design-real-autoresearch-candidate.md`
- `.10x/tickets/2026-06-23-calibrate-autoresearch-scorer-trust.md`
- `.10x/tickets/2026-06-23-broaden-codex-live-harness-isolation.md`
- `.10x/tickets/2026-06-23-propagate-campaign-statuses-to-reports.md`

## Decision

The initial autoresearch loop is accepted as a calibration-capable first
implementation, not as a promotion-grade optimization system.

The following requirements are explicitly deferred from the initial parent
ticket closure:

- Real candidate design and promotion-style comparison.
- S009 cost-efficiency scoring and normalized cost model acceptance.
- Trust Level 2 or Trust Level 3 scorer calibration.
- Campaign-scale live Codex isolation evidence.
- Report-native campaign-level null/confounded/backfire status propagation.

No canonical 10x instruction change, score-floor policy change, score-weight
change, or Trust Level 2/3 authority is approved by this decision.

## Alternatives Considered

Keep the parent implementation ticket open until every promotion-grade criterion
is complete.

Rejected because the implementation now provides a coherent runnable loop and
the remaining work is follow-on research/calibration, not missing infrastructure.
Keeping the parent open would blur the completed first implementation with later
optimization campaigns.

Treat the first calibration campaign as sufficient to promote changes.

Rejected because the campaign used a placeholder candidate, fixture-backed
outputs, Trust Level 1 scoring, and no campaign-scale live harness evidence.

Skip documenting the deferrals and close the parent ticket informally.

Rejected because future agents would likely overread the completed tooling as
promotion-grade validation.

## Consequences

The parent implementation ticket may close once its child tickets and evidence
are coherent.

Future promotion campaigns must start from the follow-up tickets and must not use
the first calibration campaign as proof of candidate improvement.

Reports and score artifacts remain useful diagnostic views, but `.10x/` research,
evidence, reviews, and decisions remain the canonical interpretation layer until
the scorer trust model is calibrated.
