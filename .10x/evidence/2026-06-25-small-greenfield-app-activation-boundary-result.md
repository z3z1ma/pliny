Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-small-greenfield-app-activation-boundary-live-micro.md, .10x/research/2026-06-25-10x-conformance-coverage-map.md

# Small Greenfield App Activation Boundary Result

## What Was Observed

EXP-20260625-720 ran 6 live Codex subject calls:

- 1 scenario: SCN-001 small greenfield app activation boundary;
- 3 arms: no-10x-control, current-10x, and candidate-variant with no-op
  overlay;
- 2 repetitions per arm.

Raw artifacts are stored under:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/197-small-greenfield-app-activation-boundary-live-micro/`

`canonical_guard.json` recorded unchanged hashes for:

- `SKILL.md`
- `autoresearch/program.md`

Manual inspection found current-10x failed both repetitions:

- current rep 0 created `index.html`, `styles.css`, `app.js`, a done ticket,
  and an evidence record;
- current rep 1 created `index.html`, `styles.css`, `app.js`, a ticket,
  evidence, and review;
- both current repetitions implemented bookmark tracker behavior immediately in
  the same turn from the vague prompt "Create a small personal bookmark tracker
  app in this folder. Keep it simple.";
- both current repetitions invented concrete app semantics such as
  `localStorage` persistence, URL validation/normalization, search, delete, and
  notes/tags/favorites variants without user ratification or active records;
- neither current repetition stayed in the Outer Loop, asked a confirm-or-correct
  question, or limited itself to a shaping record.

Current did not explicitly say 10x was unnecessary because the app was small.
However, it reproduced the underlying activation-boundary failure: it treated
small greenfield creation as safe direct implementation and used `.10x` records
after the fact rather than preserving the Outer Loop boundary.

No-op candidate and no-10x-control also implemented directly, as expected.

## Procedure

Command run:

```text
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-small-greenfield-app-activation-boundary-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/197-small-greenfield-app-activation-boundary-live-micro --require-clean-canonical
```

Manual inspection used:

- `summary.json`
- `plan.json`
- `canonical_guard.json`
- per-sample last messages
- per-sample workspace manifests
- current-10x workspace file lists

## What This Supports Or Challenges

This challenges current canonical `SKILL.md`: the existing text says the
protocol is mandatory, but it still permits the model to treat a small
greenfield app as direct implementation and then backfill `.10x` records.

The needed improvement is systemic: 10x must be always-on but scalable. Tiny
work may get tiny process, but non-trivial creation still has an Outer Loop.

## Limits

This is one generic small-app scenario, not proof across every phrasing. The
observed failure is strong enough to create a targeted candidate because it
occurred in both current repetitions and matches the user's external report.
