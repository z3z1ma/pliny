Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Profile Display Name Normalization

## Purpose And Scope

Define the small profile display-name normalization helper.

In scope:

- `src/features/profile/normalizeDisplayName.ts`
- Trimming leading and trailing whitespace.
- Returning `"Unnamed"` when the trimmed value is empty.

Out of scope:

- Validation policy.
- User profile persistence.
- UI rendering changes.
- Locale-specific name formatting.

## Behavior

Given a display name with leading or trailing whitespace, when it is normalized,
then the returned value is trimmed.

Given a display name that is empty after trimming, when it is normalized, then
the returned value is `"Unnamed"`.

## Acceptance Criteria

- `"  Ada Lovelace  "` normalizes to `"Ada Lovelace"`.
- `"   "` normalizes to `"Unnamed"`.
- Existing source file remains focused on display-name normalization only.

## Constraints

- Do not add persistence, UI, validation, or locale formatting behavior.
