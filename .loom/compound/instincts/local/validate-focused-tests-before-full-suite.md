---
id: validate-focused-tests-before-full-suite
title: Validate focused tests before full-suite gates
trigger: When implementing or debugging changes scoped to a specific module or harness
confidence: 0.7400
status: active
domain: workflow
source: local
created_at: 2026-02-15T18:42:48.199834Z
updated_at: 2026-02-15T18:42:48.199834Z
tags: workflow, testing, iteration, validation
notes: This sequence appears across two harness integration efforts and consistently precedes full-suite verification.
---

## Action
Run targeted pytest files for the area being changed until green, then run repository-wide lint/type/test gates.

## Evidence
- ts=2026-02-15T18:11:53.346482Z source_id=obs-pytest-181153 source_hash=uv-run-pytest-tests-test_team_harness_omp-py
- ts=2026-02-15T18:12:01.741295Z source_id=obs-pytest-181201 source_hash=uv-run-pytest-tests-test_team_harness_omp-py-retry
- ts=2026-02-15T18:12:09.398122Z source_id=obs-pytest-181209 source_hash=uv-run-pytest-tests-test_team_harness_omp-py-final
- ts=2026-02-15T18:34:54.382298Z source_id=obs-pytest-183454 source_hash=uv-run-pytest-tests-test_team_harness_codex-py

## Notes
This sequence appears across two harness integration efforts and consistently precedes full-suite verification.
