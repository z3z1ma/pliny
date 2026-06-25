Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-real-parallel-child-followup-dedup-manual-app.md

# Real Parallel Child Follow-Up Dedup Manual App Evidence

## What Was Observed

Ran `EXP-20260624-954-real-parallel-child-followup-dedup-manual-app` as a
manual Codex app-harness experiment with two real child subagents.

Subject workspace:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/154-real-parallel-child-followup-dedup-manual-app/subject/`

Delegation:

- CSV child: subagent `019efb4a-5f92-7c22-bd04-fcb217db5d21`, submission
  `019efcc6-9f05-76d3-bafd-c0d2ee8b9405`.
- Toolbar child: subagent `019efb53-c6f3-78b2-b91d-3df5c659ba07`, submission
  `019efcc6-c96d-7150-aff7-72a13c00289c`.

Observed child outcomes:

- CSV child implemented `sourceRef` output in `src/csvExport.js`, updated
  `src/csvExport.test.js`, recorded `npm run test:csv` passing, and recorded
  archive malformed-currency coverage as an out-of-scope follow-up suggestion.
- Toolbar child implemented `disabledReason` output in
  `src/exportToolbarState.js`, updated `src/exportToolbarState.test.js`,
  recorded `npm run test:toolbar` passing, and recorded the same archive
  malformed-currency coverage suggestion.

Parent outcome:

- Parent created exactly one active follow-up ticket:
  `.10x/tickets/2026-06-24-add-archive-malformed-currency-coverage.md`.
- Parent moved completed child and parent tickets to `.10x/tickets/done/`.
- Parent repaired stale references to moved tickets.
- Parent did not edit `src/archiveImport.js`.
- Parent did not create duplicate follow-up tickets.

Final subject ticket graph:

- active:
  `.10x/tickets/2026-06-24-add-archive-malformed-currency-coverage.md`
- done:
  `.10x/tickets/done/2026-06-24-add-source-ref-to-csv-export.md`
- done:
  `.10x/tickets/done/2026-06-24-add-toolbar-disabled-reason.md`
- done:
  `.10x/tickets/done/2026-06-24-visible-row-export-followup-parent.md`

Verification command:

```bash
npm test
```

Observed output:

```text
> test
> node --test src/csvExport.test.js src/exportToolbarState.test.js

✔ exports visible rows with id, name, and sourceRef
✔ enables export when a row is export-visible
✔ returns a disabled reason when no row is export-visible
ℹ tests 3
ℹ suites 0
ℹ pass 3
ℹ fail 0
```

Reference check:

```bash
rg 'tickets/2026-06-24-(add-source-ref-to-csv-export|add-toolbar-disabled-reason|visible-row-export-followup-parent)\.md' subject/.10x -n
```

The command returned no matches after parent repair, indicating no stale
references to the moved top-level ticket paths remained.

## Procedure

1. Created the manual subject workspace under ignored evidence storage.
2. Ran baseline `npm test` and observed 2 passing tests.
3. Sent parallel child assignments to two real `multi_agent_v1` subagents with
   disjoint write scopes.
4. Waited for both child final messages.
5. Inspected both child tickets, source files, tests, and follow-up suggestions.
6. Ran full `npm test` and observed 3 passing tests.
7. Created one active follow-up ticket for archive malformed-currency coverage.
8. Moved completed tickets to `tickets/done/` and repaired references.

## What This Supports Or Challenges

Supports that current `SKILL.md` can deduplicate overlapping follow-up
suggestions from parallel children during parent closure.

Supports marking the parallel follow-up deduplication gap as covered by manual
positive conformance evidence.

## Limits

This is manual app-harness evidence, not a repeatable `run_once.py` Codex CLI
experiment.

There is no no-10x control arm.

The child prompts explicitly asked children to record follow-up suggestions, so
this is positive conformance coverage rather than a strong spontaneous-discovery
probe.
