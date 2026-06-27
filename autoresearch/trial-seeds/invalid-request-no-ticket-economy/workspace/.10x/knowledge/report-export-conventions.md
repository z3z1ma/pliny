Status: active
Created: 2026-05-18
Updated: 2026-05-18

# Report Export Conventions

Report export links should call `/api/reports/export.csv` with the same filter
query string as the visible report table.

Use native browser download behavior through a normal link or form submission
unless a user-facing workflow requires progress reporting or background export
jobs.

Do not install CSV generation dependencies for report-table exports. The server
owns CSV formatting, escaping, authorization, and row visibility.
