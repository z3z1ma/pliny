Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: .10x/tickets/2026-06-23-increase-autoresearch-throughput.md
Depends-On: .10x/evidence/2026-06-23-records-first-retrieval-opaque-scn003-live-micro.md

# Fix Seeded SCN-003 Write Scoring

## Scope

Correct seeded-continuation artifact semantics so preexisting seed records are
not scored as subject-agent writes.

Included:

- Keep complete archived workspace file lists in workspace manifests.
- Add manifest `changed_files` for created or modified files.
- Write raw fixture `file_outputs` from changed files only.
- Keep SCN-003 S002 scoring backward-compatible with older seeded raw artifacts.
- Add regression tests for seeded files and newly created duplicate records.

Excluded:

- Report UI changes.
- Rescore/reuse CLI mode.
- Live reruns.

## Acceptance Criteria

- Seeded `.10x` files remain visible in `post_run_files`.
- Seeded `.10x` files are absent from raw `file_outputs` unless the subject
  creates or modifies them.
- No-10x-created records still appear in `changed_files` and raw
  `file_outputs`.
- S002 existing-record scoring ignores seeded records but still penalizes a new
  duplicate decision/research record.
- Autoresearch tests and validation pass.

## Progress And Notes

- 2026-06-23: Implemented changed-file snapshotting in
  `autoresearch/run_codex_subject.py`.
- 2026-06-23: Added S002 seeded-file filter in `autoresearch/offline_score.py`
  for old raw artifacts whose `file_outputs` contain seed snapshots.
- 2026-06-23: Added regression tests in
  `autoresearch/tests/test_run_codex_subject.py` and
  `autoresearch/tests/test_offline_score.py`.

## Blockers

None.
