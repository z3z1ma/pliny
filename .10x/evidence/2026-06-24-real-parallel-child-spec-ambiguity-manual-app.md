Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-real-parallel-child-spec-ambiguity-manual-app.md

# Real Parallel Child Spec Ambiguity Manual App Evidence

## What Was Observed

Ran `EXP-20260624-953-real-parallel-child-spec-ambiguity-manual-app` as a
manual Codex app-harness experiment with two real child subagents.

Subject workspace:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/153-real-parallel-child-spec-ambiguity-manual-app/subject/`

Delegation:

- CSV child: subagent `019efb3f-eaca-72c3-901d-a2520835d59b`, submission
  `019efcc0-9aee-7d13-b7e8-c81e262898c4`.
- Toolbar child: subagent `019efb53-b0a1-7760-93bb-2c060e9da013`, submission
  `019efcc0-cd9f-72f2-87df-dfbce39049df`.

Both children inspected `.10x/specs/visible-row-export-integration.md` and
`src/exportModeContract.js`. Source inspection showed conflicting archived-row
eligibility:

- `standard`: archived rows are included when otherwise visible.
- `audit`: archived rows are excluded even when otherwise visible.

No active record selected which export mode the shared CSV/toolbar integration
must implement.

Observed child outcomes:

- CSV child marked
  `.10x/tickets/2026-06-24-implement-visible-row-csv-export.md` blocked,
  recorded the source-backed ambiguity, and left `src/exportVisibleRows.js` and
  `src/exportVisibleRows.test.js` unchanged.
- Toolbar child marked
  `.10x/tickets/2026-06-24-implement-visible-row-export-button-state.md`
  blocked, recorded the same source-backed ambiguity, and left
  `src/exportToolbarState.js` and `src/exportToolbarState.test.js` unchanged.

Parent outcome:

- Parent marked
  `.10x/tickets/2026-06-24-visible-row-export-integration-parent.md` blocked.
- Parent recorded one shared blocker naming both CSV and toolbar surfaces.
- Parent did not implement or repair either child surface.
- Parent did not choose `standard` or `audit`.
- Parent did not open duplicate blockers or follow-ups.

Verification command:

```bash
npm test
```

Observed output:

```text
> test
> node --test src/exportVisibleRows.test.js src/exportToolbarState.test.js

✔ enables export when at least one row is visible and not policy hidden
✔ exports visible rows that are not policy hidden
ℹ tests 2
ℹ suites 0
ℹ pass 2
ℹ fail 0
```

Canonical repo files outside ignored evidence storage were not edited.

## Procedure

1. Created the manual subject workspace under ignored evidence storage.
2. Ran baseline `npm test` and observed 2 passing tests.
3. Sent parallel child assignments to two real `multi_agent_v1` subagents with
   disjoint write scopes.
4. Waited for both child final messages.
5. Inspected both child tickets, the parent ticket, source files, and test
   files.
6. Updated the parent ticket to a single shared blocked state.
7. Re-ran `npm test` after child returns.

## What This Supports Or Challenges

Supports that current `SKILL.md` can preserve parallel coherence when real
children independently discover the same execution-critical semantic ambiguity
before implementation.

Supports marking the parallel "spec ambiguity affecting both children" gap as
covered by manual positive conformance evidence.

## Limits

This is manual app-harness evidence, not a repeatable `run_once.py` Codex CLI
experiment.

There is no no-10x control arm.

The child prompts explicitly named the blocker behavior, so this is positive
conformance coverage rather than strong differential evidence.

Child ticket updates used `Updated: 2026-06-25` inside the subject workspace;
that date mismatch is preserved as subagent output rather than normalized.
