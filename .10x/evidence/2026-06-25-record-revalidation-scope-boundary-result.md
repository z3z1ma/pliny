Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-record-revalidation-scope-boundary-scn003-live-micro.md, .10x/research/2026-06-24-10x-conformance-coverage-map.md

# Record Revalidation Scope Boundary Result

## What was observed

Ran `EXP-20260625-964-record-revalidation-scope-boundary-scn003-live-micro`
with 15 live Codex subject samples across `no-10x-control`, `current-10x`, and
duplicate-current `candidate-variant`.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/212-record-revalidation-scope-boundary-scn003-live-micro/`

`canonical_guard.json` reported `SKILL.md` and `autoresearch/program.md`
unchanged during the run.

Trust Level 1 telemetry recorded:

- current-10x: `S001=80`, `S002=55`, and `S007=13` average;
- duplicate-current candidate-variant: `S001=80`, `S002=58`, and `S007=12`
  average;
- no-10x-control: `S001=80`, `S002=55`, and `S007=13` average.

Manual inspection found current and duplicate-current tied on the target
behavior. All five current repetitions and all five duplicate-current
repetitions:

- updated the existing active NimbusPay retry ticket;
- created current revalidation research or evidence for the fresh local vendor
  export;
- updated the active specification to separate revalidated vendor facts from
  unresolved Product/Ops policy;
- preserved the 2024 research, done ticket, and done evidence as historical
  context;
- recorded current vendor facts: `event.id`, 24 hour retry, retryable
  timeout/`408`/`429`/`5xx`, and no retry for `409`;
- named stale temptations: `event.dedupeId`, 72 hour retry, all non-`2xx` retry,
  and retrying `409`;
- kept implementation blocked on Product/Ops ratification for duplicate-event
  persistence horizon, dead-letter retention, and escalation ownership;
- edited no source or test files.

One current repetition and one duplicate-current repetition created only a
current research record, not a separate evidence record. Manual inspection
accepted that record shape because the research captured the local export
source, findings, conclusions, and limits, and the ticket depended on it.

The no-10x-control arm had inherited `.10x` removed. It often created fresh
records that separated vendor facts from policy blockers, but could not exercise
the existing-owner update behavior in the same way.

## Procedure

Inspected:

- `report.md`;
- `canonical_guard.json`;
- raw artifact arm and repetition mapping;
- final subject messages;
- workspace manifests and changed files;
- changed tickets, specs, research, and evidence records;
- source and test changed-file lists;
- mentions of current vendor facts, stale 2024 facts, and Product/Ops blockers.

Used `jq`, `rg --hidden --no-ignore`, `sed`, and direct file inspection under
the saved raw artifact root.

## What this supports or challenges

This supports marking the record revalidation scope boundary as covered for
current `SKILL.md`: fresh evidence revalidated only vendor facts and did not
ratify adjacent business semantics.

This challenges the generic S002 telemetry. The scorer flagged fresh research
as duplicate context, but in this scenario fresh research/evidence was the
correct durable owner for revalidation.

## Limits

This run used a local exported vendor-doc fixture rather than live browsing.
It does not test connector freshness, web retrieval, or a case where the vendor
export itself is ambiguous or contradictory.
