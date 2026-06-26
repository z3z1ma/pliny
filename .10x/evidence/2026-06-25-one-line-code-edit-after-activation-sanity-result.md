Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-one-line-code-edit-after-activation-sanity-live-micro.md, SKILL.md

# One-Line Code Edit After Activation Sanity Result

## What Was Observed

`EXP-20260625-725-one-line-code-edit-after-activation-sanity-live-micro` ran 9
live Codex subject samples after the scaled-down always-on activation rule was
promoted into canonical `SKILL.md`.

Raw artifacts are stored under:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/202-one-line-code-edit-after-activation-sanity-live-micro/`

Canonical guard reported no mutation to `SKILL.md` or `autoresearch/program.md`
during the run, with `--require-clean-canonical` enabled.

Current-10x manual observations:

- Rep 0 changed exactly `statusLabel.js`. The file now returns `"Archived"` for
  `status === "archived"` and leaves the active/unknown branches unchanged.
- Rep 1 changed exactly `statusLabel.js`. The file now returns `"Archived"` for
  `status === "archived"` and leaves the active/unknown branches unchanged.
- Rep 2 changed exactly `statusLabel.js`. The file now returns `"Archived"` for
  `status === "archived"` and leaves the active/unknown branches unchanged.

Across all three current-10x repetitions:

- no `.10x` records were created;
- no tests, dependency files, generated files, metadata, or unrelated files
  were created;
- no questions were asked;
- no implementation beyond the exact requested string replacement occurred.

Automated current-10x score highlights:

- S005 average: 81.67.
- S005 minimum: 75.
- S005 maximum: 95.

## Procedure

1. Registered the exact one-line code edit seed workspace under
   `autoresearch/fixtures/live-seeds/exact-one-line-code-edit/`.
2. Registered the MICRO experiment in
   `.10x/research/2026-06-25-one-line-code-edit-after-activation-sanity-live-micro.md`.
3. Validated contracts with `python3 autoresearch/validate.py`.
4. Dry-ran the Codex subject plan.
5. Ran:
   `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-one-line-code-edit-after-activation-sanity-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/202-one-line-code-edit-after-activation-sanity-live-micro --require-clean-canonical`
6. Inspected `report.md`, `canonical_guard.json`, the three current-arm
   workspace manifests, archived `statusLabel.js` contents, and final messages.

## What This Supports Or Challenges

Supports the conclusion that the promoted scaled-down activation rule preserves
trivial mechanical source edits. Always-on activation did not force records or
Outer Loop questioning when the edit was exact, bounded, and low-risk.

## Limits

This is a one-line JavaScript string edit in the Codex CLI subject harness. It
does not prove formatting-only, multi-file mechanical, or non-Codex harness
cases. Trust Level 1 scores remain heuristic; manual inspection is
authoritative.
