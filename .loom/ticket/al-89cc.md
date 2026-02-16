---
"id": "al-89cc"
"status": "review"
"deps":
- "al-aec3"
"links": []
"created": "2026-02-15T23:27:04Z"
"type": "task"
"priority": 1
"assignee": "z3z1ma"
"parent": "al-d38a"
"tags":
- "sprint:YAML-Sprint-Foundations"
"external": {}
---
# Integrate YAML composition into team start/run state

Objective alignment:
After schema definition, Team must ingest YAML composition as first-class run configuration. This moves configuration ownership out of hardcoded defaults and into a declarative source of truth.

## Scope
- Add Team CLI entry points for YAML composition input.
- Parse and validate YAML during `loom team start`.
- Persist normalized composition in run state for downstream commands.
- Surface composition metadata in status/charter where relevant.

## Non-goals
- No broadcast enforcement yet.
- No worker lifecycle automation yet beyond persisting config.

## Implementation plan
1. Extend CLI/start command surface:
   - `src/agent_loom/team/cli.py`
   - `src/agent_loom/team/commands/lifecycle.py`
   - add config flag(s), for example `--composition <path>`.
2. In `src/agent_loom/team/core.py::start`, call composition parser and persist normalized result into `run.json`.
3. Define precedence explicitly:
   - CLI explicit overrides
   - YAML composition values
   - existing defaults
4. Ensure persisted composition survives resume and appears in status output where useful.
5. Add tests:
   - `tests/test_team_start_yaml_composition.py`
   - cases for missing file, invalid yaml, invalid schema, and valid persistence.

## Verification
- `uv run pytest tests/test_team_start_yaml_composition.py`
- `uv run ruff check .`
- `uv run basedpyright`

## Acceptance criteria
- `loom team start` accepts YAML composition input and fails fast on invalid config.
- Valid composition is normalized and persisted in run state.
- Restart/resume preserves composition without recomputing nondeterministically.
- Test coverage exists for valid and invalid start-time composition loading.

## Risks and edge cases
- Risk: precedence confusion between CLI and YAML.
  - Detection: unexpected run config values in tests.
  - Mitigation: table-driven precedence tests.
- Risk: run-state migration regressions for existing runs without composition.
  - Detection: start/resume tests fail for legacy run payloads.
  - Mitigation: backward-safe defaults when `composition` key is absent.

## Notes

**2026-02-16T00:15:02Z**

Started work. Status set to in_progress. Plan: inspect current team start/run composition hooks, wire --composition path through CLI/lifecycle/core precedence (CLI > YAML > defaults), persist normalized composition in run state, then add focused tests for missing/invalid/valid composition persistence. ETA first commit in ~45 minutes.

**2026-02-16T00:19:38Z**

Milestone: wired YAML composition through team start flow. Added --composition CLI flag, passed through lifecycle->core.start, parse/load with fast-fail errors, persisted normalized composition into run.json, added precedence rule for harness (CLI > composition > defaults), and surfaced composition summary in charter + team status payload/TTY output.

**2026-02-16T00:23:46Z**

Verification pass complete for scope changes. Commands run: (1) uv run pytest tests/test_team_start_yaml_composition.py -> 4 passed, (2) uv run ruff check . -> passed, (3) uv run basedpyright -> 0 errors. Also ran uv run pytest; failures are environment/role-gated existing suite behavior when executed as worker (PERMISSION errors across manager-only team commands) plus unrelated pre-existing failures; no new failures in ticket-specific tests.

**2026-02-16T00:24:07Z**

Ready for review. Delivered: --composition flag on team start; lifecycle->core plumbing; YAML parse/validate via load_team_composition_yaml at start; persisted normalized composition in run.json; precedence implemented for harness (CLI explicit > composition manager harness > defaults); composition summary surfaced in status payload/CLI output and CHARTER composition section; new tests in tests/test_team_start_yaml_composition.py for missing file, invalid YAML, invalid schema, valid persistence and resume stability. Verification: uv run pytest tests/test_team_start_yaml_composition.py; uv run ruff check .; uv run basedpyright. Additional context: uv run pytest (full suite) fails in worker execution context due manager-role permission gating and other pre-existing unrelated failures. Risks: composition currently only influences start-time persisted state + manager harness default precedence; member-level lifecycle automation remains out of scope by design.

**2026-02-16T00:26:17Z**

Merged into team/merge-queue-44953bb8 via queue item 9d92aad2de. Validation on merge-queue: ruff passed; basedpyright passed with 0 errors and 0 warnings; pytest in neutral env (TEAM_* unset) had 269 passed / 6 failed. Failures: tests/test_architecture_guardrails.py::TestModuleBoundaryDocumentation::test_readmes_contain_architecture_sections, tests/test_compound_adapter_hooks_cli.py::{test_hook_adapters_log_observation_json,test_init_instincts_sync_json_smoke,test_omp_hook_reads_stdin_payload_with_event}, tests/test_loom_init_cli_ux.py::{test_init_yes_json_in_git_repo_initializes_everything,test_init_yes_json_outside_git_skips_team}.
