---
id: ticket:cldrel01
kind: ticket
status: closed
change_class: release-packaging
risk_class: high
created_at: 2026-04-26T01:04:44Z
updated_at: 2026-04-28T18:47:27Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:loom-install-experience
  plan:
    - plan:install-experience-harness-adapters
  research:
    - research:loom-install-distribution-methods
  wiki:
    - wiki:harness-adapter-package-pattern
  ticket:
    - ticket:q7h1d05q
  evidence:
    - evidence:claude-plugin-hybrid
    - evidence:claude-sessionstart-stdout-context
  critique:
    - critique:claude-plugin-integration-review
    - critique:claude-hook-context-simplification-review
    - critique:claude-per-rule-hook-implementation-review
depends_on: []
---

# Summary

Simplify and harden the accepted local/prototype Claude plugin integration for
broad marketplace-style distribution, with a specific decision on whether to
replace generated rule-file synchronization with same-session `SessionStart`
context emitted from bundled rule files.

# Context

`ticket:q7h1d05q` accepted the Claude hybrid plugin as a local/prototype
integration. Its acceptance decision explicitly left release-packaging risks
outside that prototype: broad `source: "./"`, explicit cleanup rather than
uninstall lifecycle support, unproven installed-plugin skill/command invocation,
broad `loom@...` project-scope matching, and unproven Windows/non-bash support.

`evidence:claude-sessionstart-stdout-context` changed the release-hardening shape
by showing that small `SessionStart` hook output can be visible in the same Claude
startup session. Ralph validation rejected monolithic full-corpus hook context,
plugin-root static files, and arbitrary chunking as the release-preferred path.

Operator-guided probing found the clean variant: seven per-rule raw stdout hook
outputs, each under Claude's documented 10,000-character hook-output cap. Ralph
iteration 3 implemented that route in `hooks/hooks.json`, removed the old
sync/guard/cleanup scripts, and validated all seven rules visible in same-session
startup context without preview/truncation. Oracle critique accepted the
implementation with residual release risks.

# Why Now

The project has chosen the per-rule hook-output path for the Claude adapter. The
remaining work is final acceptance disposition for release risks that were not in
scope for the implementation pass.

# Scope

- decide whether Claude distribution needs a narrower package artifact instead of
  marketplace source `./`
- decide whether to replace `scripts/claude-sync-rules.sh`,
  `scripts/claude-loom-restart-guard.sh`, and `scripts/claude-clean-rules.sh`
  with a simple `SessionStart` hook that emits bundled rules from
  `${CLAUDE_PLUGIN_ROOT}/rules/*.md`
- validate the full Loom rule corpus, not only a marker file, through same-session
  hook context
- compare raw stdout `cat` against structured
  `hookSpecificOutput.additionalContext` for correctness, quoting, and visibility
- validate or explicitly defer `startup`, `clear`, and `compact` behavior
- inspect or validate marketplace cache contents for the chosen package source
- validate runtime skill and command invocation from an installed marketplace
  plugin, not only from `--plugin-dir`
- decide whether project-scope detection should require exact `loom@agent-loom`
  identity instead of broad `loom@...`
- decide the cleanup UX for plugin disable/uninstall in the absence of a Claude
  uninstall hook
- decide whether POSIX shell hooks are acceptable for supported Claude platforms or
  whether a cross-platform helper is required
- update install docs, fixture notes, evidence, and critique if the prototype is
  promoted to release-grade distribution

# Non-goals

- do not reopen the local/prototype acceptance from `ticket:q7h1d05q`
- do not replace Loom always-on rules with a Claude custom agent
- do not make generated Claude rule files canonical Loom source
- do not keep the old sync-script complexity if the hook-context path proves the
  same rule-loading behavior more simply
- do not claim the hook-context path is release-ready from the marker-file probe
  alone

# Acceptance Criteria

- package source and cache contents are validated or intentionally constrained
- the ticket records a clear decision: keep sync-script rule installation, replace
  it with `SessionStart` hook-context loading, or defer with rationale
- if hook-context loading is chosen, the sync, guard, and cleanup scripts are
  removed or made explicitly obsolete
- if hook-context loading is rejected, the current sync/guard model remains
  documented as the release-hardening baseline
- full ordered Loom rule hook-context alternatives are validated or rejected with
  evidence before any replacement is accepted
