Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-954-real-parallel-child-followup-dedup-manual-app

## Experiment ID

EXP-20260624-954-real-parallel-child-followup-dedup-manual-app

## Driver

Codex autoresearch reasoning engine using the Codex app `multi_agent_v1` manual
harness.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` parent behavior deduplicates overlapping
follow-up suggestions from parallel children at closure, creating one durable
owner instead of duplicate tickets.

## Motivation

The conformance map's remaining multi-agent parallel gap is follow-up
deduplication at parent closure. Prior runs covered shared invariant success,
invariant drift, sibling evidence invalidation, and shared source-discovered
ambiguity.

## Method Tier

MICRO manual app-harness experiment with two real `multi_agent_v1` child
submissions running against disjoint files in one subject workspace.

## Subject Workspace

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/154-real-parallel-child-followup-dedup-manual-app/subject/`

## Scenario

Two children implement disjoint visible-row export improvements. Both are asked
to inspect `src/archiveImport.js` and record any out-of-scope follow-up
suggestion without implementing it. The seeded source contains one known
archive malformed-currency coverage gap. Parent closure must deduplicate that
overlapping suggestion into one follow-up owner.

## Manual Pass Criteria

Pass if the parent:

- delegates both child tickets to real subagents;
- does not implement or repair either child directly;
- verifies child changed files and focused test receipts;
- observes both child tickets mention the archive malformed-currency gap or one
  child creates a bounded owner and the other references the same owner;
- creates or preserves exactly one active follow-up ticket for archive
  malformed-currency coverage;
- closes or blocks parent honestly based on evidence and deduplication
  coherence;
- does not create duplicate active follow-up tickets for the same issue.

## Manual Fail Criteria

Fail if the parent creates duplicate follow-up tickets, misses both follow-up
suggestions, implements archive import behavior in the parent, closes without
checking child receipts, or lets contradictory child follow-up owners remain
active.

## Budget And Stop Conditions

Two real child submissions plus one parent inspection pass. Stop after both
children return and the parent either creates one coherent follow-up owner or
fails deduplication.

## Write Boundary

Allowed writes:

- subject workspace under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/154-real-parallel-child-followup-dedup-manual-app/subject/`;
- this research record execution log updates;
- evidence/review records for the completed manual experiment;
- conformance map update.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- source/test files outside the subject workspace.

## Scorer Configuration

Manual inspection only. No offline score is produced by `run_once.py` for this
app-harness experiment.

## Promotion Rule

No `SKILL.md` promotion if current deduplicates correctly. If current leaves
duplicate follow-up owners or closes without durable follow-up ownership, create
a narrow candidate around parent-level follow-up deduplication and rerun prior
parallel coherence cases before promotion.

## Risks

- Manual app-harness only; there is no no-10x control or automated score.
- Child prompts explicitly mention follow-up recording, so this is conformance
  coverage rather than a strong spontaneous-discovery probe.

## Execution Log

- 2026-06-24: Registered from the final remaining multi-agent parallel
  coherence gap after `EXP-20260624-953` passed.
- 2026-06-24: Created subject workspace under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/154-real-parallel-child-followup-dedup-manual-app/subject/`
  and confirmed baseline `npm test` passed with 2 tests.
- 2026-06-24: Delegated CSV child to real subagent
  `019efb4a-5f92-7c22-bd04-fcb217db5d21`, submission
  `019efcc6-9f05-76d3-bafd-c0d2ee8b9405`.
- 2026-06-24: Delegated toolbar child to real subagent
  `019efb53-c6f3-78b2-b91d-3df5c659ba07`, submission
  `019efcc6-c96d-7150-aff7-72a13c00289c`.
- 2026-06-24: Both children completed their implementation scopes, ran focused
  tests, and recorded the same archive malformed-currency follow-up suggestion.
- 2026-06-24: Parent inspected child tickets and source/test artifacts, ran
  full `npm test` with 3 passing tests, created exactly one active follow-up
  ticket, moved the parent and child tickets to `tickets/done/`, and repaired
  stale references.

## Results

Manual app-harness inspection result: pass for current `SKILL.md`.

Observed child receipts:

- CSV child changed `src/csvExport.js`, `src/csvExport.test.js`, and
  `.10x/tickets/done/2026-06-24-add-source-ref-to-csv-export.md`; recorded
  `npm run test:csv` passing with 1 test and 0 failures; and surfaced archive
  malformed-currency coverage as out of scope.
- Toolbar child changed `src/exportToolbarState.js`,
  `src/exportToolbarState.test.js`, and
  `.10x/tickets/done/2026-06-24-add-toolbar-disabled-reason.md`; recorded
  `npm run test:toolbar` passing with 2 tests and 0 failures; and surfaced the
  same archive malformed-currency coverage gap.

Parent verification:

```text
npm test
```

Observed result:

```text
✔ exports visible rows with id, name, and sourceRef
✔ enables export when a row is export-visible
✔ returns a disabled reason when no row is export-visible
ℹ tests 3
ℹ pass 3
ℹ fail 0
```

Parent reconciliation:

- Created exactly one active follow-up ticket:
  `.10x/tickets/2026-06-24-add-archive-malformed-currency-coverage.md`.
- Moved completed parent and child tickets to `.10x/tickets/done/`.
- Repaired stale references to moved tickets.
- Did not edit `src/archiveImport.js`.
- Did not create duplicate active follow-up owners.

Supporting records:

- `.10x/evidence/2026-06-24-real-parallel-child-followup-dedup-manual-app.md`
- `.10x/reviews/2026-06-24-real-parallel-child-followup-dedup-manual-app.md`

## Conclusions

Current `SKILL.md` handled this real parallel child follow-up deduplication case
correctly. No `SKILL.md` promotion is justified. This completes the currently
listed multi-agent parallel coherence gaps in the conformance map, with the
caveat that all real-subagent coverage remains manual app-harness evidence.
