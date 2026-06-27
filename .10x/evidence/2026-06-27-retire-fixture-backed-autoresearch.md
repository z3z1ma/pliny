Status: recorded
Created: 2026-06-27
Updated: 2026-06-27
Relates-To: .10x/tickets/done/2026-06-27-retire-fixture-backed-autoresearch.md, .10x/decisions/autoresearch-live-trial-scientist-inspection.md

# Retire Fixture-Backed Autoresearch Evidence

## Summary

Removed the static offline fixture-backed autoresearch path and kept the live
clean-room subject-agent flow.

Primary changes observed:

- Added the active decision
  `.10x/decisions/autoresearch-live-trial-scientist-inspection.md`.
- Superseded the older active autoresearch decisions and repaired references to
  their `superseded/` paths.
- Removed offline scoring and calibration code, labels, schema, offline fixture
  JSON, result ledger helper, and their unit tests.
- Updated `run_codex_subject.py` and `run_once.py` so live runs emit raw trial
  artifacts, command metadata, prompts, workspaces, manifests, summaries, and
  reports without score artifacts.
- Replaced the score report with a trial artifact report.
- Updated the active program, README, templates, spec, catalogs, and validator
  around scientist inspection of trial artifacts.
- Renamed the live seed directory to `autoresearch/trial-seeds/` and updated
  active path references across code, docs, seed manifests, and research
  records.

## Commands

```text
python3 autoresearch/validate.py
```

Result: `autoresearch contracts valid`.

```text
python3 -m unittest autoresearch.tests.test_run_codex_subject autoresearch.tests.test_run_once autoresearch.tests.test_report autoresearch.tests.test_validate
```

Result: 36 tests passed.

```text
python3 -m unittest discover -s autoresearch/tests
```

Result: 41 tests passed.

```text
git diff --check
```

Result: no whitespace or conflict-marker issues.

Retired seed-path residue search across `.10x` and `autoresearch`
returned no matches.

## Inspection Notes

Search review found no active Python imports or runnable docs for the removed
offline scorer, fixture-backed MICRO runner, calibration utility, result ledger,
or score-artifact schema. The live seed directory has since been renamed to
`autoresearch/trial-seeds/`, and path references were updated repo-wide.

The live runner no longer creates `scores/`, `score_artifact_dir`,
`score_artifact_path`, or offline scorer output. Tests assert those fields stay
absent.

## Limits

Historical records still describe old fixture-backed work because that history
is accurate. Their decision references were repaired to the new `superseded/`
paths, but their historical conclusions were not rewritten.