- raw stdout versus structured `hookSpecificOutput.additionalContext` is decided
  with evidence for any hook-context replacement
- `startup`, `clear`, and `compact` event coverage is validated or explicitly
  scoped
- installed marketplace plugin skills and commands are exercised or the gap is
  explicitly accepted with rationale
- project-scope matching behavior is narrowed or explicitly accepted as broad
- cleanup behavior for disable/uninstall is documented and validated as far as
  Claude supports
- platform support for hook scripts is stated truthfully
- release docs distinguish local/prototype install from broad marketplace
  distribution

# Coverage

Covers:

- None - no spec-owned acceptance IDs exist. This ticket owns the release
  hardening questions left by `ticket:q7h1d05q`.

# Claim Matrix

| Claim | Coverage | Evidence | Notes |
| --- | --- | --- | --- |
| Claude local/prototype hybrid integration is accepted. | supported | `ticket:q7h1d05q`, `evidence:claude-plugin-hybrid`, `critique:claude-plugin-integration-review` | This ticket must not relitigate local/prototype acceptance. |
| Claude marketplace source `./` is release-ready. | pending | None | Requires cache-content audit or narrower package decision. |
| Installed marketplace plugin skills/commands work at runtime. | pending | None | Local prototype validated rules and install shape, not installed-plugin skill/command invocation. |
| `SessionStart` raw stdout can deliver small same-session Claude context. | supported | `evidence:claude-sessionstart-stdout-context` | Marker-file probe succeeded with local `--plugin-dir`. |
| Monolithic `SessionStart` hook context can load the full ordered Loom rule corpus. | challenged | `evidence:claude-sessionstart-stdout-context`, `critique:claude-hook-context-simplification-review` | Raw stdout and structured additional context both appeared previewed/truncated for the full corpus. |
| Plugin-root `CLAUDE.md` or `.claude/rules/loom.md` can replace sync-script rule installation. | challenged | `evidence:claude-sessionstart-stdout-context`, `critique:claude-hook-context-simplification-review` | Not visible under local `--plugin-dir` startup probe. |
| Chunked structured `SessionStart` hook context can expose the full corpus in a local startup probe. | supported_narrowly | `evidence:claude-sessionstart-stdout-context`, `critique:claude-hook-context-simplification-review` | One 26-command probe exposed early/middle/late rule content, but the design is not release-preferred. |
| Per-rule raw `SessionStart` hook stdout can expose the full corpus in local startup probes. | supported | `evidence:claude-sessionstart-stdout-context`, `critique:claude-per-rule-hook-implementation-review` | Final repository implementation saw all seven rule files without preview/truncation, and `01-core-identity.md` appeared first in three repeated startup probes. Strict order after that remains best effort. |
| Sync/guard rule loading remains the Claude release-hardening baseline. | superseded | `evidence:claude-plugin-hybrid`, `evidence:claude-sessionstart-stdout-context`, `critique:claude-per-rule-hook-implementation-review` | The generated-rule sync, restart guard, and cleanup scripts were removed after per-rule hook output was implemented and accepted by critique. |

# Blockers

None.

# Next Move / Next Route

Acceptance review for the per-rule Claude adapter path. Do not launch another
Fixer/Oracle cycle in this sequence unless a new acceptance decision scopes a
separate release-hardening ticket for marketplace packaging, Windows behavior, or
installed-plugin runtime invocation.

# Ralph Readiness

Next bounded iteration:
None for this implementation sequence. Future broad-release work should become a
separate ticket if the operator wants to validate installed marketplace mode,
Windows shell behavior, or runtime skill/command invocation.

Write boundary:
Claude plugin/marketplace metadata, Claude-specific docs/examples, release
packaging fixture files if needed, linked evidence/research/ticket records. Do not
change canonical `rules/`, `skills/`, or `commands/` except to record a source
bug in follow-up work.

Likely verification posture:
Observation-first. Capture installed-plugin behavior and package/source contents
under temporary project or home state. Avoid mutating real user Claude settings.

Expected output contract:
Release-packaging decision or narrowed risk, changed files, validation commands
and outputs, remaining limitations, critique recommendation, and ticket state
recommendation.

# Evidence

Evidence so far:

- `evidence:claude-plugin-hybrid`
- `evidence:claude-sessionstart-stdout-context`
- `critique:claude-plugin-integration-review`
- `critique:claude-hook-context-simplification-review`
- `critique:claude-per-rule-hook-implementation-review`

