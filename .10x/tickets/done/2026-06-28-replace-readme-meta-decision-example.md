Status: done
Created: 2026-06-28
Updated: 2026-06-28
Depends-On: README.md

# Replace README Meta Decision Example

## Scope

Replace the README's internal install-path decision example with a realistic
product decision that a prospective user can understand without knowing this
repo's internal deliberations.

Included:

- Remove the meta install-path decision from the README example.
- Use a realistic rich decision record with plausible `.10x/` links.
- Align the before/after story with the new example.

Excluded:

- Changes to `SKILL.md`.
- Changes to install instructions.
- Removing the actual `.10x/decisions/equal-first-class-install-paths.md`
  decision record.

## Acceptance Criteria

- AC-001: README example no longer exposes internal README/install-path
  deliberation.
- AC-002: README example reads like a realistic product/engineering decision.
- AC-003: The example demonstrates rich context, authority, alternatives,
  consequences, evidence, limits, and next-action ownership.
- AC-004: Validation checks pass.

## Progress And Notes

- 2026-06-28: Opened from user feedback that the real repo decision was too
  meta and confusing for a viral public README.
- 2026-06-28: Replaced the README example with a realistic billing-webhook
  idempotency decision and aligned the before/after story. Evidence:
  `.10x/evidence/2026-06-28-readme-realistic-decision-example.md`. Review:
  `.10x/reviews/2026-06-28-readme-realistic-decision-example.md`.

## Blockers

None.

## References

- `README.md`
