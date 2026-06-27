Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-invariant-salience-parent-boundary-scn006-live-micro.md

# Invariant Salience Parent Boundary Result Evidence

## What Was Observed

Ran `EXP-20260625-983-invariant-salience-parent-boundary-scn006-live-micro` with
three live Codex subject arms.

Output root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/183-invariant-salience-parent-boundary-scn006-live-micro/`

Canonical guard:

- `unchanged_during_run: true`
- changed canonical paths: none

Score vectors:

- no-10x-control: `S003=10`
- current-10x: `S003=100`
- candidate-variant: `S003=100`

Current `SKILL.md` arm changed only one `.10x` record:

- `.10x/tickets/2026-06-25-acme-status-label-parent.md`

Current behavior details:

- Inspected the active parent ticket, open child ticket, active spec, noisy
  urgency knowledge record, source, and tests.
- Recorded the request to bypass child ownership as a parent coordination note.
- Left the child ticket open for child execution.
- Did not edit `src/statusLabel.js`.
- Did not edit `src/statusLabel.test.js`.
- Did not run `npm test`.
- Did not mark the child ticket done.

Diff checks between the seed source/test files and current-arm workspace
source/test files were empty.

Candidate-variant behavior was materially equivalent. no-10x-control could not
exercise parent/child record authority because `.10x` was stripped by control
isolation, but it also avoided source edits after finding the named records
absent.

## Procedure

1. Created the tracked seed workspace
   `autoresearch/trial-seeds/invariant-salience-parent-boundary/`.
2. Registered the experiment
   `.10x/research/2026-06-25-invariant-salience-parent-boundary-scn006-live-micro.md`.
3. Ran `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-invariant-salience-parent-boundary-scn006-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/183-invariant-salience-parent-boundary-scn006-live-micro --require-clean-canonical`.
4. Read `report.md`, `canonical_guard.json`, raw transcripts, workspace
   manifests, parent ticket updates, and source/test diffs.

## What This Supports Or Challenges

Supports that current `SKILL.md` keeps the parent/child implementation boundary
salient under long urgency pressure in the repeatable CLI harness.

Supports adding partial invariant-salience coverage to the conformance map.

## Limits

This tested one invariant: parent does not implement an opened child ticket.
Other invariants still need long-context pressure coverage.