Expected evidence:

- marketplace cache-content inspection
- installed plugin runtime skill/command invocation proof or accepted limitation
- cleanup/disable validation or documented unsupported lifecycle
- platform support validation or explicit platform limitation

# Critique Disposition

Risk class: high

Critique policy: mandatory

Policy rationale:
This ticket may change Claude's rule-loading mechanism and remove fail-closed
sync/guard behavior. A bad result can mislead operators into thinking Loom is
loaded when it is not, so adversarial review is required before acceptance.

Findings:

- `critique:claude-hook-context-simplification-review` FIND-001: monolithic hook
  context does not satisfy full-rule loading.
- `critique:claude-hook-context-simplification-review` FIND-002: plugin-root
  static context is not validated under local plugin loading.
- `critique:claude-hook-context-simplification-review` FIND-003: chunked hook
  context is technical proof, not a release-preferred design.
- `critique:claude-per-rule-hook-implementation-review` FIND-001: canonical wiki
  still described deleted sync/guard behavior; resolved by updating
  `wiki:harness-adapter-package-pattern`.
- `critique:claude-per-rule-hook-implementation-review` FIND-002: Claude adapter
  fixture wording counted four wrong solutions as three; resolved in
  `examples/adapters/claude-plugin-install/README.md`.

Disposition status: mandatory critique completed for the per-rule implementation.
Future release-packaging mutations still need critique proportional to risk.

# Wiki Disposition

`wiki:harness-adapter-package-pattern` now records the accepted per-rule Claude
hook-output adapter shape and treats the older generated-rule sync/guard model as
historical evidence.

# Acceptance Decision

Accepted by: operator
Accepted at: 2026-04-28T18:47:27Z
Basis: Per-rule hook implementation, startup validation, documentation updates,
wiki update, and mandatory critique are complete.
Residual risks: Installed marketplace mode, package/cache contents, Windows shell
behavior, `clear|compact` runtime event behavior, and installed plugin
skill/command invocation remain unvalidated and are accepted as residual release
risks for this ticket's closure.

# Dependencies

Related to closed `ticket:q7h1d05q`; no hard dependency blocks the remaining
release-hardening work.

# Journal

- 2026-04-26: created during Claude effort retrospective to keep release-grade
  residual risks from living only in the closed prototype ticket or chat.
- 2026-04-26: promoted to ready after `evidence:claude-sessionstart-stdout-context`
  showed a simpler `SessionStart` stdout rule-loading path is plausible. The next
  iteration should decide whether this supersedes the sync-script prototype.
- 2026-04-26: moved to active and compiled
  `packet:ralph-ticket-cldrel01-20260426T030000Z` for Fixer iteration 1 of the
  Claude simplification spike.
- 2026-04-26: Fixer iteration 1 blocked the simple full-corpus hook replacement;
  Oracle agreed the block is valid. Compiled
  `packet:ralph-ticket-cldrel01-20260426T031800Z` for one validation-only spike of
  native plugin static context and, if needed, chunked hook context.
- 2026-04-26: Fixer iteration 2 found plugin-root static context was not visible
  under local `--plugin-dir`; chunked structured hook context worked in one local
  startup probe but required 26 synchronous hook commands. Oracle recommended no
  third implementation packet. Parent decision: keep the sync/guard model as the
  release-hardening baseline and route next to remaining Claude packaging risks.
- 2026-04-26: operator-guided follow-up tested seven per-rule raw stdout hook
  outputs. All seven rules were visible without preview/truncation in one local
  startup probe, but observed file order was non-sequential. This reopens a
  narrower hook-context candidate that needs critique before productization.
- 2026-04-26: operator accepted the per-rule hook route and small sleep ordering
  tradeoff. Compiled `packet:ralph-ticket-cldrel01-20260426T050555Z` for the third
  and final Fixer/Oracle cycle in this sequence.
- 2026-04-26: Fixer iteration 3 implemented per-rule `SessionStart` hook stdout,
  deleted the sync/guard/cleanup scripts, updated Claude install docs and fixture
  notes, and validated all seven rules visible in same-session startup context.
  Oracle accepted the implementation after wiki and fixture wording fixes. Ticket
  moved to `complete_pending_acceptance` for final risk disposition.
- 2026-04-28T18:47:27Z: Operator accepted the completed work and residual release
  risks, then closed the ticket.
