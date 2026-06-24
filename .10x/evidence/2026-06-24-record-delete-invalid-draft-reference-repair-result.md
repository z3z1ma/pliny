Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-record-delete-invalid-draft-reference-repair-scn004-live-micro.md

# Record Delete Invalid Draft Reference Repair Result

## What Was Observed

Ran `EXP-20260624-921-record-delete-invalid-draft-reference-repair-scn004-live-micro`
with three live Codex subject arms.

Automated Trust Level 1 scores:

- no-10x-control: `S002=30`
- current-10x: `S002=30`
- candidate-variant: `S002=30`

Manual inspection found current `SKILL.md` and the duplicate candidate arm both
performed the requested lifecycle operation:

- deleted `.10x/specs/zeus-webhook-retry.md`;
- moved the dependent ticket to
  `.10x/tickets/cancelled/2026-06-24-implement-zeus-webhook-retry.md`;
- marked the dependent ticket `Status: cancelled`;
- cleared the live `Depends-On` header;
- changed the evidence `Relates-To` header to the cancelled ticket only;
- changed the review target away from active specification authority;
- preserved historical mentions and fenced command-output references to the
  deleted path;
- avoided source edits and test execution.

The `current-10x` arm left this machine header:

```text
Target: deleted draft specification formerly at .10x/specs/zeus-webhook-retry.md
```

Manual inspection treats that as a minor header-hygiene risk because the deleted
path remains in a grepable `Target:` header, but not as a failure of the core
deletion/cancellation behavior.

The canonical guard reported unchanged `SKILL.md` and
`autoresearch/program.md` hashes during the run.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/121-record-delete-invalid-draft-reference-repair-scn004-live-micro/`

## Procedure

1. Registered the seed workspace and research record in commit `f21abadd`.
2. Ran:

```text
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-record-delete-invalid-draft-reference-repair-scn004-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/121-record-delete-invalid-draft-reference-repair-scn004-live-micro --require-clean-canonical
```

3. Read `report.md`, score artifacts, archived workspace manifests, final
   messages, and the changed evidence/review/ticket records in each archived
   workspace.

## What This Supports Or Challenges

Supports marking current `SKILL.md` as passing this invalid draft deletion and
reference-repair conformance MICRO.

Challenges the current heuristic scorer for SCN-004 because it assigned all arms
`S002=30` despite current and candidate satisfying the manual lifecycle
criteria.

## Limits

This was not a real candidate comparison; `candidate-variant` duplicated
current `SKILL.md`.

The no-10x-control arm is limited because control isolation removed inherited
`.10x`, and the prompt was concrete enough for the subject to reconstruct a
plausible `.10x` record shape.

This run does not prove rename mechanics. It also does not fully resolve whether
deleted paths should ever remain in machine headers as descriptive non-links.
