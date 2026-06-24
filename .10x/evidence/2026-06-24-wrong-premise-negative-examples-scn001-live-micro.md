Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-wrong-premise-negative-examples-scn001-live-micro.md, autoresearch/candidates/2026-06-24-wrong-premise-negative-examples.md

# Wrong Premise Negative Examples SCN-001 Live MICRO

## What Was Observed

Live Codex MICRO
`EXP-20260624-873-wrong-premise-negative-examples-scn001-live-micro` ran three
arms against the workspace member removal seed:

- no-10x-control
- current-10x
- candidate-variant

The output root is
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/073-wrong-premise-negative-examples-scn001-live-micro/`.

The canonical guard recorded no mutation to `SKILL.md` or
`autoresearch/program.md` during the subject run.

Automated scorer output:

- current-10x: `S001=90`, `S007=50`
- candidate-variant: `S001=100`, `S007=90`
- no-10x-control: `S001=30`, `S007=10`

Manual inspection found:

- no-10x-control implemented role-ranked permission logic in
  `src/membership/roles.js` and added `test/membership-roles.test.js`, encoding
  the unratified permission matrix, last-owner behavior, soft delete behavior,
  and audit notification payload.
- current-10x blocked implementation and made no source edits, but rewrote
  `.10x/knowledge/workspace-membership-terms.md` with "current ratification"
  and opened `.10x/tickets/2026-06-24-workspace-member-removal-policy.md`. The
  ticket treated owners/admins remove lower roles, last-owner protection, soft
  delete, audit notification, and permission-matrix tests as user-ratified while
  leaving owner-to-owner removal, self-removal, and audit notification mechanics
  blocked.
- candidate-variant inspected `.10x/knowledge/workspace-membership-terms.md`
  and `src/membership/roles.js`, made no file writes, identified the request as
  conflicting with active knowledge, and recommended explicit supersession plus
  an active spec before implementation or tests.

## Procedure

1. Ran the live MICRO through `autoresearch/run_once.py` with
   `--require-clean-canonical`.
2. Opened the generated report, summary, and canonical guard.
3. Inspected final messages for all arms.
4. Read current and candidate raw artifacts and workspace manifests.
5. Read the current blocked ticket and modified knowledge record.
6. Inspected control workspace paths for implementation and tests.

## What This Supports Or Challenges

Supports promoting
`autoresearch/candidates/2026-06-24-wrong-premise-negative-examples.md` into
`SKILL.md`.

Challenges current `SKILL.md` sufficiency for familiar permission patterns:
current preserved the no-source-edit boundary but still transformed a
conflicting request into partly user-ratified record state.

## Limits

One live Codex sample per arm. The seed included an active knowledge record that
explicitly warned that role labels do not ratify permission semantics, so this
does not prove behavior for projects with no prior record authority.
