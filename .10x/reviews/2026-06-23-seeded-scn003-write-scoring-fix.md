Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Target: autoresearch/run_codex_subject.py, autoresearch/offline_score.py
Verdict: pass

# Seeded SCN-003 Write Scoring Fix Review

## Target

Diff touching:

- `autoresearch/run_codex_subject.py`
- `autoresearch/offline_score.py`
- `autoresearch/tests/test_run_codex_subject.py`
- `autoresearch/tests/test_offline_score.py`

## Findings

- Pass: The runner now preserves complete archived workspace visibility via
  `post_run_files` while making raw `file_outputs` mean subject-created or
  subject-modified files.
- Pass: `changed_files` gives reports and manual reviewers a manifest-level
  changed-file list without losing the full archive file list.
- Pass: The S002 filter keeps older seeded raw artifacts from producing false
  duplicate-created-record caps.
- Concern: Deleted files are not represented in raw `file_outputs` or
  `changed_files`. This is acceptable for the current SCN-003 duplicate-record
  problem, but a future deletion-sensitive score would need explicit
  `deleted_files` metadata.
- Concern: The S002 retrieval rubric still under-scores exact sourced retrieval
  unless the transcript uses its preferred generic phrases.

## Verdict

Pass.

## Residual Risk

The fix changes raw `file_outputs` semantics for future live runs. Existing
score logic that expected a full workspace snapshot must use manifest
`post_run_files` instead.
