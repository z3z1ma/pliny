---
id: critique:claude-hook-context-simplification-review
kind: critique
status: final
created_at: 2026-04-26T03:52:16Z
updated_at: 2026-04-26T04:26:00Z
scope:
  kind: repository
  repositories:
    - repo:root
review_target: ticket:cldrel01 Claude hook-context simplification Ralph cycles
links:
  ticket:
    - ticket:cldrel01
  evidence:
    - evidence:claude-sessionstart-stdout-context
    - evidence:claude-plugin-hybrid
  critique:
    - critique:claude-plugin-integration-review
external_refs:
  claude_code_docs:
    - https://code.claude.com/docs/en/hooks
    - https://code.claude.com/docs/en/plugins
---

# Summary

Oracle critique of the Claude hook-context simplification work for
`ticket:cldrel01`, covering two Ralph/Fixer cycles and the resulting evidence.

# Review Target

The review targeted the decision whether to replace the accepted Claude
sync/guard prototype with same-session plugin context loading.

Reviewed surfaces:

- `ticket:cldrel01`
- `packet:ralph-ticket-cldrel01-20260426T030000Z`
- `packet:ralph-ticket-cldrel01-20260426T031800Z`
- `evidence:claude-sessionstart-stdout-context`
- current Claude hook/script product files after candidate restoration

# Verdict

`pass_with_findings`

The evidence is sufficient to reject the simple hook-context replacement and to
avoid a third implementation packet. The current sync/guard model should remain
the Claude release-hardening baseline while the ticket moves to the remaining
marketplace/package, installed-plugin, cleanup, scope, and platform questions.

# Findings

## FIND-001: Monolithic hook context does not satisfy full-rule loading

Severity: high
Confidence: high
Disposition: resolved

Observation:

The full-corpus raw stdout candidate and the monolithic structured
`hookSpecificOutput.additionalContext` candidate both appeared to Claude as a
previewed/truncated hook-output artifact. Later rule content such as
`07-validation-and-honesty.md` was not visible in the same-session probe.

Why it matters:

Loom's Claude adapter cannot claim always-on Loom rules are loaded if only the
first portion of the corpus is visible. Removing the sync/guard scripts on this
basis would be a fail-open install regression.

Follow-up:

Do not replace the sync/guard model with one full-corpus hook command.

Challenges:

- `ticket:cldrel01`
- `evidence:claude-sessionstart-stdout-context`

## FIND-002: Plugin-root static context is not validated under local plugin loading

Severity: medium
Confidence: high
Disposition: resolved

Observation:

The temporary plugin-root `CLAUDE.md` and plugin-root `.claude/rules/loom.md`
probe validated structurally but did not expose sentinels or early/middle/late
Loom rule content under local `--plugin-dir` startup.

Why it matters:

This blocks treating plugin-bundled static files as the replacement for generated
Claude rule synchronization in the validated local plugin path.

Follow-up:

Keep this scoped as `not validated under local --plugin-dir`; do not overstate it
as a universal Claude plugin limitation.

Challenges:

- `ticket:cldrel01`
- `evidence:claude-sessionstart-stdout-context`

## FIND-003: Chunked hook context is technical proof, not a release-preferred design

Severity: high
Confidence: high
Disposition: resolved

Observation:

The only passing full-rule hook-context candidate used 26 synchronous
`SessionStart` hook commands, each emitting a small structured additional-context
chunk below the observed preview threshold.

Why it matters:

That shape is more complex than the simplification it was meant to replace and
depends on Claude behavior that is not documented as a stable full-corpus static
instruction contract. It also remains untested for marketplace installs,
`clear`, `compact`, repeated reliability, Windows, startup latency, and token or
cache cost.

Follow-up:

Do not productize chunked hook context in this cycle. Record it as technically
possible but not release-preferred.

Challenges:

- `ticket:cldrel01`
- `evidence:claude-sessionstart-stdout-context`

# Evidence Reviewed

- `evidence:claude-sessionstart-stdout-context`
- `evidence:claude-plugin-hybrid`
- `packet:ralph-ticket-cldrel01-20260426T030000Z`
- `packet:ralph-ticket-cldrel01-20260426T031800Z`
- current `hooks/hooks.json` sync/guard hook shape
- current Claude sync, guard, and cleanup script references
- Oracle cycle 1 and cycle 2 review outputs

# Residual Risks

- Installed marketplace plugin behavior remains untested for the release path.
- Runtime skills and commands from an installed marketplace plugin remain
  unproven.
- Marketplace source/cache contents remain unaudited for broad release.
- Cleanup remains explicit because Claude docs do not describe a plugin uninstall
  lifecycle hook.
- POSIX hook script support on Windows remains unproven.
- Broad `loom@...` project-scope matching still needs a release decision.

# Required Follow-up

- Keep the current sync/guard rule-loading model as the release-hardening
  baseline.
- Route the next bounded work to marketplace package/source shape,
  installed-plugin skill and command runtime validation, scope matching, cleanup
  UX, platform support, and release-doc truthfulness.
- Do not run a third Fixer implementation packet for chunked hook context unless a
  new ticket or revised decision explicitly accepts its complexity risk.

Post-review addendum:

After this critique, `evidence:claude-sessionstart-stdout-context` recorded a
new per-rule raw stdout probe. That evidence challenges the assumption that the
only full-corpus hook-context alternative is arbitrary chunking. This critique's
`no third packet` recommendation still applies to the reviewed 26-command
chunking candidate, but the per-rule candidate needs fresh critique before any
product implementation.

# Acceptance Recommendation

active follow-up required
