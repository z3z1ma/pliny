---
id: wiki:harness-adapter-package-pattern
kind: wiki
page_type: workflow
status: active
created_at: 2026-04-25T22:14:57Z
updated_at: 2026-04-26T05:15:49Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:loom-install-experience
  plan:
    - plan:install-experience-harness-adapters
  spec:
    - spec:opencode-plugin-install-contract
  ticket:
    - ticket:6uy1rx20
    - ticket:q7h1d05q
    - ticket:cldrel01
  evidence:
    - evidence:open-loom-smoke
    - evidence:claude-plugin-hybrid
    - evidence:claude-sessionstart-stdout-context
  critique:
    - critique:open-loom-config-hook-review
    - critique:claude-plugin-integration-review
    - critique:claude-hook-context-simplification-review
    - critique:claude-per-rule-hook-implementation-review
  research:
    - research:loom-install-distribution-methods
---

# Summary

Adapter packages are harness-native packaging surfaces that make Loom easier to
install without becoming owners of Loom semantics.

`open-loom@0.1.0` is the first accepted example in this repository: an OpenCode
npm plugin that exposes bundled Loom rules, skills, and optional command wrappers
through OpenCode config surfaces.

Claude Code is the first accepted hybrid example: a Claude plugin exposes skills
and command wrappers while a plugin `SessionStart` hook emits Loom's canonical
rules as same-session, source-marked per-rule context.

# When To Use It

Use this pattern when a harness has a first-class package, plugin, or extension
mechanism that can expose Loom's required surfaces more cleanly than direct
user-config mutation.

Do not use this pattern when the harness package system cannot express ordered
always-on rules, skill discovery, or command wrappers without a separate fallback.
In that case, use a hybrid install and document the split.

Use the hybrid form when the harness package can carry some Loom surfaces but not
all of them. The package should still improve installation, but the missing
surface must be routed through a documented and evidenced harness-owned mechanism,
not hidden in an unvalidated hook or custom agent prompt.

# Inputs

- canonical top-level `rules/`, `skills/`, and optional `commands/`
- the harness's official package/plugin/extension docs
- a ticket that owns one bounded harness install slice
- evidence for package structure, install behavior, and surface discovery
- critique for operator clarity and release-packaging risk

# Procedure

1. Start from the canonical Loom surfaces. Do not copy dogfooding `.loom/` or
   `.opencode/` state into the package.
2. Choose the smallest harness-native registration path that exposes rules,
   skills, and commands.
3. Keep generated or emitted adapter content derivative and source-marked.
4. Declare compatibility metadata when the package manager or harness supports it.
5. Validate package layout before publication or release.
6. Validate harness loading through the harness's own debug, install, link, or
   discovery commands when available.
7. Record install caveats as evidence and either accept them explicitly or create
   follow-up tickets.
8. Update install docs only after evidence supports the recommendation.

# Hybrid Adapter Procedure

Use this procedure when a harness plugin/package cannot own every Loom surface.

1. Name which Loom surfaces the package can natively expose and which it cannot.
2. Route the missing surface to a documented static harness surface.
3. Keep generated outputs derivative from canonical `rules/`, `skills/`, and
   optional `commands/`.
4. Prefer one generated ordered rule file when the harness supports documented
   static rule loading but does not document ordering across multiple rule files.
5. Use hooks as the knowledge channel only when the harness docs and runtime
   evidence prove complete same-session context delivery and the ticket accepts
   the tradeoff.
6. Fail closed when a bootstrap sync changes instructions after the session has
   already loaded context; avoid bootstrap sync entirely when same-session hook
   context is validated.
7. Validate both manifest shape and real install/load behavior; schema validation
   alone is not enough.
8. Keep disable/uninstall cleanup explicit when the harness provides no lifecycle
   hook.

# Claude Hybrid Example

The accepted Claude adapter uses this split:

- `.claude-plugin/plugin.json` exposes canonical `skills/` and optional
  `commands/`.
- `.claude-plugin/marketplace.json` exposes local marketplace `agent-loom` with
  plugin `loom` sourced from `./` for local/prototype installs.
- Claude auto-loads the standard plugin `hooks/hooks.json`; the manifest should
  not duplicate that standard hook path.
- `SessionStart` uses matcher `startup|clear|compact` and emits one
  source-marked stdout block per canonical top-level rule file.
- Each rule output stays below Claude's documented 10,000-character hook-output
  context cap.
- Small increasing sleeps make `01-core-identity.md` appear first in observed
  startup probes, but strict rule ordering is not guaranteed; source markers are
  the stable attribution mechanism.
- Disabling or uninstalling the plugin follows Claude's plugin manager UX because
  the active rule delivery path is plugin hook context emitted at session start.

The important accepted limitation is ordering: Claude runs matching hooks
concurrently, so per-rule outputs are source-marked and only best-effort ordered.
Local startup probes saw all seven rules without preview/truncation and saw
`01-core-identity.md` first, but did not prove strict numeric order after that.

Validation review: `evidence:claude-sessionstart-stdout-context` showed that
monolithic full-corpus hook context was previewed/truncated, plugin-root static
context did not load under local `--plugin-dir`, and arbitrary 26-command chunking
was more complex than the per-rule design.

# Outputs

- package or adapter entrypoint files
- package metadata and compatibility range
- install docs and adapter fixture notes
- evidence record for package contents and harness loading
- critique record or disposition for release-packaging risk
- ticket acceptance decision with residual risks or linked follow-ups

# Failure Modes

- treating package files as the new canonical Loom source
- recommending a plugin path before the harness actually loads the package
- hiding a required fallback step behind plugin-first marketing
- publishing docs that point at files omitted from the package
- claiming cold-cache or first-run behavior works when only warm-cache behavior
  was observed
- overgeneralizing one harness's plugin behavior to other harnesses
- assuming plugin schema validation proves installed plugin behavior
- declaring a standard auto-loaded hook file in the plugin manifest and causing a
  duplicate hook-load error
- treating `${CLAUDE_PLUGIN_ROOT}` as the user's or project's `.claude` directory
- selecting project-local install scope because `.claude/` exists instead of
  because the plugin is explicitly enabled for that project
- relying on hook stdout or a custom agent prompt as the always-on rule layer
  without runtime evidence and explicit ticket acceptance
- replacing a documented static rule sync with many chunked hook-context commands
  just because a local probe worked once
- accepting source-marked per-rule hook output as strictly ordered when the
  harness only provides best-effort ordering

# Sources

- `spec:opencode-plugin-install-contract`
- `ticket:6uy1rx20`
- `ticket:us1brnsv`
- `ticket:q7h1d05q`
- `ticket:cldrel01`
- `evidence:open-loom-smoke`
- `evidence:claude-plugin-hybrid`
- `evidence:claude-sessionstart-stdout-context`
- `critique:open-loom-config-hook-review`
- `critique:claude-plugin-integration-review`
- `critique:claude-hook-context-simplification-review`
- `research:loom-install-distribution-methods`
- `plan:install-experience-harness-adapters`
- `initiative:loom-install-experience`

# Related Pages

Future Cursor, Gemini, and Codex package work should link here only after their
harness-specific evidence is recorded. Claude and OpenCode are accepted examples
with linked ticket, evidence, and critique records.
