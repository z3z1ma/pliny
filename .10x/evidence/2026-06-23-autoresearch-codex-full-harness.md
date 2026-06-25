Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/tickets/done/2026-06-23-autoresearch-codex-full-harness.md, .10x/evidence/2026-06-23-autoresearch-micro-runner.md

# Autoresearch Codex FULL Harness Validation

## What Was Observed

The Codex FULL harness implementation added dry-run planning and fixture-smoke
execution for Codex-shaped FULL runs.

Changed implementation files:

- `autoresearch/run_full_codex.py`
- `autoresearch/tests/test_run_full_codex.py`

Validation artifacts were written under:

- `.10x/evidence/.storage/2026-06-23-codex-full-harness-validation/experiment.json`
- `.10x/evidence/.storage/2026-06-23-codex-full-harness-validation/plan.json`
- `.10x/evidence/.storage/2026-06-23-codex-full-harness-validation/summary.json`
- `.10x/evidence/.storage/2026-06-23-codex-full-harness-validation/raw/`
- `.10x/evidence/.storage/2026-06-23-codex-full-harness-validation/scores/`
- `.10x/evidence/.storage/2026-06-23-codex-full-harness-validation/rescore/`
- `.10x/evidence/.storage/2026-06-23-codex-full-harness-validation/workspaces/`

Worker verification reported:

```text
$ python3 -m unittest autoresearch.tests.test_run_full_codex
Ran 4 tests ... OK

$ python3 -m py_compile autoresearch/run_full_codex.py autoresearch/tests/test_run_full_codex.py
no output

$ python3 -m unittest discover -s autoresearch/tests
Ran 21 tests ... OK

$ python3 autoresearch/validate.py
autoresearch contracts valid

$ python3 autoresearch/run_full_codex.py --experiment .../experiment.json --dry-run --out .../2026-06-23-codex-full-harness-validation
exited 0; planned 3 FULL harness samples, 0 live Codex calls

$ python3 autoresearch/run_full_codex.py --experiment .../experiment.json --fixture-smoke --out .../2026-06-23-codex-full-harness-validation
wrote 3 raw artifacts, 3 score artifacts, 3 workspace manifests

$ python3 autoresearch/offline_score.py --fixtures .../raw --out .../rescore
wrote 3 score artifacts
```

Worker artifact inspection reported:

```text
raw 3
scores 3
rescore 3
manifests 3
no10x_present_suppressed []
no10x_argv_has_ignore_user_config True
```

Parent verification output:

```text
$ python3 -m unittest autoresearch.tests.test_run_full_codex
....
----------------------------------------------------------------------
Ran 4 tests in 0.090s

OK

$ python3 -m py_compile autoresearch/run_full_codex.py autoresearch/tests/test_run_full_codex.py
no output

$ python3 autoresearch/validate.py
autoresearch contracts valid

$ python3 -m unittest discover -s autoresearch/tests
.....................
----------------------------------------------------------------------
Ran 21 tests in 0.217s

OK
```

Parent fresh dry-run, fixture-smoke, and rescore output:

```text
dry_samples 3
dry_live_codex_calls 0
summary_samples_written 3
summary_live_codex_calls 0
raw_count 3
score_count 3
rescore_count 3
manifest_count 3
budget {'planned_harness_runs': 3, 'max_harness_runs': 20, 'estimated_wall_seconds_per_run': 0.0, 'planned_wall_clock_hours': 0.0, 'max_wall_clock_hours': 36, 'suggested_per_run_cap_hours': 3}
no10x_ignore_user_config True
no10x_present_suppressed []
no10x_isolation_status represented-and-smoke-checked
no10x_isolation_limitation Fixture smoke verifies the planned workspace and arguments only; it does not prove live Codex ignores every possible instruction source.
```

Parent inspection of stored validation artifacts showed:

```text
experiment_id EXP-20260623-201-codex-full
method_tier FULL
arms ['no-10x-control', 'current-10x', 'candidate-variant']
scenarios ['SCN-008']
samples_written 3
live_codex_calls 0
planned_harness_runs 3
max_harness_runs 20
max_wall_clock_hours 36
suggested_per_run_cap_hours 3
```

An ASCII source and validation-artifact scan over the Codex FULL files and
storage directory produced no output.

## Procedure

1. Read the Codex FULL ticket, worker output, runner source, runner tests, and
   validation artifacts.
2. Ran the focused Codex FULL runner tests.
3. Ran Python compilation for the runner and tests.
4. Ran the static contract validator.
5. Ran the complete autoresearch unittest suite.
6. Ran a fresh Codex FULL dry-run against the stored validation experiment.
7. Ran a fresh fixture-smoke execution into a temporary directory.
8. Re-scored the generated raw fixture-smoke artifacts with `offline_score.py`.
9. Inspected artifact counts, budget metadata, no-10x workspace manifest
   suppression state, and planned Codex arguments.
10. Ran an ASCII scan over scoped files and validation artifacts.

## What This Supports Or Challenges

This supports:

- `.10x/tickets/done/2026-06-23-autoresearch-codex-full-harness.md#AC-001`
- `.10x/tickets/done/2026-06-23-autoresearch-codex-full-harness.md#AC-002`
- `.10x/tickets/done/2026-06-23-autoresearch-codex-full-harness.md#AC-003`
- `.10x/tickets/done/2026-06-23-autoresearch-codex-full-harness.md#AC-004`
- `.10x/tickets/done/2026-06-23-autoresearch-codex-full-harness.md#AC-005`

The observations support that the first Codex FULL harness slice can plan
registered FULL runs, enforce the accepted 20-run/36-hour/3-hour-per-run budget
metadata, write fixture-smoke raw artifacts, score artifacts, and workspace
manifests, record required model/harness/instruction/fixture metadata, represent
no-10x control isolation, and produce raw artifacts consumable by the offline
scorer.

The observations also challenge any stronger claim that live Codex isolation has
been proven. The runner records planned `codex exec` arguments including
`--ignore-user-config`, and generated no-10x fixture workspaces omit
`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursor/rules`, and `.agents/skills`,
but Codex was not invoked live in this slice.

## Limits

This evidence does not show that:

- A live Codex subject-agent run executes successfully.
- `codex exec --ignore-user-config` suppresses every relevant user, project, or
  plugin instruction source in a live run.
- Live Codex transcripts or JSONL event logs are captured.
- Claude Code, OpenCode, or oh-my-pi harnesses work.
- Fixture-smoke scores are calibrated beyond Trust Level 1.
- Any promotion decision is justified.

Follow-up live isolation validation is tracked in
`.10x/tickets/done/2026-06-23-codex-live-isolation-smoke.md`.
