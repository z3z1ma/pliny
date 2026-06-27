# Reports Dashboard

The reports dashboard already exports filtered report rows through the
server-owned `/api/reports/export.csv` endpoint.

The dashboard toolbar renders an `Export CSV` link using
`reportExportUrl(filters)`, so the downloaded CSV uses the same filters as the
visible report view. Do not add browser-side CSV generation for this workflow.
