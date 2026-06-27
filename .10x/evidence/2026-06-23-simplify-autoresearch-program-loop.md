Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/tickets/done/2026-06-23-simplify-autoresearch-program-loop.md, .10x/decisions/superseded/autoresearch-program-owned-loop.md

# Simplify Autoresearch Around Program-Owned Loop Evidence

## What Was Observed

New core files:

- `autoresearch/program.md`
- `autoresearch/run_once.py`
- `autoresearch/tests/test_run_once.py`
- `.10x/decisions/superseded/autoresearch-program-owned-loop.md`

Deleted controller files:

```text
autoresearch/run_loop.py False
autoresearch/run_codex_candidate.py False
autoresearch/templates/long-run-loop.json False
autoresearch/templates/long-run-live-candidates.json False
autoresearch/tests/test_run_loop.py False
autoresearch/tests/test_run_codex_candidate.py False
```

Deleted stale long-run readiness records:

```text
.10x/decisions/autoresearch-long-run-safety-boundaries.md False
.10x/evidence/2026-06-23-autoresearch-long-run-orchestrator.md False
.10x/evidence/2026-06-23-autoresearch-long-run-readiness.md False
.10x/evidence/2026-06-23-live-candidate-generation-loop.md False
.10x/reviews/2026-06-23-autoresearch-long-run-readiness.md False
.10x/tickets/2026-06-23-autoresearch-long-run-orchestrator.md False
.10x/tickets/2026-06-23-autoresearch-long-run-readiness.md False
.10x/tickets/2026-06-23-live-candidate-generation-loop.md False
```

`autoresearch/program.md` states that:

- it is human-owned;
- autoresearch agents read it before experimenting;
- agents do not edit it unless a human explicitly asks;
- the LLM reasoning engine is the loop controller;
- Python utilities run one experiment, produce scores, validate contracts,
  render reports, or run diagnostics.

`autoresearch/run_once.py` supports one MICRO or FULL experiment. It writes score
artifacts and a report, but it does not loop, resume, generate candidates, use
stop files, or mutate canonical `SKILL.md`.

Durable MICRO smoke:

```text
$ python3 autoresearch/run_once.py --experiment .10x/research/2026-06-23-first-autoresearch-calibration-campaign.md --out .10x/evidence/.storage/2026-06-23-run-once-validation/micro
experiment_id EXP-20260623-301-first-calibration-micro
method_tier MICRO
runner autoresearch/run_micro.py
mode fixture-backed
samples_written 3
score_artifact_dir .10x/evidence/.storage/2026-06-23-run-once-validation/micro/scores
report_path .10x/evidence/.storage/2026-06-23-run-once-validation/micro/report.md
loop_controller LLM reasoning engine; this command runs exactly one iteration
promotion_decision not-performed
```

Reference scan:

```text
$ rg -n "run_loop|run_codex_candidate|long-run|live candidate-generation|resumable state|STOP file|events\\.jsonl|state\\.json|autoresearch-long-run-readiness|live-candidate-generation-loop" autoresearch .10x/tickets .10x/evidence .10x/reviews .10x/decisions --glob '!**/.storage/**'
```

The only remaining controller references were in the simplification ticket
itself, plus one unrelated "long-running" phrase in an older MICRO ticket about
test budget enforcement.

Validation:

```text
$ python3 autoresearch/validate.py
autoresearch contracts valid

$ python3 -m unittest discover -s autoresearch/tests
Ran 34 tests in 0.323s
OK

$ python3 -m unittest autoresearch.tests.test_run_once
Ran 5 tests in 0.090s
OK
```

## Procedure

1. Read the current README, runner implementations, tests, prior long-run
   records, and Karpathy's `program.md` example.
2. Opened `.10x/tickets/done/2026-06-23-simplify-autoresearch-program-loop.md`.
3. Added `autoresearch/program.md`.
4. Added `autoresearch/run_once.py` and focused tests.
5. Deleted Python-owned controller modules, templates, tests, and stale long-run
   readiness records.
6. Repaired retained evidence and ticket references that pointed at the deleted
   readiness parent.
7. Updated README to present `program.md` plus `run_once.py` as the core usage
   path.
8. Ran focused and full validation.

## What This Supports Or Challenges

This supports all acceptance criteria in
`.10x/tickets/done/2026-06-23-simplify-autoresearch-program-loop.md`.

It supports the architectural claim that 10x autoresearch is now centered on a
human-owned program plus one-shot experiment execution, with the LLM reasoning
engine controlling repeated iteration.

It challenges any claim that the repository is still designed around Python
loop/state controllers.

## Limits

This does not add live subject-agent evaluation. Existing MICRO and FULL slices
remain fixture-backed or fixture-smoke. The one-shot runner executes experiments;
it does not judge whether a candidate should be promoted.
