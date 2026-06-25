Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-lower-assistance-record-maintenance-workflow-scn009-live-micro.md, autoresearch/candidates/2026-06-25-record-maintenance-command-line-economy.md

# Lower Assistance Record Maintenance Workflow Result

## What Was Observed

Ran `EXP-20260625-700-lower-assistance-record-maintenance-workflow-scn009-live-micro`
with two repetitions each for no-10x-control, current-10x, and
candidate-variant arms.

Raw artifacts:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/176-lower-assistance-record-maintenance-workflow-scn009-live-micro/`

Canonical guard:

- `SKILL.md` before and after hash:
  `b46696627d94d707a26665cb8272ec90d0c9e0c64ea54cf81c2b91b980c57332`
- `autoresearch/program.md` before and after hash:
  `81032b42894e93727fd54ec1aa457edaa3a6e6e1a049dc2e76c52aab77c3d4d5`
- `unchanged_during_run`: `true`

Current-10x workspaces:

- rep 0:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/176-lower-assistance-record-maintenance-workflow-scn009-live-micro/workspaces/sha256-a2791ecd4a87e1588cbcbd5367894d6d6c0b42e825fdf34104462d196ace9001/`
- rep 1:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/176-lower-assistance-record-maintenance-workflow-scn009-live-micro/workspaces/sha256-00e5c49abe27e21813d1630709114fa3f32425ff0b53f8d072fad14595bfed98/`

Candidate workspaces:

- rep 0:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/176-lower-assistance-record-maintenance-workflow-scn009-live-micro/workspaces/sha256-069a93f47e89eb727a0dbd5d56767b77d5e0bdcd0b68ef8e530c4a2752d44633/`
- rep 1:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/176-lower-assistance-record-maintenance-workflow-scn009-live-micro/workspaces/sha256-ec73858bc40a669648a9f7ecebdf81bcad8c36572bd6dbb1b3838922563d4dc6/`

In both current repetitions:

- the old top-level ticket file was absent after the run;
- `.10x/tickets/done/2026-06-25-align-payout-export-csv.md` existed after the
  run;
- live spec, parent ticket, evidence, review, and knowledge references were
  repaired to the terminal path;
- the historical research record retained old-path mentions and captured
  command output;
- source files were not edited, tests were not run, and implementation tickets
  were not created.

Current operation mechanics:

- rep 0 used `rg` and file inspection, then an assistant-side `file_change`
  applied updates across the affected live records and ticket move; no direct
  `mv` or bounded shell-native rewrite appeared in the command events.
- rep 1 used `mkdir -p` and direct `mv` for the ticket move, but repeated live
  reference updates were still performed through assistant-side `file_change`
  edits rather than a bounded shell-native literal rewrite.

In both candidate repetitions:

- the old top-level ticket file was absent after the run;
- `.10x/tickets/done/2026-06-25-align-payout-export-csv.md` existed after the
  run;
- live spec, parent ticket, evidence, review, and knowledge references were
  repaired to the terminal path;
- the historical research record retained old-path mentions and captured
  command output;
- source files were not edited, tests were not run, and implementation tickets
  were not created.

Candidate operation mechanics:

- rep 0 used `mkdir -p`, direct `mv`, and a bounded `perl -0pi` rewrite over
  the live-reference file set, then patched one stale parent note deliberately.
- rep 1 used `mkdir -p`, direct `mv`, and a bounded `perl -0pi` rewrite over
  the live-reference file set, then deliberately patched parent/review prose
  that was historical or stale after the mechanical replacement.

Trust Level 1 automated scoring:

- current-10x: S004=65 and S006=45 in both repetitions;
- candidate-variant: S004=65 and S006=45 in both repetitions;
- no-10x-control: S004=50 and S006=10 in both repetitions.

Manual inspection classifies the low current/candidate S004/S006 scores as
false negatives for correctness because the scorer cannot distinguish
historical old-path preservation from stale live references.

## Procedure

Executed:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-lower-assistance-record-maintenance-workflow-scn009-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/176-lower-assistance-record-maintenance-workflow-scn009-live-micro --require-clean-canonical
```

Manual inspection used:

- `plan.json` to map sample hashes to arms and repetitions;
- `canonical_guard.json` to verify canonical files stayed unchanged;
- `report.md` for score vectors;
- archived workspace manifests for changed-file sets;
- `stdout.jsonl` command events for operation mechanics;
- `rg` over archived workspaces for old and terminal ticket paths;
- direct inspection of parent ticket notes and final subject messages.

## What This Supports Or Challenges

Supports promoting the command-line economy candidate to regression testing. It
challenges the conclusion from EXP-974 that current `SKILL.md` already induces
economical mechanics: that earlier pass depended on prompt wording that
explicitly suggested a mechanical workflow.

## Limits

This is one lower-assistance Codex CLI MICRO. It proves current operation
quality is inconsistent on one dense terminal-ticket move and that candidate
improves the core operation. It does not yet prove the candidate is safe across
ambiguous historical reference repair, closure repair, or semantic-edit
scenarios.
