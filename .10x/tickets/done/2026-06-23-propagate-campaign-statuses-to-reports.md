Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: none
Depends-On: .10x/research/2026-06-23-first-autoresearch-calibration-campaign.md, .10x/evidence/2026-06-23-first-autoresearch-calibration-campaign.md

# Propagate Campaign Statuses To Reports

## Scope

Make campaign-level negative, null, confounded, backfire, or inconclusive
statuses visible in generated autoresearch reports without requiring a reader to
open separate research/evidence records.

Included:

- Decide whether statuses belong in score artifacts, a campaign summary artifact,
  or report-side metadata input.
- Preserve the distinction between automated score output and human/manual
  campaign verdicts.
- Ensure generated reports show null/confounded candidate findings from campaign
  evidence when available.
- Keep `.10x/` research/evidence records canonical for verdict rationale.

Excluded:

- Changing score semantics or score floors.
- Marking automated score artifacts as manually inspected unless that inspection
  is actually written into the artifact by design.
- Promotion decisions.

## Acceptance Criteria

- AC-001: A report generated from a campaign with a null/confounded verdict makes
  that verdict visible.
- AC-002: The implementation does not conflate Trust Level 1 scorer output with
  human-reviewed campaign verdicts.
- AC-003: Tests or fixture artifacts cover at least one null/confounded campaign
  and one report with no statuses.
- AC-004: Documentation or evidence records explain where campaign verdict status
  should be recorded.

## Progress And Notes

- 2026-06-23: Opened from first calibration campaign because `report.md`
  reported no result statuses even though the campaign verdict was
  null/confounded in research and evidence.
- 2026-06-23: Added optional campaign metadata input to `autoresearch/report.py`
  and tests for null/confounded metadata plus the no-metadata path. Reports now
  render `## Campaign Verdict` while keeping score artifacts separate. Evidence:
  `.10x/evidence/2026-06-23-report-campaign-status-metadata.md`.

## Blockers

None.
