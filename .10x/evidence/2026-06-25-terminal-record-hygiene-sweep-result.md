Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-terminal-record-hygiene-sweep-scn012-live-micro.md, autoresearch/candidates/2026-06-25-terminal-record-hygiene-sweep.md

# Terminal Record Hygiene Sweep Result

## What was observed

Ran `EXP-20260625-962-terminal-record-hygiene-sweep-scn012-live-micro` with 15
live Codex subject samples across `no-10x-control`, `current-10x`, and
`candidate-variant`.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/210-terminal-record-hygiene-sweep-scn012-live-micro/`

`canonical_guard.json` reported `SKILL.md` and `autoresearch/program.md`
unchanged during the run.

Trust Level 1 telemetry recorded:

- current-10x: `S002=85` average and `S006=65` average;
- candidate-variant: `S002=85` average and `S006=65` average;
- no-10x-control: `S002=85` average and `S006=32` average.

Manual inspection found current and candidate tied on the target behavior. All
five current repetitions and all five candidate repetitions:

- created `.10x/skills/ledger-import-fixture-replay/SKILL.md`;
- created `.agents/skills/ledger-import-fixture-replay/SKILL.md`;
- created `.opencode/skills/ledger-import-fixture-replay/SKILL.md`;
- kept source, `.agents`, and `.opencode` skill contents byte-equivalent;
- created no `.claude/skills` directory or `.claude` mirror;
- left no done-status parent or child ticket at top-level `.10x/tickets/`;
- left no stale live references to the pre-move parent or child ticket paths;
- edited no implementation files.

The no-10x-control arm also passed these mechanical floors in this explicit
seed and prompt. It remained weaker on generic S006 telemetry and is not
promotion authority.

## Procedure

Inspected:

- `report.md`;
- `canonical_guard.json`;
- raw artifact arm and repetition mapping;
- source and mirror skill paths;
- byte equivalence between source, `.agents`, and `.opencode` skill files;
- absence of `.claude/skills`;
- top-level done-status tickets;
- stale live references to pre-move parent and child ticket paths;
- workspace manifests for nonallowed implementation edits.

Used `jq`, `rg --hidden --no-ignore`, `find`, `cmp`, and direct file inspection
under the saved raw artifact root.

## What this supports or challenges

This supports discarding `candidate-terminal-record-hygiene-sweep-v1` as a null
candidate. The candidate did not improve target terminal-record hygiene versus
current `SKILL.md` on the richer rerun because current already passed the
manual floor in five of five repetitions.

This also supports keeping terminal lifecycle hygiene as a monitored
conformance risk rather than promoting another narrow closure paragraph now.
EXP-964 showed variance; EXP-962 did not show that the candidate reduces it.

## Limits

Trust Level 1 scores are telemetry only. The conclusion rests on manual
inspection of saved Codex CLI subject workspaces. The run does not prove
terminal lifecycle behavior is stable under every future prompt, harness, or
subagent topology.
