---
id: critique:claude-per-rule-hook-implementation-review
kind: critique
status: final
created_at: 2026-04-26T05:15:49Z
updated_at: 2026-04-26T05:15:49Z
scope:
  kind: repository
  repositories:
    - repo:root
review_target: ticket:cldrel01 per-rule Claude SessionStart hook implementation
links:
  ticket:
    - ticket:cldrel01
  evidence:
    - evidence:claude-sessionstart-stdout-context
  critique:
    - critique:claude-hook-context-simplification-review
external_refs:
  claude_code_docs:
    - https://code.claude.com/docs/en/hooks
    - https://code.claude.com/docs/en/plugins
---

# Summary

Oracle critique of the per-rule Claude `SessionStart` hook implementation for
`ticket:cldrel01`.

# Review Target

Reviewed implementation surfaces:

- `hooks/hooks.json`
- deleted generated-rule scripts under `scripts/claude-*.sh`
- `INSTALL.md`
- `examples/adapters/claude-plugin-install/README.md`
- `evidence:claude-sessionstart-stdout-context`
- `packet:ralph-ticket-cldrel01-20260426T050555Z`

# Verdict

`pass_with_findings`

The per-rule `SessionStart` design is acceptable to keep. It should not be
rejected. The implementation removes the old sync/guard/cleanup stack and
validates all seven rules in same-session startup context. Remaining issues are
documentation reconciliation and release-risk disclosure rather than code blockers.

# Findings

## FIND-001: Canonical wiki still described deleted sync/guard behavior

Severity: medium
Confidence: high
Disposition: resolved

Observation:

The first review pass found `wiki:harness-adapter-package-pattern` still described
the Claude example as generated-rule sync plus restart guard, even though product
files now use per-rule hook output.

Why it matters:

The wiki is the accepted explanation layer. Leaving it stale would cause future
agents to inherit the wrong Claude adapter model.

Follow-up:

Resolved by updating `wiki:harness-adapter-package-pattern` to describe per-rule
hook output as current and the sync/guard model as historical evidence.

Challenges:

- `ticket:cldrel01`
- `wiki:harness-adapter-package-pattern`

## FIND-002: Fixture wording counted four wrong solutions as three

Severity: low
Confidence: high
Disposition: resolved

Observation:

The Claude adapter fixture said "three wrong solutions" while listing four.

Why it matters:

Minor operator-facing polish issue that weakens fixture clarity.

Follow-up:

Resolved by changing the wording to "four wrong solutions".

Challenges:

- `examples/adapters/claude-plugin-install/README.md`

# Evidence Reviewed

- `hooks/hooks.json`
- `INSTALL.md`
- `examples/adapters/claude-plugin-install/README.md`
- deletion status for `scripts/claude-sync-rules.sh`,
  `scripts/claude-loom-restart-guard.sh`, and `scripts/claude-clean-rules.sh`
- `evidence:claude-sessionstart-stdout-context`
- `packet:ralph-ticket-cldrel01-20260426T050555Z`
- Fixer validation output: `claude plugin validate .`, startup visibility probe,
  repeated ordering probes, deleted-script reference checks, and `git diff --check`

# Residual Risks

- `clear` and `compact` are configured but not runtime-validated.
- Installed marketplace mode and package/cache contents remain unproven.
- Windows behavior is untested; hooks depend on POSIX-like `sleep`, `printf`, and
  `cat`.
- Runtime skill and command-wrapper invocation from an installed plugin remains
  untested.
- Ordering after `01-core-identity.md` remains nondeterministic; source markers
  mitigate this but strict numeric ordering is not proven.
- Evidence depends on Claude model self-report from loaded context, not direct
  internal context inspection.
- Future rule growth past the 10,000-character per-output cap would require
  splitting or another delivery design.

# Required Follow-up

- Record the per-rule hook-output implementation decision in `ticket:cldrel01`.
- Keep the ticket out of `closed` until acceptance explicitly handles or defers
  the residual release risks.
- If broad marketplace release is pursued, validate installed plugin behavior,
  package/source contents, and runtime skill/command invocation.

# Acceptance Recommendation

complete pending acceptance
