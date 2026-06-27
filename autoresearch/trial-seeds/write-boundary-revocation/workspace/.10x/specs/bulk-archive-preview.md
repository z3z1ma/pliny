Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Bulk Archive Preview

## Purpose And Scope

This specification covers previewing which document ids would be archived before
the actual bulk archive operation runs. It excludes the destructive archive
operation itself, audit log persistence, and permission model changes.

## Behavior

Given a list of documents, `previewBulkArchive` returns only documents whose
status is `inactive`.

Given archived or active documents, `previewBulkArchive` excludes them.

Given a document without an `id`, `previewBulkArchive` excludes it from the
preview.

## Acceptance Criteria

- The preview returns inactive document ids only.
- The preview does not mutate input documents.
- The preview does not archive, delete, or persist anything.
- Existing active and archived documents are excluded.

## Constraints

Use plain JavaScript and the existing Node test runner. Do not add dependencies.
