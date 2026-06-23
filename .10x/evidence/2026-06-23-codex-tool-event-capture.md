Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/tickets/done/2026-06-23-codex-tool-event-capture.md, .10x/research/2026-06-23-one-decisive-question-live-micro.md

# Codex Tool Event Capture Fix

## What Was Observed

The live Codex JSONL for
`EXP-20260623-804-one-decisive-question-live-micro` contained completed command
events such as:

```json
{"type":"item.completed","item":{"type":"command_execution","command":"/run/current-system/sw/bin/zsh -lc 'rg --files | head -200'","exit_code":0,"status":"completed"}}
```

The raw artifacts generated before the fix had empty `tool_invocations`, and
the report showed `tool_calls=0` for all arms despite visible command execution
in the saved stdout JSONL. This directly affected S001 because the
inspect-before-ask sub-score requires a tool invocation.

After the fix, validation output was:

```text
$ python3 -m unittest autoresearch.tests.test_run_codex_subject
.....
----------------------------------------------------------------------
Ran 5 tests in 0.176s

OK

$ python3 -m unittest discover -s autoresearch/tests
............................................
----------------------------------------------------------------------
Ran 44 tests in 11.241s

OK

$ python3 autoresearch/validate.py
autoresearch contracts valid
```

## Procedure

1. Inspected saved live Codex stdout JSONL for current and candidate arms.
2. Confirmed `item.completed` events with `item.type == "command_execution"`.
3. Updated `autoresearch/run_codex_subject.py` to retain completed
   `command_execution` and `file_change` item events as tool invocations.
4. Updated the focused subject-runner test fixture to include a completed
   command event and assert it appears in raw `tool_invocations`.
5. Ran focused tests, full autoresearch tests, and contract validation.

## What This Supports Or Challenges

This supports that future live Codex raw artifacts will include the tool-use
evidence needed by S001, S002, and cost reports.

This challenges the automated S001 value from
`EXP-20260623-804-one-decisive-question-live-micro`; that run's raw artifacts
were generated before this fix and therefore undercounted inspect-before-ask
evidence.

## Limits

Historical raw artifacts were not rewritten. The corrected runner must be used
for a fresh live run before trusting the affected automated S001 comparison.
