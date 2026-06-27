Status: recorded
Created: 2026-06-27
Updated: 2026-06-27
Relates-To: .10x/tickets/done/2026-06-27-harden-autoresearch-scientific-environment.md, autoresearch/trial-seeds/index.json, autoresearch/catalogs/scores.json

# Autoresearch Scientific Environment Hardening

## What Was Observed

Hardened the active autoresearch environment after complex current-skill trials
showed that seed selection still required manual directory archaeology.

The setup now has:

- a first-class trial seed registry at `autoresearch/trial-seeds/index.json`;
- deterministic regeneration through `autoresearch/build_trial_seed_index.py`;
- validation that the registry covers checked-in seed directories and references
  known scenario and score IDs;
- richer manual scoring policy in `autoresearch/catalogs/scores.json`;
- active docs and templates that point scientists to the seed index and manual
  rubric;
- a report artifact-inspection checklist that lists artifact class presence
  without grading the run.

## Seed Index

The generated index covers:

- Indexed seeds: 129.
- Actual seed directories with `raw.json`: 129.
- Scenario selection guide entries: 15.
- Medium or rich seeds: 111.

Each seed entry includes scenario ID, target rubrics, condition summary,
conditions created, experiment use, prompt family, expected high-quality
behavior, expected failure behavior, known traps, quality-floor signals,
material records, material source files, raw path, workspace manifest path, and
workspace procedure.

## Verification

Commands run:

```text
python3 autoresearch/build_trial_seed_index.py
python3 autoresearch/validate.py
python3 -m py_compile autoresearch/build_trial_seed_index.py autoresearch/validate.py autoresearch/report.py autoresearch/run_codex_subject.py
python3 -m unittest discover -s autoresearch/tests
python3 autoresearch/report.py --artifacts .10x/evidence/.storage/2026-06-27-current-skill-complex-trials/EXP-20260627-101-current-skill-source-record-conflict --out /tmp/autoresearch-report-check.md
git diff --check
```

Results:

- Index regeneration was deterministic: before and after SHA-256 were both
  `0dfddd618f72dcc089927a3eb85730f22c3cae8cb808a5266f06139828220d94`.
- `autoresearch contracts valid`.
- `py_compile` exited 0.
- Full autoresearch test suite: 46 tests passed.
- Report check wrote `/tmp/autoresearch-report-check.md` and included
  `Artifact Inspection Checklist`, `canonical_guard.json`, and
  `workspace manifests`.
- `git diff --check` exited 0.

## What This Supports

The scientific setup now has an explicit seed-selection surface, validated
metadata synchronization, robust manual scoring guidance, and lightweight
artifact-completeness support in reports.

Within the scoped tooling surface, no known blocking gap remains.

## Limits

The index is derived from checked-in seed artifacts and scenario/score catalogs.
It makes seed selection much more legible, but the scientist still must inspect
material records/source files before writing the experiment prompt. Manual
scoring remains judgment by design; the tooling makes the rubric and evidence
requirements explicit rather than automating the verdict.
