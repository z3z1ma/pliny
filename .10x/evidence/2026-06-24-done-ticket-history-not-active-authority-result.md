Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-done-ticket-history-not-active-authority-scn006-live-micro.md

# Done Ticket History Not Active Authority Result

## What Was Observed

Ran `EXP-20260624-956-done-ticket-history-not-active-authority-scn006-live-micro`
with three live Codex subject arms.

Automated Trust Level 1 S003 scores:

- no-10x-control: `100`
- current-10x: `100`
- candidate-variant: `100`

Manual inspection found `current-10x` passed the target behavior:

- inspected `.10x/decisions/refund-negative-adjustment-policy-supersession.md`;
- inspected `.10x/specs/refund-negative-adjustment-csv.md`;
- inspected
  `.10x/tickets/done/2026-06-20-include-test-refund-adjustments.md`;
- inspected `.10x/evidence/2026-06-20-legacy-negative-adjustment-export.md`;
- inspected `src/refunds/exportNegativeAdjustments.js`;
- inspected `src/refunds/exportNegativeAdjustments.test.js`;
- created one executable child ticket,
  `.10x/tickets/2026-06-24-align-refund-negative-adjustment-export.md`, in the
  archived subject workspace;
- treated the 2026-06-20 ticket/evidence as historical context only;
- scoped the implementation target to the active spec and decision;
- edited no source or test files.

Manual inspection found `candidate-variant` also passed, creating
`.10x/tickets/2026-06-24-align-refund-negative-adjustment-csv-policy.md`. Its
ticket included an explicit assumption-provenance section, but the arm used the
same canonical `SKILL.md`, so this is conformance evidence rather than a
candidate comparison.

Direct `diff -u` checks of both 10x archived workspaces against the tracked seed
source and test files produced no output.

The no-10x-control arm is not a direct contrast. Control isolation removed
inherited `.10x`, so it blocked for missing active policy records instead of
arbitrating active versus terminal records.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/156-done-ticket-history-not-active-authority-scn006-live-micro/`

Canonical guard:

- `SKILL.md` unchanged during the run.
- `autoresearch/program.md` unchanged during the run.

## Procedure

1. Registered the research record and tracked live seed workspace.
2. Validated the experiment definition with `python3 autoresearch/validate.py`.
3. Verified the seed workspace's intentionally stale test suite with `npm test`.
4. Dry-ran the Codex subject plan with:

```text
python3 autoresearch/run_codex_subject.py --experiment .10x/research/2026-06-24-done-ticket-history-not-active-authority-scn006-live-micro.md --dry-run --out /tmp/10x-done-ticket-history-plan
```

5. Ran:

```text
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-done-ticket-history-not-active-authority-scn006-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/156-done-ticket-history-not-active-authority-scn006-live-micro --require-clean-canonical
```

6. Read `report.md`, `summary.json`, `canonical_guard.json`, final messages,
   score artifacts, archived workspace manifests, and generated subject tickets.
7. Compared archived 10x source/test files against the seed source/test files
   with `diff -u`.

## What This Supports Or Challenges

Supports current `SKILL.md` conformance for terminal-record history handling:
done tickets and old evidence are useful context, but active decisions/specs
own current behavior when they supersede terminal records.

Challenges the Trust Level 1 scorer for this scenario because all arms received
S003 `100` even though the no-10x-control arm did not exercise the active versus
terminal record authority comparison.

## Limits

This was a prompted MICRO. The prompt explicitly said terminal records and old
evidence are historical context unless active records re-authorize them.

The duplicate candidate arm used the same `SKILL.md`, so this is conformance
coverage, not a discriminating candidate comparison.

The run does not prove multi-session cold-start quality or unprompted terminal
record authority classification.
