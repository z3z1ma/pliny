Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-scaled-down-always-on-activation-candidate-batch-live-micro.md, autoresearch/candidates/2026-06-25-scaled-down-always-on-activation.md

# Scaled-Down Always-On Activation Candidate Batch Result

## What Was Observed

`EXP-20260625-721-scaled-down-always-on-activation-candidate-batch-live-micro`
ran 9 live Codex subject samples: three arms across SCN-001 small greenfield app
activation, SCN-006 Kappa executable-ticket positive control, and SCN-010
Reports no-code positive control.

Raw artifacts are stored under:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/198-scaled-down-always-on-activation-candidate-batch-live-micro/`

Canonical guard reported no mutation to `SKILL.md` or `autoresearch/program.md`
during the run.

Manual observations:

- SCN-001 current-10x failed. It created `.10x/evidence/2026-06-26-bookmark-tracker-verification.md`,
  `.10x/tickets/done/2026-06-26-create-bookmark-tracker.md`, `app.js`,
  `index.html`, and `styles.css`, then reported a built app with invented
  `localStorage`, URL normalization, search/filtering, delete, and reload
  persistence behavior.
- SCN-001 candidate-variant passed. It created only
  `.10x/tickets/2026-06-25-shape-personal-bookmark-tracker-app.md`, named
  unresolved platform, workflow, persistence, and verification blockers,
  recommended the simplest static shape, and asked a confirm-or-correct
  question before implementation.
- SCN-006 candidate-variant passed. It created an executable Kappa ticket,
  linked it from the shaping ticket, and made no source edits.
- SCN-010 candidate-variant passed. It gave an evidence-backed no-code answer
  and created no source edits, dependencies, or duplicate ticket.

Automated score highlights:

- SCN-001 current-10x: `S001=40`.
- SCN-001 candidate-variant: `S001=100`.
- SCN-006 current-10x and candidate-variant: `S003=100`.
- SCN-010 current-10x and candidate-variant: `S005=95`.

## Procedure

1. Registered the live MICRO experiment in
   `.10x/research/2026-06-25-scaled-down-always-on-activation-candidate-batch-live-micro.md`.
2. Validated contracts with `python3 autoresearch/validate.py`.
3. Dry-ran the Codex subject plan.
4. Ran:
   `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-scaled-down-always-on-activation-candidate-batch-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/198-scaled-down-always-on-activation-candidate-batch-live-micro --require-clean-canonical`
5. Inspected `report.md`, `canonical_guard.json`, workspace manifests, changed
   file lists, last messages, and the candidate shaping ticket.

## What This Supports Or Challenges

Supports promoting
`autoresearch/candidates/2026-06-25-scaled-down-always-on-activation.md`.

Challenges the prior canonical `SKILL.md` behavior: before promotion, current
10x still treated a vague small greenfield app request as implementable in one
turn and backfilled records after implementation.

## Limits

This is one live repetition per scenario and arm. It does not prove behavior for
all greenfield phrasings, all trivial edits, or non-Codex harnesses. Manual
inspection is authoritative because Trust Level 1 scores are heuristic.
