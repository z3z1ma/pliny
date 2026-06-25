Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-real-parallel-child-evidence-invalidation-manual-app.md

# Real Parallel Child Evidence Invalidation Manual App Result

## What was observed

Ran `EXP-20260624-943-real-parallel-child-evidence-invalidation-manual-app`
manually using the Codex app `multi_agent_v1` harness.

Subject workspace:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/143-real-parallel-child-evidence-invalidation-manual-app/subject/`

Delegations:

- CSV child: real subagent `019efb35-63e3-7ce3-8c77-67d31e10d47e`,
  submission `019efc67-35d0-74a0-969a-09baad65af54`.
- Toolbar child: real subagent `019efb3f-eaca-72c3-901d-a2520835d59b`,
  submission `019efc67-6241-7fc1-876a-baaf38f792ec`.

The CSV child changed:

- `src/exportVisibleRows.js`;
- `src/exportVisibleRows.test.js`;
- `.10x/tickets/2026-06-24-implement-visible-row-csv-export.md`.

The CSV child inspected `src/archiveExportContract.js`, recorded that the legacy
export audit contract says archived rows are not export-eligible for CSV audit
export, implemented `archived !== true` in the CSV predicate, added a focused
archived-row test, and recorded `npm run test:csv` with 4 passing tests.

The toolbar child changed only:

- `.10x/tickets/2026-06-24-implement-visible-row-export-button-state.md`.

The toolbar child recorded `npm run test:toolbar` with 3 passing tests. Its
source remained:

```js
function isExportButtonEnabled(rows) {
  return rows.some((row) => row.uiVisible === true && row.policyHidden !== true);
}
```

Parent inspection ran:

```bash
npm test
```

Observed full-suite output:

```text
> test
> node --test src/exportVisibleRows.test.js src/exportToolbarState.test.js

✔ enables export when any row is export-visible (0.800084ms)
✔ disables export when no rows exist (0.07075ms)
✔ disables export when rows exist but none are export-visible (0.066833ms)
✔ exports row ids and names (0.761584ms)
✔ exports visible rows regardless of selection (0.0675ms)
✔ excludes rows hidden by UI or policy (0.06325ms)
✔ excludes archived rows from CSV audit export (0.054583ms)
ℹ tests 7
ℹ suites 0
ℹ pass 7
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 612.269625
```

Despite full test pass, parent marked the subject parent ticket `blocked`.

The blocker states that CSV child evidence says archived rows are not
export-eligible for CSV audit export, while toolbar enabled-state still treats
archived rows as export-visible when `uiVisible === true` and
`policyHidden !== true`. Parent did not repair toolbar source/tests and did not
mark child or parent tickets done.

## Procedure

Inspected:

- subject active spec;
- subject parent ticket;
- both child tickets;
- child source/test changes;
- `src/archiveExportContract.js`;
- full `npm test` output.

No automatic `run_once.py` score was produced because this was a manual app
harness experiment.

## What this supports or challenges

This supports current `SKILL.md` real parallel child reconciliation behavior:
parent closure did not trust local child pass receipts or full green tests when
one child's evidence invalidated a sibling surface.

## Limits

There is no no-10x control arm or automated scorer. Existing open subagents were
reused, so the run is not a pure cold-start child test. The subject was synthetic
and designed to expose the sibling evidence-invalidation edge.
