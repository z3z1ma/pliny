Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-post-promotion-scaled-down-activation-sanity-live-micro.md, SKILL.md

# Post-Promotion Scaled-Down Activation Sanity Result

## What Was Observed

`EXP-20260625-722-post-promotion-scaled-down-activation-sanity-live-micro` ran
9 live Codex subject samples after the scaled-down activation rule was promoted
into canonical `SKILL.md`.

Raw artifacts are stored under:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/199-post-promotion-scaled-down-activation-sanity-live-micro/`

Canonical guard reported no mutation to `SKILL.md` or `autoresearch/program.md`
during the run. The guard was not configured with `--require-clean-canonical`
because the run intentionally tested a dirty promoted `SKILL.md` before commit.

Current-10x observations:

- SCN-001 passed. Current created only
  `.10x/tickets/2026-06-25-shape-bookmark-tracker-app.md`, left app/source/test
  files untouched, named platform, persistence, workflow, and verification
  blockers, recommended a single-file static `index.html` app, and asked three
  confirm-or-correct blocker questions.
- SCN-006 passed. Current created
  `.10x/tickets/2026-06-26-implement-kappa-greenline-label.md`, updated the
  shaping ticket, inspected source read-only, and made no source edits.
- SCN-010 passed. Current made an evidence-backed no-code answer citing the
  active server-owned export decision and existing `ReportsToolbar` /
  `reportExportUrl` wiring, with no source edits, dependency changes, or
  duplicate ticket.

Automated current-10x score highlights:

- SCN-001: `S001=100`, `S007=75`.
- SCN-006: `S003=100`.
- SCN-010: `S005=95`, `S007=25`.

## Procedure

1. Promoted the scaled-down activation rule into `SKILL.md`.
2. Registered the post-promotion MICRO experiment in
   `.10x/research/2026-06-25-post-promotion-scaled-down-activation-sanity-live-micro.md`.
3. Validated contracts with `python3 autoresearch/validate.py`.
4. Dry-ran the Codex subject plan.
5. Ran:
   `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-post-promotion-scaled-down-activation-sanity-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/199-post-promotion-scaled-down-activation-sanity-live-micro`
6. Inspected `report.md`, `canonical_guard.json`, current-arm workspace
   manifests, changed file lists, last messages, the SCN-001 shaping ticket, and
   the SCN-006 executable ticket.

## What This Supports Or Challenges

Supports the conclusion that the promoted canonical `SKILL.md` fixes the
small-greenfield activation boundary while preserving decisive ticket creation
and no-code minimalism.

## Limits

This is one live repetition per scenario. It does not cover every trivial edit,
all greenfield phrasings, or non-Codex harness behavior. Trust Level 1 scores
remain heuristic; manual inspection is authoritative.
