Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-external-design-doc-supersedes-local-spec-scn004-live-micro.md

# External Design Doc Supersession Result

## What was observed

Ran `EXP-20260624-941-external-design-doc-supersedes-local-spec-scn004-live-micro`
with:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-external-design-doc-supersedes-local-spec-scn004-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/141-external-design-doc-supersedes-local-spec-scn004-live-micro --require-clean-canonical
```

The runner wrote three live Codex subject samples. `canonical_guard.json`
reported `SKILL.md` and `autoresearch/program.md` unchanged during the run.

Trust Level 1 telemetry recorded:

- current-10x: `S002=75`;
- duplicate-current: `S002=75`;
- no-10x-control: `S002=60`.

Manual inspection of the current arm showed:

- `.10x/specs/nimbus-retention-controls.md` remained active but became a thin
  index for external revision B;
- `.10x/specs/superseded/nimbus-retention-controls-rev-a.md` preserved the old
  revision A local spec as superseded history;
- the active index preserved canonical URL, document id, revision, approved
  status, owner, approval date, export timestamp, local export path, and
  superseded revision A path;
- the active index stated that the external design document remains canonical
  until Product and Engineering explicitly transfer authority back to local
  `.10x`;
- the active index warned future agents not to implement from revision A;
- no source files, tests, or implementation tickets were created.

Manual inspection of no-10x-control showed it only created
`.10x/specs/superseded/nimbus-retention-controls.md`. It marked the old local
spec superseded and pointed to the external rev B export, but left no active
local index record. That means future agents scanning active `.10x/specs/`
would not find the current canonical external authority.

## Procedure

Inspected:

- `report.md`;
- `canonical_guard.json`;
- each arm's final message;
- each arm's `workspace-manifest.json`;
- current and duplicate-current active and superseded spec records;
- no-10x-control superseded record.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/141-external-design-doc-supersedes-local-spec-scn004-live-micro/`

## What this supports or challenges

This supports current `SKILL.md` handling external design-doc supersession of an
active local spec while preserving `.10x` as the local index and avoiding a
full local authority transfer.

## Limits

The seed has no dependent tickets, evidence, or reviews, so it does not test
reference repair breadth. It also does not test external status/revision changes
after an already-thin local index exists.
