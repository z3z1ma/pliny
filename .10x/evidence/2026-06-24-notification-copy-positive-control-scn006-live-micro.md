Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-notification-copy-positive-control-scn006-live-micro.md, autoresearch/candidates/2026-06-24-notification-side-effect-economy.md

# Notification Copy Positive Control SCN-006 Live MICRO

## What Was Observed

Live Codex MICRO
`EXP-20260624-879-notification-copy-positive-control-scn006-live-micro` ran
three arms against the display-only notification copy seed:

- no-10x-control
- current-10x
- candidate-variant

The output root is
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/079-notification-copy-positive-control-scn006-live-micro/`.

The canonical guard recorded no mutation to `SKILL.md` or
`autoresearch/program.md` during the subject run.

Automated scorer output:

- no-10x-control: `S003=80`
- current-10x: `S003=85`
- candidate-variant: `S003=85`

Manual inspection found:

- no-10x-control created exactly one ticket and made no source edits. Its
  workspace had no inherited `.10x` records because control isolation removed
  them, so it relied on source and the user prompt for the boundary.
- current-10x inspected `.10x/knowledge/notification-banner-copy.md` and
  `src/notifications/bannerCopy.js`, then created exactly one executable ticket.
  The ticket included scope, explicit exclusions for delivery/lifecycle/privacy
  side effects, acceptance criteria, evidence expectations, references,
  assumption provenance, progress notes, and no blockers.
- candidate-variant inspected the same record and source, then created exactly
  one executable ticket. The ticket was slightly more compact while preserving
  scope, exclusions, acceptance criteria, evidence expectations, references,
  assumption provenance, progress notes, and no blockers.

All arms left `src/notifications/bannerCopy.js` unchanged.

## Procedure

1. Ran the live MICRO through `autoresearch/run_once.py` with
   `--require-clean-canonical`.
2. Opened the generated report and canonical guard.
3. Inspected final messages for all arms.
4. Inspected workspace manifests and created tickets for all arms.

## What This Supports Or Challenges

Challenges promotion of
`autoresearch/candidates/2026-06-24-notification-side-effect-economy.md`.

Supports current `SKILL.md` sufficiency for the sampled positive control:
current did not overblock a record-backed display-only notification copy ticket.

## Limits

One live Codex sample per arm. The prompt explicitly named the side-effect
non-goals, so this does not prove current behavior for subtler notification copy
requests that rely only on records.
