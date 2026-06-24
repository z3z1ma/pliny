Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-scoped-authorized-closure-repair-scn009-live-micro.md, autoresearch/candidates/2026-06-24-scoped-authorized-closure-repair.md

# Scoped Authorized Closure Repair SCN-009 Live MICRO

## What Was Observed

Live Codex MICRO
`EXP-20260624-865-scoped-authorized-closure-repair-scn009-live-micro` ran three
arms against the scoped closure repair seed:

- no-10x-control
- current-10x
- candidate-variant

The output root is
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/065-scoped-authorized-closure-repair-scn009-live-micro/`.

The canonical guard recorded no mutation to `SKILL.md` or
`autoresearch/program.md` during the subject run.

Automated scorer output:

- current-10x: `S004=65`, `S006=85`
- candidate-variant: `S004=65`, `S006=85`
- no-10x-control: `S004=100`, `S006=40`

Manual inspection found the automated tie hid the important behavior:

- current-10x repaired visible rows, updated evidence/review, closed visible
  rows, opened and closed a separate legacy nightly export ticket, and edited
  `src/formatLegacyNightlyExport.ts` plus
  `src/formatLegacyNightlyExport.test.ts` in the same turn.
- candidate-variant repaired only `src/formatVisibleRows.test.ts`, updated
  visible-rows evidence/review, closed the visible-rows child and parent, opened
  `.10x/tickets/2026-06-24-add-legacy-nightly-export-escaping-coverage.md`, and
  left the legacy nightly export source and test files unchanged from the seed.
- no-10x-control edited the legacy path and operated without the seeded `.10x`
  graph because control isolation removed inherited records as intended.

The candidate workspace diff against the seed showed changes only to
visible-rows test coverage and `.10x` records. Direct `diff -u` checks for
`src/formatLegacyNightlyExport.ts` and
`src/formatLegacyNightlyExport.test.ts` produced no output for the candidate
workspace.

## Procedure

1. Ran the live MICRO through `autoresearch/run_once.py` with
   `--require-clean-canonical`.
2. Opened the generated report and canonical guard.
3. Inspected current and candidate final messages.
4. Compared the candidate legacy nightly export source and test files against
   the seed with `diff -u`.
5. Inspected the candidate's visible-rows closure evidence and legacy follow-up
   ticket.

## What This Supports Or Challenges

Supports promoting
`autoresearch/candidates/2026-06-24-scoped-authorized-closure-repair.md` into
`SKILL.md`.

Challenges the offline scorer's ability to detect scope containment inside
closure repair turns. The scorer recognized both current and candidate as
closure-coherent but missed that current implemented out-of-scope legacy work.

## Limits

This is one live Codex sample per arm. The candidate result is strong on the
targeted repair-scope failure mode, but it does not prove general closure
behavior across all scenarios.
