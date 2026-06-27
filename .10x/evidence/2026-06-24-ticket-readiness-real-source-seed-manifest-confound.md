Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-ticket-readiness-real-source-scn006-live-micro.md

# Ticket Readiness Real Source Seed Manifest Confound

## What Was Observed

The first attempted run of
`EXP-20260624-861-ticket-readiness-real-source-scn006-live-micro` to:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/061-ticket-readiness-real-source-scn006-live-micro/`

was interrupted after all three subject last messages were written because the
runner was stuck archiving an unexpectedly large workspace.

Inspection showed the seed workspace manifest contained:

```json
{
  "workspace": "."
}
```

The runner and validator resolved `workspace` relative to the canonical repo
root, not relative to the manifest directory. As a result, the subject workspace
included the whole 10x repository instead of only
`autoresearch/trial-seeds/ticket-readiness-real-source/workspace`.

## Procedure

1. Started the live run with `--require-clean-canonical`.
2. Observed no terminal output for an extended period after subject last-message
   artifacts were present.
3. Inspected process state and archived workspace manifests.
4. Found post-run files including canonical `SKILL.md`, `README.md`,
   `autoresearch/`, and historical `.10x/evidence/.storage/` artifacts.
5. Interrupted the wrapper while it was copying the oversized workspace archive.

## What This Supports Or Challenges

This challenges the validity of any artifacts under the `061-...` output root.
They are confounded and must not be used for candidate promotion.

This supports fixing seed workspace resolution so manifest-relative workspace
paths such as `"."` point at the manifest directory, and validating that the
resolved workspace contains its own workspace manifest.

## Limits

This evidence concerns harness setup, not candidate behavior. A clean rerun is
required before judging `candidate-ticket-readiness-gate-v1`.
