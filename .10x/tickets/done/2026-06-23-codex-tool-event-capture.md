Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: none
Depends-On: .10x/evidence/2026-06-23-dynamic-subject-continuations.md

# Capture Codex Command Events As Tool Invocations

## Scope

Fix the live Codex subject runner so command execution and file change events in
Codex JSONL are recorded as `tool_invocations` in raw artifacts.

Included:

- Count completed `command_execution` items as tool invocations.
- Count completed `file_change` items as tool invocations.
- Add unit coverage for the Codex JSONL shape observed in live runs.

Excluded:

- Rewriting historical raw artifacts.
- Changing scoring rubrics.
- Changing canonical `SKILL.md`.

## Acceptance Criteria

- AC-001: A live raw artifact produced from Codex `item.completed` /
  `command_execution` events includes at least one `tool_invocations` entry.
- AC-002: Existing score artifact validation still passes.
- AC-003: Full autoresearch tests and static validation pass.

## Progress And Notes

- 2026-06-23: Opened after the live
  `EXP-20260623-804-one-decisive-question-live-micro` run. Raw Codex JSONL
  clearly contained `command_execution` events, but generated raw artifacts had
  empty `tool_invocations`, causing reports to show `tool_calls=0`.
- 2026-06-23: Updated `autoresearch/run_codex_subject.py` to capture completed
  `command_execution` and `file_change` item events.
- 2026-06-23: Updated `autoresearch/tests/test_run_codex_subject.py` to cover
  command execution event capture.
- 2026-06-23: Verification passed:
  `python3 -m unittest autoresearch.tests.test_run_codex_subject` ran 5 tests
  with `OK`; `python3 -m unittest discover -s autoresearch/tests` ran 44 tests
  with `OK`; `python3 autoresearch/validate.py` reported
  `autoresearch contracts valid`.

## Blockers

None.
