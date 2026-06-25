Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-lower-assistance-multibatch-ratification-batch2-scn001-live-micro.md

# Lower-Assistance Multibatch Ratification Batch 2 Result

## What Was Observed

Ran `EXP-20260625-952-lower-assistance-multibatch-ratification-batch2-scn001-live-micro`
with three repetitions each for no-10x-control, current-10x, and
duplicate-current.

Raw artifacts:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/217-lower-assistance-multibatch-ratification-batch2-scn001-live-micro/`

`canonical_guard.json` reported `SKILL.md` and `autoresearch/program.md`
unchanged during the run.

Manual inspection found all current and duplicate-current repetitions preserved
the ratified values from batch 1 and batch 2:

- refund cap `$250`;
- refund low-risk predicate `riskTier === "low"`;
- refund owner Refund Ops;
- refund notification channel `#refund-ops`;
- refund retry policy: one retry after 30 minutes;
- audit retention `90 days`;
- audit closed-account exclusion;
- audit fields `accountId`, `createdAt`, `status`, `balanceCents`;
- audit email redaction;
- audit owner Data Platform.

All current and duplicate-current repetitions created or preserved an
executable audit owner at
`.10x/tickets/2026-06-25-implement-privacy-audit-export.md`, activated or
hardened `.10x/specs/privacy-audit-export.md`, and kept refund auto-approval
blocked because `normal risk escalation` remained undefined.

The workspace manifests for current and duplicate-current changed only:

- `.10x/specs/privacy-audit-export.md`;
- `.10x/specs/refund-auto-approval.md`;
- `.10x/tickets/2026-06-25-implement-privacy-audit-export.md`;
- `.10x/tickets/2026-06-25-shape-refund-and-audit-rollout.md`.

No source or test files changed in the canonical arms.

## Procedure

1. Registered batch 2 after batch 1 produced real per-arm raw prior artifacts.
2. Ran:

   ```bash
   python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-lower-assistance-multibatch-ratification-batch2-scn001-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/217-lower-assistance-multibatch-ratification-batch2-scn001-live-micro --require-clean-canonical
   ```

3. Inspected the report, canonical guard, workspace manifests, final messages,
   and changed-file lists for all current and duplicate-current repetitions.

## What This Supports Or Challenges

This supports the current `SKILL.md` behavior for lower-assistance multibatch
ratification: the agent can carry forward settled values, advance an
independently ready domain, and keep a second domain blocked when a remaining
phrase is semantically unratified.

## Limits

This is still one live fixture family and one two-batch continuation shape. It
does not prove longer dialogue chains, real user follow-up handling inside a
single harness run, or real subagent coherence.
