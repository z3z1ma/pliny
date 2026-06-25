Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: .10x/tickets/done/2026-06-23-autoresearch-calibration-campaign.md
Depends-On: .10x/specs/10x-autoresearch-loop.md

## Scope
Fix the S001 offline scorer so record-only `.10x/` writes during ambiguous
Outer Loop work do not trigger the unauthorized implementation hard floor.

Included:

- Distinguish implementation file outputs from `.10x/` record outputs for
  S001 only.
- Keep the hard floor for source, UI, prototype, and other non-record writes in
  explicitly ambiguous scenarios.
- Add a regression test proving a ticket/evidence record write can still score
  as Outer Loop discipline instead of premature implementation.
- Rerun the affected information-gain MICRO score artifacts after the fix.

Excluded:

- Changing score weights, active floors, or scorer trust level.
- Rewriting S002-S009 scoring behavior.
- Promoting any SKILL.md candidate from automated scores alone.

## Acceptance criteria
- AC-001: `autoresearch/offline_score.py` caps S001 only when implementation
  file outputs exist, not when all file outputs are `.10x/` records.
- AC-002: An automated regression test covers the record-only write case.
- AC-003: Existing S001 fail fixtures with implementation writes still trigger
  the unauthorized implementation hard floor.
- AC-004: The affected live MICRO score artifacts are regenerated and the
  manual evidence records state the scorer bug and its limits.

## Progress and notes
- 2026-06-23: Live information-gain MICRO runs exposed that current 10x and
  the candidate were capped at S001=40 solely because they wrote `.10x` shaping
  records. Manual transcript inspection showed those were not implementation
  writes.
- 2026-06-23: Updated `autoresearch/offline_score.py` so S001 uses
  implementation writes only. Added regression tests for `.10x` record writes
  and implementation writes.
- 2026-06-23: Verification passed:
  `python3 -m unittest autoresearch.tests.test_offline_score`,
  `python3 -m unittest discover -s autoresearch/tests`, and
  `python3 autoresearch/validate.py`.
- 2026-06-23: Rescored the affected SCN-001 and SCN-002 live MICRO artifacts,
  regenerated reports, and recorded evidence at
  `.10x/evidence/2026-06-23-s001-record-write-floor-fix.md`.

## Blockers
None.
