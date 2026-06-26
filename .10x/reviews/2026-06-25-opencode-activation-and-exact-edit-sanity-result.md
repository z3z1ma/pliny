Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Target: .10x/research/2026-06-25-opencode-activation-and-exact-edit-sanity-manual-micro.md
Verdict: pass

# OpenCode Activation And Exact Edit Sanity Result Review

## Target

Manual OpenCode MICRO `EXP-20260625-734-opencode-activation-and-exact-edit-sanity-manual-micro`
and evidence record:

`.10x/evidence/2026-06-25-opencode-activation-and-exact-edit-sanity-result.md`

## Findings

- **Pass:** Current-10x greenfield behavior matched the 10x activation
  invariant. The agent did not dismiss the app as too small for 10x, did not
  implement, and created only a blocked shaping ticket with concrete blockers
  and a recommended minimal contract.
- **Pass:** Current-10x exact-edit behavior matched minimalism. The subject
  `statusLabel.js` changed from `"Old"` to `"Archived"` for the archived case,
  and no `.10x` records were created.
- **Pass:** Clean no-10x greenfield control provided a useful contrast by
  directly creating app files and smoke-test artifacts.
- **Concern:** The first manual OpenCode calibration attempt exposed an
  isolation flaw: global OpenCode instructions can contaminate no-10x controls,
  and `--dir` alone was insufficient for the no-10x exact-edit cell. The
  accepted evidence uses corrected isolation, but future manual OpenCode runs
  should treat process `cwd` as part of the harness contract.

## Verdict

Pass. The result is strong enough to mark OpenCode activation sanity as
partially covered and does not justify a new `SKILL.md` mutation.

## Residual Risk

This does not cover Claude Code, oh-my-pi, OpenCode multi-turn follow-ups, or
larger app requests. The OpenCode manual harness should be hardened or
automated before relying on it for broad candidate promotion.
