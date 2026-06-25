Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-skill-terminal-ticket-path-maintenance-scn012-live-micro.md

# Skill Terminal Ticket Path Maintenance Result

## What was observed

Ran `EXP-20260625-965-skill-terminal-ticket-path-maintenance-scn012-live-micro`
with 15 live Codex subject samples across `no-10x-control`, `current-10x`, and
duplicate-current `candidate-variant`.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/207-skill-terminal-ticket-path-maintenance-scn012-live-micro/`

`canonical_guard.json` reported `SKILL.md` and `autoresearch/program.md`
unchanged during the run.

Trust Level 1 telemetry recorded:

- current-10x: `S002=85` average and `S006=65` average;
- duplicate-current candidate-variant: `S002=85` average and `S006=65`
  average;
- no-10x-control: `S002=59` average and `S006=28` average.

Manual inspection found the terminal ticket path target passed:

- all five current-10x repetitions moved
  `.10x/tickets/2026-06-23-ledger-import-parent.md` to
  `.10x/tickets/done/2026-06-23-ledger-import-parent.md`;
- all five current-10x repetitions moved
  `.10x/tickets/2026-06-23-add-ledger-import-preview.md` to
  `.10x/tickets/done/2026-06-23-add-ledger-import-preview.md`;
- all five duplicate-current repetitions moved the same parent and child tickets
  to `.10x/tickets/done/`;
- no current or duplicate-current repetition left a done-status parent or child
  ticket at top-level `.10x/tickets/`;
- all current and duplicate-current repetitions created
  `.10x/skills/ledger-import-fixture-replay/SKILL.md`;
- no current or duplicate-current repetition created `.agents`, `.claude`, or
  `.opencode` mirrors in the no-native seed workspace;
- workspace manifests showed no implementation file edits;
- live references to the moved parent and child paths were repaired in all
  current and duplicate-current repetitions.

Manual inspection also found a closure-evidence salience concern:

- current-10x created a fresh `2026-06-25-*` closure or validation evidence
  record in three of five repetitions;
- two current-10x repetitions closed by updating tickets, evidence/review
  references, the skill, and the follow-up ticket, but did not add a new durable
  closure evidence record;
- duplicate-current created a fresh closure evidence record in all five
  repetitions.

The `no-10x-control` arm is not meaningful for the terminal-path verdict because
the runner removes `.10x/` for control isolation.

## Procedure

Inspected:

- `report.md`;
- `canonical_guard.json`;
- raw artifact arm and repetition mapping;
- workspace manifests and changed files;
- final parent and child ticket paths;
- top-level `.10x/tickets/` done-status files;
- generated skill paths;
- harness-native skill mirror paths;
- live `.10x` references to the moved parent and child ticket paths;
- final subject messages for current and duplicate-current samples.

Used `rg --hidden --no-ignore`, `jq`, `find`, and direct file inspection under
the saved raw artifact root.

## What this supports or challenges

This supports treating terminal ticket path maintenance as covered for current
`SKILL.md` in the skill-authoring closure lane. The prior top-level done-ticket
variance did not reproduce in this isolated five-repetition current run or the
five-repetition duplicate-current arm.

This challenges treating closure evidence as fully reliable under weak wrap-up
prompts. The agent can perform coherent record movement while failing to create
fresh durable closure evidence in some repetitions.

## Limits

This was a duplicate-current conformance gate, not a new candidate comparison.
It does not test ambiguous multi-harness exposure, real subagent-authored skill
creation, or app-level subagent coherence. Trust Level 1 scores are telemetry;
the terminal-path conclusion rests on manual inspection.
