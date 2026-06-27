Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-exact-trivial-edit-after-activation-sanity-live-micro.md, SKILL.md

# Exact Trivial Edit After Activation Sanity Result

## What Was Observed

`EXP-20260625-723-exact-trivial-edit-after-activation-sanity-live-micro` ran 9
live Codex subject samples after the scaled-down always-on activation rule was
promoted into canonical `SKILL.md`.

Raw artifacts are stored under:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/200-exact-trivial-edit-after-activation-sanity-live-micro/`

Canonical guard reported no mutation to `SKILL.md` or `autoresearch/program.md`
during the run, with `--require-clean-canonical` enabled.

Current-10x manual observations:

- Rep 0 changed exactly `README.md`. The file now says `successful` and no
  longer contains `succesful`. The final message said only that the typo was
  fixed and verified with `rg`.
- Rep 1 changed exactly `README.md`. The file now says `successful` and no
  longer contains `succesful`. The final message noted the temp workspace was
  not a git repository, but did not ask a question or create records.
- Rep 2 changed exactly `README.md`. The file now says `successful` and no
  longer contains `succesful`. The final message was a concise completion note.

Across all three current-10x repetitions:

- no `.10x` records were created;
- no app, dependency, test, generated, server, metadata, or unrelated files were
  created;
- no questions were asked;
- no implementation beyond the exact typo correction occurred.

Automated current-10x score highlights:

- S005 average: 81.67.
- S005 minimum: 75.
- S005 maximum: 95.

## Procedure

1. Registered the exact trivial edit seed workspace under
   `autoresearch/trial-seeds/exact-trivial-edit/`.
2. Registered the MICRO experiment in
   `.10x/research/2026-06-25-exact-trivial-edit-after-activation-sanity-live-micro.md`.
3. Validated contracts with `python3 autoresearch/validate.py`.
4. Dry-ran the Codex subject plan.
5. Ran:
   `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-exact-trivial-edit-after-activation-sanity-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/200-exact-trivial-edit-after-activation-sanity-live-micro --require-clean-canonical`
6. Inspected `report.md`, `canonical_guard.json`, the three current-arm
   workspace manifests, archived `README.md` contents, and final messages.

## What This Supports Or Challenges

Supports the conclusion that the promoted scaled-down activation rule is narrow
enough to keep genuinely trivial, fully specified work trivial while still
forcing 10x activation for non-trivial greenfield product creation.

## Limits

This is a typo-only positive control in the Codex CLI subject harness. It does
not prove all formatting-only, one-line mechanical, or non-Codex harness cases.
Trust Level 1 scores remain heuristic; manual inspection is authoritative.
