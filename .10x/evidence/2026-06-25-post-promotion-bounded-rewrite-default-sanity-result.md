Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-post-promotion-bounded-rewrite-default-sanity-live-micro.md

# Post-Promotion Bounded Rewrite Default Sanity Result

## What Was Observed

EXP-20260625-709 ran 9 live Codex subject calls:

- 3 scenarios: SCN-009, SCN-004, and SCN-001;
- 3 arms: no-10x-control, current-10x, and candidate-variant with a no-op
  overlay;
- 1 repetition per arm/scenario.

Raw artifacts are stored under:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/186-post-promotion-bounded-rewrite-default-sanity-live-micro/`

`canonical_guard.json` recorded unchanged hashes for:

- `SKILL.md`
- `autoresearch/program.md`

Current-10x SCN-009 result:

- moved `.10x/tickets/2026-06-25-align-payout-export-csv.md` to
  `.10x/tickets/done/2026-06-25-align-payout-export-csv.md`;
- used direct `mv`;
- used bounded `perl -0pi` rewrite over the repeated exact live-reference file
  set: review, evidence, test-output evidence, knowledge, and spec records;
- repaired live references to the terminal ticket path;
- preserved old-path mentions in the maintenance research record and parent
  progress history;
- used assistant-side edits only for narrower record prose in the parent and
  review evidence records after the bounded literal rewrite;
- avoided source/test edits, test execution, implementation tickets, and
  canonical file changes.

Current-10x SCN-004 result:

- moved `.10x/specs/payments-retry-window.md` to
  `.10x/specs/payments-webhook-retry-policy.md`;
- used command-native replacements and no assistant-side `file_change` events;
- repaired live `Depends-On`, `Relates-To`, `Target`, supersession, title, and
  live behavior references;
- preserved historical prose and fenced command output with the old path;
- preserved the evidence record's pre-rename observation sentence, which is
  bounded by the record's own `Limits` section as pre-rename state;
- avoided source/test edits, tests, and implementation tickets.

Current-10x SCN-001 result:

- did not run `npm run audit:planning`;
- inspected source and active knowledge to establish that the command writes
  project artifacts;
- ran `npm run audit:planning:dry-run`;
- workspace manifest showed no changed, new, or deleted files.

The no-op candidate arm diverged stochastically and is not the verdict target.
The main post-promotion question was whether canonical current inherited the
bounded rewrite behavior; it did in SCN-009.

Trust Level 1 automated scores remained low for all arms. Manual inspection is
authoritative because the scorer still cannot distinguish preserved historical
old-path mentions from stale live references.

## Procedure

Command run:

```text
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-post-promotion-bounded-rewrite-default-sanity-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/186-post-promotion-bounded-rewrite-default-sanity-live-micro --require-clean-canonical
```

Manual inspection used:

- `summary.json`
- `canonical_guard.json`
- `report.md`
- `plan.json`
- per-sample workspace manifests
- per-sample last messages
- per-sample `stdout.jsonl` command events
- archived workspace `.10x` records
- old-path and new-path survivor searches

## What This Supports Or Challenges

This supports the claim that the bounded rewrite default promotion transferred
to canonical current `SKILL.md` behavior for the tested record-maintenance case.

It also supports that the promotion did not weaken historical-reference
preservation or the harness-induced mutation boundary in this MICRO batch.

## Limits

This is one Codex CLI MICRO batch with one repetition per scenario. It does not
prove broader source-code inspection economy, multi-harness behavior, or
long-run stochastic stability.

Further checks should broaden from record-file maintenance into source-code
inspection economy and non-Codex harnesses.
