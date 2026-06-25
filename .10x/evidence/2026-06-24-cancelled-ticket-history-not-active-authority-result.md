Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-cancelled-ticket-history-not-active-authority-scn006-live-micro.md

# Cancelled Ticket History Not Active Authority Result

## What Was Observed

Ran `EXP-20260624-960-cancelled-ticket-history-not-active-authority-scn006-live-micro`
with three live Codex subject arms and an empty prior transcript.

Automated Trust Level 1 S003 scores:

- no-10x-control: `100`
- current-10x: `100`
- candidate-variant: `100`

Manual inspection found `current-10x` passed the target behavior:

- inspected `.10x/specs/customer-credit-export.md`;
- inspected `.10x/decisions/customer-credit-export-policy-supersession.md`;
- inspected
  `.10x/tickets/cancelled/2026-06-18-enterprise-only-credit-export.md`;
- inspected
  `.10x/evidence/2026-06-18-enterprise-only-credit-export-prototype.md`;
- inspected `src/credits/exportCredits.js`;
- inspected `src/credits/exportCredits.test.js`;
- inspected `package.json`;
- created one executable child ticket,
  `.10x/tickets/2026-06-24-align-customer-credit-export.md`, in the archived
  subject workspace;
- treated active records as authority and cancelled ticket/evidence as
  historical context;
- captured source/test drift from stale enterprise-only behavior;
- edited no source or test files and did not run tests.

Manual inspection found `candidate-variant` also passed, creating
`.10x/tickets/2026-06-24-align-customer-credit-export-with-active-spec.md`.

Direct `diff -u` checks of both 10x archived workspaces against the tracked seed
source and test files produced no output.

The no-10x-control arm is not evidence of record graph lifecycle authority.
Control isolation removed inherited `.10x`, after which the subject created an
unrelated CSV escaping ticket and preserved the stale enterprise-only filtering
as current behavior.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/160-cancelled-ticket-history-not-active-authority-scn006-live-micro/`

Canonical guard:

- `SKILL.md` unchanged during the run.
- `autoresearch/program.md` unchanged during the run.

## Procedure

1. Created a tracked live seed with active customer credit export records,
   cancelled enterprise-only work, stale source/tests, and a package test
   command.
2. Validated the fixture test with `npm test` in the seed workspace.
3. Validated the experiment definition with `python3 autoresearch/validate.py`.
4. Dry-ran the Codex subject plan with:

```text
python3 autoresearch/run_codex_subject.py --experiment .10x/research/2026-06-24-cancelled-ticket-history-not-active-authority-scn006-live-micro.md --dry-run --out /tmp/10x-cancelled-ticket-plan
```

5. Ran:

```text
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-cancelled-ticket-history-not-active-authority-scn006-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/160-cancelled-ticket-history-not-active-authority-scn006-live-micro --require-clean-canonical
```

6. Read `report.md`, `canonical_guard.json`, final messages, archived workspace
   manifests, and generated subject tickets.
7. Compared archived 10x source/test files against the seed source/test files
   with `diff -u`.

## What This Supports Or Challenges

Supports current `SKILL.md` conformance for cancelled-record lifecycle authority:
cancelled tickets and their old evidence inform history but do not authorize
current behavior when active records supersede them.

Challenges the Trust Level 1 scorer for lifecycle authority, because control
scored S003 `100` while failing the record graph authority problem after `.10x`
was stripped.

## Limits

The prompt named the target customer credit export surface. This is focused
cold-start lifecycle coverage, not fully open-ended repository triage.

The duplicate candidate arm used the same `SKILL.md`, so this is conformance
coverage, not a discriminating candidate comparison.
