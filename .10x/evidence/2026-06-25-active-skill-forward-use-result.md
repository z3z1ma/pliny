Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-active-skill-forward-use-scn012-live-micro.md, autoresearch/candidates/2026-06-25-active-skill-forward-use.md

# Active Skill Forward-Use Result

## What was observed

Ran `EXP-20260625-963-active-skill-forward-use-scn012-live-micro` with 15 live
Codex subject samples across `no-10x-control`, `current-10x`, and
`candidate-variant`.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/211-active-skill-forward-use-scn012-live-micro/`

`canonical_guard.json` reported `SKILL.md` and `autoresearch/program.md`
unchanged during the run.

Trust Level 1 telemetry recorded:

- current-10x: `S002=45` average and `S006=45` average;
- candidate-variant: `S002=45` average and `S006=45` average;
- no-10x-control: `S002=45` average and `S006=30` average.

Manual inspection found current and candidate tied on the target forward-use
behavior. All five current repetitions and all five candidate repetitions:

- created one `.10x/evidence/` record for Ledger import fixture replay;
- used the existing active skill or existing tracked fixture procedure;
- ran the fixture replay command with `testdata/ledger/import-preview.csv` and
  posting date `2026-01-15`;
- recorded the expected `sourceRef` values `LEDGER-001` and `LEDGER-002`;
- recorded the expected `amountCents` values `12345` and `-678`;
- recorded posting date `2026-01-15`;
- avoided `externalId` in changed evidence and ticket files;
- edited no implementation, fixture, script, or skill files.

All five current repetitions updated the open verification ticket. Four
candidate repetitions updated the open ticket; one candidate repetition moved
the ticket to `.10x/tickets/done/`.

The no-10x-control arm also used the `.agents` skill exposure and recorded
evidence. Because control workspaces had inherited `.10x` removed, control
samples could not link the evidence to the pre-existing `.10x` ticket or source
skill. That makes the control useful for harness diagnosis but not promotion
authority.

## Procedure

Inspected:

- `report.md`;
- `canonical_guard.json`;
- raw artifact arm and repetition mapping;
- final subject messages;
- workspace manifests and changed files;
- changed evidence and ticket records;
- source and exposed skill files;
- references to `ledger-import-fixture-replay`, the fixture replay command,
  expected values, stale `externalId`, and nonallowed changed paths.

Used `jq`, `rg --hidden --no-ignore`, `find`, and direct file inspection under
the saved raw artifact root.

## What this supports or challenges

This supports marking active skill forward-use as covered for current
`SKILL.md` in this CLI-runnable subject workspace. Current did not need an
additional overlay to discover and use the existing Ledger import fixture replay
procedure.

This challenges promoting `candidate-active-skill-forward-use-v1`: the candidate
did not improve the target behavior over current. The only visible difference
was one candidate ticket-closure action, which was outside this candidate's
forward-use claim and not required by the prompt.

## Limits

Trust Level 1 scores are manual false negatives for this scenario. The scorer
is shaped around broad SCN-012 retrospective extraction, not existing-skill
procedure execution. The conclusion rests on manual inspection of saved Codex
CLI subject workspaces.
