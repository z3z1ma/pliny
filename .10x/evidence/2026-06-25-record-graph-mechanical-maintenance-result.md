Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-record-graph-mechanical-maintenance-scn009-live-micro.md

# Record Graph Mechanical Maintenance Result

## What Was Observed

Ran `EXP-20260625-974-record-graph-mechanical-maintenance-scn009-live-micro`
with two repetitions each for no-10x-control, current-10x, and
duplicate-current candidate arms.

Raw artifacts:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/174-record-graph-mechanical-maintenance-scn009-live-micro/`

Canonical guard:

- `SKILL.md` before and after hash:
  `b46696627d94d707a26665cb8272ec90d0c9e0c64ea54cf81c2b91b980c57332`
- `autoresearch/program.md` before and after hash:
  `81032b42894e93727fd54ec1aa457edaa3a6e6e1a049dc2e76c52aab77c3d4d5`
- `unchanged_during_run`: `true`

Current-10x workspaces:

- rep 0:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/174-record-graph-mechanical-maintenance-scn009-live-micro/workspaces/sha256-daf9e157838cfe70b3480a26cbba6f358951f59a02e514b9f04ba3aac2163242/`
- rep 1:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/174-record-graph-mechanical-maintenance-scn009-live-micro/workspaces/sha256-32439aa7361c6c7bfb723965256be0e15fe79d01e0d8b54eb26afc7b8033c01a/`

In both current repetitions:

- `.10x/tickets/2026-06-25-align-payout-export-csv.md` was moved to
  `.10x/tickets/done/2026-06-25-align-payout-export-csv.md`.
- Live references in `.10x/specs`, `.10x/tickets`, `.10x/evidence`,
  `.10x/reviews`, and `.10x/knowledge` were repaired to the terminal path.
- Old top-level path references remained in
  `.10x/research/2026-06-25-payout-export-maintenance-history.md` as historical
  prose and captured command output.
- The old top-level path also remained in the parent ticket's append-only
  progress log, paired with an appended completion note that live references now
  use the terminal path.
- No source or test files were present or changed.
- No tests ran and no implementation tickets were created.

Current operation mechanics:

- current rep 0 used `rg` discovery, `mkdir -p`, `mv`, a single `perl -0pi`
  rewrite over the live-reference file set, and `rg` validation.
- current rep 1 used the same compact pattern: `rg`, `mv`, `perl -0pi`, `git
  diff`, and targeted `rg` validation.

Trust Level 1 automated scoring gave current S004=65 and S006=45 in both
repetitions. Manual inspection overrides those scores because the scorer cannot
classify preserved historical old-path references correctly.

## Procedure

Executed:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-record-graph-mechanical-maintenance-scn009-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/174-record-graph-mechanical-maintenance-scn009-live-micro --require-clean-canonical
```

Manual inspection used:

- `plan.json` to map sample hashes to arms and repetitions;
- `canonical_guard.json` to verify canonical files stayed unchanged;
- archived subject workspaces to inspect moved files and path references;
- `stdout.jsonl` command events to inspect operation mechanics;
- `report.md` to capture Trust Level 1 score vectors.

## What This Supports Or Challenges

Supports the conclusion that current `SKILL.md` already handles dense terminal
ticket path maintenance with correct, economical mechanics. It challenges the
need for a new `SKILL.md` instruction about mechanical record maintenance.

## Limits

This proves one dense terminal-ticket move fixture under Codex CLI. It does not
prove repository-scale path repair, multi-day repeated maintenance, or
non-Codex harness behavior. The prompt explicitly encouraged simple mechanical
workflow, so a lower-assistance follow-up may still be useful later if this
behavior regresses.
