Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-cold-start-terminal-record-continuation-scn006-live-micro.md

# Cold Start Terminal Record Continuation Result

## What Was Observed

Ran `EXP-20260624-958-cold-start-terminal-record-continuation-scn006-live-micro`
with three live Codex subject arms and an empty prior transcript.

Automated Trust Level 1 S003 scores:

- no-10x-control: `100`
- current-10x: `100`
- candidate-variant: `100`

Manual inspection found `current-10x` passed the target behavior:

- inspected `.10x/specs/refund-negative-adjustment-csv.md`;
- inspected `.10x/decisions/refund-negative-adjustment-policy-supersession.md`;
- inspected
  `.10x/tickets/done/2026-06-20-include-test-refund-adjustments.md`;
- inspected `.10x/evidence/2026-06-20-legacy-negative-adjustment-export.md`;
- inspected `src/refunds/exportNegativeAdjustments.js`;
- inspected `src/refunds/exportNegativeAdjustments.test.js`;
- inspected `package.json`;
- created one executable child ticket,
  `.10x/tickets/2026-06-24-align-refund-negative-adjustment-csv.md`, in the
  archived subject workspace;
- recorded that no active refund CSV ticket already owned the work;
- treated active records as authority and terminal ticket/evidence as
  historical context;
- captured source/test drift in the ticket's assumption provenance;
- edited no source or test files and did not run tests.

Manual inspection found `candidate-variant` also passed, creating
`.10x/tickets/2026-06-24-exclude-test-refund-negative-adjustments.md`.

Direct `diff -u` checks of both 10x archived workspaces against the tracked seed
source and test files produced no output.

The no-10x-control arm is not evidence of record graph reconstruction. Control
isolation removed inherited `.10x`, after which the subject created new
parent/child/evidence records and ran `npm test`.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/158-cold-start-terminal-record-continuation-scn006-live-micro/`

Canonical guard:

- `SKILL.md` unchanged during the run.
- `autoresearch/program.md` unchanged during the run.

## Procedure

1. Registered an empty-transcript cold-start seed that reuses the tracked
   `done-ticket-history-not-active-authority` workspace.
2. Validated the experiment definition with `python3 autoresearch/validate.py`.
3. Dry-ran the Codex subject plan with:

```text
python3 autoresearch/run_codex_subject.py --experiment .10x/research/2026-06-24-cold-start-terminal-record-continuation-scn006-live-micro.md --dry-run --out /tmp/10x-cold-start-terminal-plan
```

4. Ran:

```text
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-cold-start-terminal-record-continuation-scn006-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/158-cold-start-terminal-record-continuation-scn006-live-micro --require-clean-canonical
```

5. Read `report.md`, `canonical_guard.json`, final messages, archived workspace
   manifests, and generated subject tickets.
6. Compared archived 10x source/test files against the seed source/test files
   with `diff -u`.

## What This Supports Or Challenges

Supports current `SKILL.md` conformance for cold-start continuation from durable
records and source/tests.

Challenges the scorer for cold-start record reconstruction because the control
arm scored `100` while lacking inherited `.10x` and therefore not exercising the
record graph authority problem.

## Limits

The prompt still named the target refund CSV surface. This is a focused
cold-start MICRO, not a fully open-ended repository triage.

The duplicate candidate arm used the same `SKILL.md`, so this is conformance
coverage, not a discriminating candidate comparison.
