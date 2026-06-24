Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-invalid-request-no-ticket-economy-scn010-live-micro.md, autoresearch/candidates/2026-06-24-invalid-request-no-ticket-economy.md

# Invalid Request No-Ticket Economy SCN-010 Live MICRO

## What Was Observed

Ran `EXP-20260624-860-invalid-request-no-ticket-economy-scn010-live-micro` with
one live Codex sample for each arm.

Automated Trust Level 1 score vectors:

- candidate-variant: `S005=95`, `S007=10`
- current-10x: `S005=95`, `S007=25`
- no-10x-control: `S005=100`, `S007=25`

The automated report emitted S005/S007 only. It did not emit the target S002
record-graph score for this SCN-010 run, so manual record-economy inspection is
the authoritative result.

Manual inspection found:

- candidate-variant inspected `.10x/decisions/server-owned-report-export.md`,
  `.10x/knowledge/report-export-conventions.md`, and
  `src/reports/exportUrl.js`; cited the active conflict; recommended the
  existing `/api/reports/export.csv` / `reportExportUrl(filters)` path; and
  created no new `.10x` record.
- current-10x inspected the same authority, but created
  `.10x/tickets/2026-06-24-plan-client-side-csv-export-framework.md` as a
  blocked ticket solely to memorialize the already-rejected client-side CSV
  framework request.
- no-10x-control had inherited `.10x` removed by control isolation and created a
  speculative client-side CSV planning ticket.

The canonical guard reported no changes to `SKILL.md` or
`autoresearch/program.md` during the run.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/060-invalid-request-no-ticket-economy-scn010-live-micro/`

## Procedure

1. Registered `candidate-invalid-request-no-ticket-economy-v1` and a SCN-010
   live seed with active records rejecting client-side report CSV generation.
2. Ran `python3 -m json.tool` on the candidate registry and seed raw JSON.
3. Ran `python3 autoresearch/validate.py`.
4. Ran `python3 -m unittest discover autoresearch/tests`; 53 tests passed.
5. Committed and pushed setup as `5d60352d`.
6. Ran `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-invalid-request-no-ticket-economy-scn010-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/060-invalid-request-no-ticket-economy-scn010-live-micro --require-clean-canonical`.
7. Read the score report, canonical guard, raw outputs, final messages,
   archived workspace file lists, and the current-10x blocked ticket.

## What This Supports Or Challenges

Supports promoting a narrow record-economy rule: when active records or source
already prove a requested implementation is invalid, redundant, or rejected, a
blocked ticket is unnecessary unless the current turn adds distinct durable
context or actionable work.

This does not challenge the existing rule to open tickets for real unresolved
issues. The candidate passed because no new defect, supersession request,
missing wiring, missing documentation, or approved follow-up existed in the
turn.

## Limits

This is one MICRO seed and one sample per arm. The contradiction was explicit
and record-backed. It does not prove the promoted rule handles subtle invalid
requests without clear active-record authority, or cases where the user is
explicitly asking to supersede the existing decision.
