Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-repository-triage-record-quality-scn005-live-micro.md

# Repository Triage Record Quality Result

## What Was Observed

Ran `EXP-20260625-975-repository-triage-record-quality-scn005-live-micro` with
one repetition each for no-10x-control, current-10x, and duplicate-current
candidate arms.

Raw artifacts:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/175-repository-triage-record-quality-scn005-live-micro/`

Canonical guard:

- `SKILL.md` before and after hash:
  `b46696627d94d707a26665cb8272ec90d0c9e0c64ea54cf81c2b91b980c57332`
- `autoresearch/program.md` before and after hash:
  `81032b42894e93727fd54ec1aa457edaa3a6e6e1a049dc2e76c52aab77c3d4d5`
- `unchanged_during_run`: `true`

Current-10x workspace:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/175-repository-triage-record-quality-scn005-live-micro/workspaces/sha256-5bbc7ce5d3e10b1c6ae9bd233ecdf711cdfea19ac53012a20a497fd851650d00/`

Current-10x inspected:

- active spec `.10x/specs/account-export-csv.md`;
- active parent ticket
  `.10x/tickets/2026-06-25-account-export-hardening-parent.md`;
- active test ticket
  `.10x/tickets/2026-06-25-add-account-export-email-redaction-test.md`;
- done visible-filter ticket
  `.10x/tickets/done/2026-06-24-add-account-export-visible-filter.md`;
- cancelled legacy adapter ticket
  `.10x/tickets/cancelled/2026-06-23-build-legacy-account-export-adapter.md`;
- stale row-limit research
  `.10x/research/2025-12-01-account-export-vendor-row-limit.md`;
- `src/accountExport.js`;
- `src/accountExport.test.js`;
- `docs/account-export.md`;
- `package.json`.

Current-10x changed only these subject workspace records:

- `.10x/tickets/2026-06-25-account-export-hardening-parent.md`;
- `.10x/tickets/2026-06-25-add-account-export-email-redaction-test.md`;
- `.10x/tickets/2026-06-25-remove-account-export-email-from-docs.md`.

The new docs ticket was bounded to removing `email` from current operator docs.
The existing test ticket was reused rather than duplicated. The parent ticket
was updated to record triage progress and clear the triage blocker. Done,
cancelled, and stale research records remained historical. Source, tests, docs,
and package metadata were not changed.

Duplicate-current workspace:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/175-repository-triage-record-quality-scn005-live-micro/workspaces/sha256-1559060f824c426b43b65810646eb15ea4b498b954e0f81c7d5a8b41dd8d9258/`

Duplicate-current made the same three record changes and no source/test/doc
edits.

No-10x-control workspace:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/175-repository-triage-record-quality-scn005-live-micro/workspaces/sha256-a2fd0e001a351c0a091a0800e390bda493849b363b74dfc7b3b8aa65c53f3ea9/`

Because the no-10x-control environment removes inherited `.10x`, it opened one
new docs ticket but did not exercise reuse of the active parent or active test
ticket owners.

Trust Level 1 automated scoring:

- current-10x: S002=50, S005=100;
- duplicate-current: S002=50, S005=100;
- no-10x-control: S002=100, S005=100.

Manual inspection classifies the current and duplicate-current S002 failures as
false negatives. The scorer treated updates to multiple relevant existing
records as record spam, but the scenario expected exactly that reuse plus one
new docs owner.

## Procedure

Executed:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-repository-triage-record-quality-scn005-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/175-repository-triage-record-quality-scn005-live-micro --require-clean-canonical
```

Manual inspection used:

- `plan.json` to map sample hashes to arms;
- `canonical_guard.json` to confirm canonical files stayed unchanged;
- `report.md` for score vectors and floor failures;
- subject workspace manifests to inspect changed files;
- `stdout.jsonl` command events to verify inspected records, source, tests, and
  docs;
- archived subject workspace ticket contents.

## What This Supports Or Challenges

Supports the conclusion that current `SKILL.md` can perform broader repository
record-quality triage while preserving record economy and lifecycle authority.
It challenges the need for a new repository-triage instruction in `SKILL.md`.

## Limits

This is one one-turn Codex CLI MICRO. It does not prove longer repeated-session
record maintenance, app-level subagent orchestration, or non-Codex harness
behavior. The prompt directly requested triage and owner reuse, so lower-
assistance variants may still be useful if this behavior regresses elsewhere.
