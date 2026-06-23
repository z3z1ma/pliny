Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: .10x/tickets/2026-06-23-implement-autoresearch-loop.md
Depends-On: .10x/tickets/2026-06-23-autoresearch-codex-full-harness.md, .10x/tickets/2026-06-23-autoresearch-reporting.md

# Run First Autoresearch Calibration Campaign

## Scope

Run the first calibration campaign against the implemented autoresearch loop and
record evidence, scorer limitations, and follow-up work.

Likely write scope:

- `.10x/research/YYYY-MM-DD-*.md` for campaign research.
- `.10x/evidence/YYYY-MM-DD-*.md` for observed runs and scorer output.
- `.10x/reviews/YYYY-MM-DD-*.md` for adversarial review.
- `.10x/tickets/` for follow-ups discovered during calibration.
- `autoresearch/` only for small fixes required to make the campaign runnable,
  if authorized by a child ticket or scope update.

Included:

- Register a MICRO calibration experiment.
- Run at least one MICRO battery within accepted budget.
- Run at least one Codex FULL smoke/calibration run if the FULL harness is ready.
- Compare no-10x/current/candidate behavior where a safe candidate exists; if no
  candidate exists, use no-10x/current and record the limitation.
- Preserve raw artifacts and score outputs.
- Manually inspect scorer matches that support conclusions.
- Record negative, null, and confounded findings.
- Produce a review record before proposing any canonical instruction change.

Excluded:

- Shipping canonical 10x instruction changes.
- Treating score floors as accepted promotion gates.
- Running Claude/OpenCode/oh-my-pi.

## Acceptance Criteria

- AC-001: A registered experiment record exists before runs begin.
- AC-002: At least one MICRO result has score artifacts, raw outputs, and manual
  inspection notes.
- AC-003: If Codex FULL is run, evidence records control isolation, metadata, and
  scorer output.
- AC-004: A review record challenges the campaign's conclusions and scorer
  trust.
- AC-005: Follow-up tickets exist for any implementation gaps, scorer bugs, or
  spec ambiguities discovered.
- AC-006: No canonical 10x instruction change is made without a separate
  promotion decision.

## Progress And Notes

- 2026-06-23: Ticket opened from implementation scoping.
- 2026-06-23: First calibration campaign executed within ticket write scope.
  Registered research record:
  `.10x/research/2026-06-23-first-autoresearch-calibration-campaign.md`.
  MICRO fixture-backed run wrote three raw artifacts and three score artifacts
  with no live calls. Codex FULL fixture-smoke wrote three raw artifacts, three
  score artifacts, and workspace manifests with no live Codex calls. Generated
  `.10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/report.md`.
  Evidence:
  `.10x/evidence/2026-06-23-first-autoresearch-calibration-campaign.md`.
  Review:
  `.10x/reviews/2026-06-23-first-autoresearch-calibration-campaign.md`.
  Verdict is null/confounded for candidate improvement because candidate reused
  current `SKILL.md` and identical pass fixtures. Follow-ups opened:
  `.10x/tickets/2026-06-23-design-real-autoresearch-candidate.md`,
  `.10x/tickets/2026-06-23-calibrate-autoresearch-scorer-trust.md`,
  `.10x/tickets/2026-06-23-broaden-codex-live-harness-isolation.md`, and
  `.10x/tickets/2026-06-23-propagate-campaign-statuses-to-reports.md`.
- 2026-06-23: Parent verification completed. Evidence and review records support
  AC-001 through AC-006 within the ticket's calibration scope. Status set to
  done; promotion-grade gaps are tracked in follow-up tickets and deferred by
  `.10x/decisions/superseded/autoresearch-initial-loop-deferrals.md`.

## Blockers

None.
