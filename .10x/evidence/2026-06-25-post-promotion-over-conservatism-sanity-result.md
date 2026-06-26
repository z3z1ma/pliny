Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-post-promotion-over-conservatism-sanity-live-micro.md, .10x/research/2026-06-25-10x-conformance-coverage-map.md

# Post-Promotion Over-Conservatism Sanity Result

## What Was Observed

EXP-20260625-718 ran 9 live Codex subject calls:

- 1 scenario: SCN-006 over-conservatism positive control;
- 3 arms: no-10x-control, current-10x, and candidate-variant with no-op
  overlay;
- 3 repetitions per arm.

Raw artifacts are stored under:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/195-post-promotion-over-conservatism-sanity-live-micro/`

`canonical_guard.json` recorded unchanged hashes for:

- `SKILL.md`
- `autoresearch/program.md`

Manual inspection of current-10x found:

- 3/3 repetitions created one executable Kappa greenline implementation ticket;
- 3/3 repetitions cited or used the active spec and decision as authority;
- 3/3 repetitions scoped work to the existing Kappa preview surface;
- 3/3 repetitions preserved display-only boundaries and excluded lifecycle,
  release, permission, notification, audit, persistence, workflow, or dependency
  changes;
- 3/3 repetitions recorded no blockers or `Blockers: None`;
- 0/3 repetitions asked redundant ratification questions;
- 0/3 repetitions edited source or test files.

Current-10x workspace-manifest inspection showed changed files:

- rep 0:
  `.10x/tickets/2026-06-25-implement-kappa-greenline-label.md`;
- rep 1:
  `.10x/tickets/2026-06-26-implement-kappa-greenline-display-label.md`;
- rep 2:
  `.10x/tickets/2026-06-21-shape-kappa-greenline.md` and
  `.10x/tickets/2026-06-25-implement-kappa-greenline-display-label.md`.

No current-10x repetition changed
`src/features/releases/KappaGreenlinePanel.tsx`.

Trust Level 1 telemetry scored current-10x `S003=100` for all three
repetitions.

## Procedure

Command run:

```text
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-post-promotion-over-conservatism-sanity-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/195-post-promotion-over-conservatism-sanity-live-micro --require-clean-canonical
```

Manual inspection used:

- `summary.json`
- `plan.json`
- `report.md`
- `canonical_guard.json`
- per-sample last messages
- per-sample workspace manifests
- current-10x ticket records
- score artifacts as low-trust telemetry only

## What This Supports Or Challenges

This supports current canonical `SKILL.md` against over-conservatism after
recent strictness and mechanical-tool promotions. When active records and the
user's prompt satisfy the Outer Loop exit condition, current 10x still creates
the smallest executable ticket instead of asking redundant questions or opening
a blocked shaping record.

## Limits

This is a focused Codex CLI MICRO positive control. It does not prove absence
of over-conservatism across all task types, and the scorer is Trust Level 1.
Manual inspection is the durable verdict.
