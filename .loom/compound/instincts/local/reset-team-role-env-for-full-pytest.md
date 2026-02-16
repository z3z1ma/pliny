---
id: reset-team-role-env-for-full-pytest
title: Reset team role env for full pytest runs
trigger: When running repository-wide `uv run pytest` from team-managed or worker harness contexts
confidence: 0.7000
status: active
domain: testing
source: local
created_at: 2026-02-15T23:53:14.030817Z
updated_at: 2026-02-16T00:43:41.409394Z
tags: testing, pytest, environment, team, reliability
notes: The same full-suite command failed twice with team-role permission errors before an immediate retry with LOOM_TEAM_ROLE cleared.
---

## Action
Before running repository-wide `uv run pytest`, clear role-scoped environment (`LOOM_TEAM_ROLE=` or `unset LOOM_TEAM_ROLE`) so permission-gated team tests execute under neutral context.

## Evidence
- ts=2026-02-15T23:51:52.451917Z source_id=obs-pytest-fail-235152 source_hash=uv-run-pytest-teamerror-role-worker
- ts=2026-02-15T23:53:06.723008Z source_id=obs-pytest-fail-235306 source_hash=uv-run-pytest-teamerror-resume-restores-workers
- ts=2026-02-15T23:53:13.299323Z source_id=obs-pytest-retry-235313 source_hash=LOOM_TEAM_ROLE-empty-uv-run-pytest
- ts=2026-02-15T23:55:32.200355Z source_id=obs-env-reset-235532 source_hash=env-u-team-role-before-pytest-session
- ts=2026-02-16T00:07:15.067685Z source_id=obs-env-reset-000715 source_hash=env-u-team-role-pre-full-suite
- ts=2026-02-16T00:23:36.211908Z source_id=obs-pytest-fail-002336 source_hash=uv-run-pytest-teamerror-role-worker-clock-out
- ts=2026-02-16T00:24:46.775172Z source_id=obs-env-reset-002446 source_hash=env-u-team-role-pre-pytest-retry
- ts=2026-02-16T00:43:04.478708Z source_id=obs-pytest-fail-004304 source_hash=uv-run-pytest-teamerror-role-worker-clock-out
- ts=2026-02-16T00:43:13.033225Z source_id=obs-env-reset-004313 source_hash=env-u-team-role-before-pytest-retry
- ts=2026-02-16T00:43:40.690205Z source_id=obs-env-reset-004340 source_hash=env-u-loom-team-role-pre-next-suite

## Notes
The same full-suite command failed twice with team-role permission errors before an immediate retry with LOOM_TEAM_ROLE cleared.
