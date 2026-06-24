Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/tickets/done/2026-06-23-fix-seeded-scn003-write-scoring.md

# Seeded SCN-003 Write Scoring Fix

## What Was Observed

After `EXP-20260623-829-records-first-retrieval-opaque-scn003-live-micro`, the
SCN-003 S002 scorer treated seeded `.10x` records as duplicate subject-agent
writes because raw `file_outputs` contained the full archived workspace.

The fix changes runner semantics:

- workspace manifest `post_run_files` keeps all archived files;
- workspace manifest `changed_files` lists created or modified files only;
- raw fixture `file_outputs` contains changed files only.

The scorer also filters seeded/prior files for older raw artifacts when scoring
SCN-003 existing-record scenarios.

## Procedure

Commands:

```bash
python3 -m unittest autoresearch.tests.test_run_codex_subject autoresearch.tests.test_offline_score
python3 -m unittest discover autoresearch/tests
python3 autoresearch/validate.py
git diff --check
python3 autoresearch/offline_score.py --fixtures .10x/evidence/.storage/2026-06-23-skill-autoresearch/029-records-first-retrieval-opaque-scn003-live-micro/raw --out /tmp/10x-rescore-829
```

Observed results:

- Targeted runner/scorer tests: `17` tests passed.
- Full autoresearch test suite: `50` tests passed.
- Autoresearch contracts: valid.
- Diff whitespace check: passed.
- Temporary rescore of EXP-829 removed the duplicate-created-record trigger from
  current and candidate S002. Their S002 remained below the active floor because
  the heuristic still does not fully reward exact opaque retrieval wording.

## What This Supports Or Challenges

Supports:

- Future seeded continuation runs will not misclassify inherited seed records as
  new subject writes.
- Old raw artifacts can be rescored with lower false-positive duplicate-record
  risk.

Challenges:

- S002 SCN-003 still needs better positive retrieval markers if we want the
  automated score to match manual exact-retrieval judgments.

## Limits

No live rerun was performed for this fix. The evidence is unit/regression
coverage plus temporary rescore of existing raw artifacts.
