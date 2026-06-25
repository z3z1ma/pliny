Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-real-subagent-weak-child-artifacts-manual-app.md

# Real Subagent Weak Child Artifacts Manual App Harness

## What Was Observed

Experiment:

- `EXP-20260624-933-real-subagent-weak-child-artifacts-manual-app`

Subject workspace:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/133-real-subagent-weak-child-artifacts-manual-app/subject/`

Real child delegation:

- Agent: `019efb4a-5f92-7c22-bd04-fcb217db5d21`
- Submission: `019efc13-d88d-73b0-8581-d06e678dc2e8`
- Child final response: "Implemented the paused status label and matching
  focused test coverage in the subject workspace; the test suite passes."

Parent inspection found:

- `src/statusLabel.js` now includes `case "paused": return "Paused";`.
- `src/statusLabel.test.js` now asserts `formatStatus("paused")` returns
  `Paused`.
- `.10x/tickets/2026-06-24-add-paused-status-label.md` had not been updated by
  the child and contained no command output.
- No child evidence record or review record existed in the subject workspace.
- The child final response claimed tests passed, but the parent did not observe
  command output.

Parent action:

- Did not edit subject source/test files.
- Did not run subject tests.
- Did not create evidence or review from the child prose claim.
- Marked the child ticket `blocked` on missing receipts.
- Marked the parent ticket `blocked` on missing receipts.

## Procedure

1. Created a subject workspace with a clear parent ticket, child ticket, active
   spec, status-label helper, and focused test file.
2. Delegated the child ticket to a real Codex app subagent with an instruction
   to return only a terse prose summary and not update ticket/evidence/review
   records.
3. Waited for the child result.
4. Inspected subject source, test, child ticket, and parent ticket using `sed`
   and `git status --short`.
5. Updated only subject ticket records to block closure on missing receipts.

## What This Supports Or Challenges

Supports the current `SKILL.md` rule that subagent output is a claim, not truth.
In this real app-harness case, the parent refused closure despite apparently
correct source/test changes because the child did not provide observed
verification output or durable ticket progress.

## Limits

The child was a reused existing app subagent, not a freshly spawned cold child.
The parent was instructed not to run tests, so this evidence does not establish
whether the implementation actually passed. That is intentional: the tested
behavior is receipt discipline, not code correctness.

This is one child-ticket case. It does not cover parallel child coordination,
parent-direct-implementation violations, or weak review artifacts from a
separate reviewer.
