Status: active
Created: 2026-06-24
Updated: 2026-06-24
Parent: None
Depends-On: .10x/specs/bulk-archive-preview.md

# Add Bulk Archive Preview

## Scope

Implement `previewBulkArchive` in `src/documents/archivePreview.js`.

Explicitly included:

- Return inactive document ids only.
- Preserve the input array and document objects.
- Add or update tests in `src/documents/archivePreview.test.js`.

Explicitly excluded:

- Destructive archive behavior.
- Audit persistence.
- Permission model changes.
- Runtime dependencies.

## Acceptance Criteria

- `npm test` passes.
- `previewBulkArchive` returns inactive document ids only.
- The preview does not mutate input documents.
- Active and already archived documents are excluded.

## Progress And Notes

- 2026-06-24: Ticket opened from product request. Implementation was approved in
  the prior turn, but no files have been changed yet.

## Blockers

None.
