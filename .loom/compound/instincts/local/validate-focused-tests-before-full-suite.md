---
id: validate-focused-tests-before-full-suite
title: Validate focused tests before full-suite gates
trigger: When implementing or debugging changes scoped to a specific module or harness
confidence: 0.8200
status: active
domain: workflow
source: local
created_at: 2026-02-15T18:42:48.199834Z
updated_at: 2026-02-16T06:22:48.260602Z
tags: workflow, testing, iteration, validation
notes: The run did not proceed to full-suite until the scoped test was made green, then gates followed in order.
---

## Action
Run targeted pytest files for the area being changed until green, then run repository-wide lint/type/test gates.

## Evidence
- ts=2026-02-16T00:19:43.228000Z source_id=obs-pytest-focused-fail-001943 source_hash=uv-run-pytest-tests-test-team-start-yaml-composition-fail
- ts=2026-02-16T00:19:54.256391Z source_id=obs-pytest-focused-fail-001954 source_hash=uv-run-pytest-tests-test-team-start-yaml-composition-fail-retry
- ts=2026-02-16T00:20:06.348082Z source_id=obs-pytest-focused-pass-002006 source_hash=uv-run-pytest-tests-test-team-start-yaml-composition-pass
- ts=2026-02-16T00:20:09.421367Z source_id=obs-gate-ruff-002009 source_hash=uv-run-ruff-check-pass
- ts=2026-02-16T00:22:07.544781Z source_id=obs-gate-pyright-002207 source_hash=uv-run-basedpyright-pass
- ts=2026-02-16T00:22:15.916011Z source_id=obs-gate-pytest-full-002215 source_hash=uv-run-pytest-full-start
- ts=2026-02-16T00:40:16.646101Z source_id=obs-pytest-focused-fail-004016 source_hash=uv-run-pytest-tests-test-team-spawn-yaml-members-fail
- ts=2026-02-16T00:41:14.658737Z source_id=obs-pytest-focused-pass-004114 source_hash=uv-run-pytest-tests-test-team-spawn-yaml-members-pass
- ts=2026-02-16T00:41:17.513137Z source_id=obs-gate-ruff-004117 source_hash=uv-run-ruff-check-pass
- ts=2026-02-16T00:41:29.097667Z source_id=obs-gate-pyright-004129 source_hash=uv-run-basedpyright-pass
- ts=2026-02-16T06:10:48.700626Z source_id=obs-pytest-focused-pass-061048 source_hash=uv-run-pytest-tests-test-team-harness-codex-pass
- ts=2026-02-16T06:10:50.940139Z source_id=obs-gate-pytest-full-061050 source_hash=uv-run-pytest-full-after-focused
- ts=2026-02-16T06:10:38.322935Z source_id=obs-gate-ruff-061038 source_hash=uv-run-ruff-check-pass
- ts=2026-02-16T06:10:45.054383Z source_id=obs-gate-pyright-061045 source_hash=uv-run-basedpyright-pass

## Notes
The run did not proceed to full-suite until the scoped test was made green, then gates followed in order.
