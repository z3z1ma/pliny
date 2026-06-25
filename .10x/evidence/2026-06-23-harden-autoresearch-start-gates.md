Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/tickets/done/2026-06-23-harden-autoresearch-start-gates.md

# Harden Autoresearch Start Gates Evidence

## What Was Observed

New hardening files:

- `autoresearch/canonical_guard.py`
- `autoresearch/results.py`
- `autoresearch/splits/skill-improvement-v1.json`
- `autoresearch/tests/test_canonical_guard.py`
- `autoresearch/tests/test_results.py`

Updated files:

- `autoresearch/run_once.py`
- `autoresearch/program.md`
- `autoresearch/README.md`
- `autoresearch/validate.py`
- `autoresearch/tests/test_run_once.py`
- `autoresearch/tests/test_validate.py`

`run_once.py` now writes `canonical_guard.json` by default and supports
`--require-clean-canonical` for multiday start gates.

Guarded one-shot smoke:

```text
$ python3 autoresearch/run_once.py --experiment .10x/research/2026-06-23-first-autoresearch-calibration-campaign.md --out .10x/evidence/.storage/2026-06-23-start-gates/run-once-guarded
experiment_id EXP-20260623-301-first-calibration-micro
method_tier MICRO
runner autoresearch/run_micro.py
mode fixture-backed
samples_written 3
canonical_guard_path .10x/evidence/.storage/2026-06-23-start-gates/run-once-guarded/canonical_guard.json
loop_controller LLM reasoning engine; this command runs exactly one iteration
```

Canonical guard artifact:

```text
exists True
unchanged True
changed_paths []
paths ['SKILL.md', 'autoresearch/program.md']
```

Strong clean-canonical preflight:

```text
$ python3 autoresearch/canonical_guard.py --require-clean
exit_code 2
canonical files are not clean in git: ?? autoresearch/program.md
```

This is the expected state before committing the new setup. After setup is
committed, the same command is the required multiday-run start gate.

Results ledger smoke:

```text
$ python3 autoresearch/results.py init --path .10x/evidence/.storage/2026-06-23-start-gates/results.tsv
wrote .10x/evidence/.storage/2026-06-23-start-gates/results.tsv

$ python3 autoresearch/results.py append --path .10x/evidence/.storage/2026-06-23-start-gates/results.tsv --experiment-id EXP-20260623-301-first-calibration-micro --tier MICRO --candidate baseline-current --score-vector 'S001=100;S007=80' --status review --description 'guarded baseline smoke'
wrote .10x/evidence/.storage/2026-06-23-start-gates/results.tsv
```

Ledger contents:

```text
timestamp	experiment_id	tier	candidate	score_vector	status	description
2026-06-23T18:24:02Z	EXP-20260623-301-first-calibration-micro	MICRO	baseline-current	S001=100;S007=80	review	guarded baseline smoke
```

Validation:

```text
$ python3 autoresearch/validate.py
autoresearch contracts valid

$ python3 -m unittest discover -s autoresearch/tests
Ran 42 tests in 13.104s
OK

$ python3 -m unittest autoresearch.tests.test_canonical_guard autoresearch.tests.test_results autoresearch.tests.test_run_once autoresearch.tests.test_validate
Ran 16 tests in 11.441s
OK
```

## Procedure

1. Added a reusable canonical guard for `SKILL.md` and
   `autoresearch/program.md`.
2. Wired the guard into `run_once.py` by default.
3. Added `--require-clean-canonical` for the committed-setup start gate.
4. Added a results ledger helper with strict TSV validation.
5. Added `autoresearch/splits/skill-improvement-v1.json` and validator checks.
6. Updated `program.md` and README with branch, ledger, guard, held-out, ablation,
   and confidence-boundary instructions.
7. Ran guarded one-shot smoke, ledger smoke, validator, focused tests, and full
   tests.

## What This Supports Or Challenges

This supports all acceptance criteria in
`.10x/tickets/done/2026-06-23-harden-autoresearch-start-gates.md`.

It supports raising operational safety confidence close to 99% once the setup is
committed and the real multiday run uses `--require-clean-canonical` on every
experiment.

It challenges any claim that automated scores alone can become 99% promotion
proof. `program.md` now explicitly preserves that boundary.

## Limits

The guard can prove only the checked canonical files did not change before or
during guarded commands. It does not prove candidate quality, scorer correctness,
or live harness behavior. Discovery confidence still depends on scenario quality,
candidate search, review, and scorer calibration.
