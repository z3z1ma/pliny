Status: open
Created: 2026-06-21
Updated: 2026-06-23
Parent:
Depends-On: .10x/specs/kappa-greenline-pilot.md, .10x/decisions/kappa-greenline-display-threshold.md

# Shape Kappa Greenline Pilot

## Scope

Shape the Kappa greenline pilot so it can be executed by a cold-start
implementer.

Included:

- Preserve display-only semantics.
- Use active records for source field and threshold.
- Open a bounded executable implementation ticket when records are coherent.

Excluded:

- Implementing the code directly in this shaping ticket.
- Automatic release or lifecycle changes.

## Acceptance Criteria

- Active spec and decision own display-only behavior, source field, and
  threshold.
- Executable implementation ticket cites the active spec and decision.
- Any unresolved ambiguity remains in blockers instead of implementation scope.

## Progress And Notes

- 2026-06-23: Product ratified display-only greenline behavior.
- 2026-06-23: Active records ratify `KappaReleaseRow.readinessScore >= 85` for
  the display-only pilot label.

## Blockers

None for opening an executable implementation ticket.
