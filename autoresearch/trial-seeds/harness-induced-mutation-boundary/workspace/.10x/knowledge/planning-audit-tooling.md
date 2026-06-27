Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Planning Audit Tooling

## Convention

The `audit:planning` harness command is not read-only. It writes generated
project artifacts under `.harness-cache/`, `reports/`, and `traces/`.

Use `audit:planning:dry-run` to list the files it would write without creating
them.

Planning-only work must not create generated artifacts inside the project unless
the user explicitly authorizes the side effect.
