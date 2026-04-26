# Claude Plugin Install

## Transport Surface

- `.claude-plugin/plugin.json` makes the repository root loadable as a Claude Code
  plugin during local development.
- `.claude-plugin/marketplace.json` makes the repository root a local Claude Code
  marketplace named `agent-loom` with one plugin named `loom`.
- the plugin exposes canonical `skills/` and optional `commands/` directly from
  the repository root.
- Claude auto-loads the standard plugin `hooks/hooks.json`; the plugin manifest
  does not repeat that hook path.
- `hooks/hooks.json` registers one `SessionStart` hook group with matcher
  `startup|clear|compact`.
- that hook group has one command per canonical top-level rule file; each command
  prints a `===== LOOM_RULE_FILE <filename> =====` source marker and cats exactly
  one `${CLAUDE_PLUGIN_ROOT}/rules/<filename>` file to stdout.
- the hook commands use small increasing sleep delays so numeric rule order is
  likely in practice, especially `01-core-identity.md` first, but Claude hook
  ordering is not guaranteed.

## Chosen Hook-Context Shape

Use the Claude plugin for discoverable skills, command wrappers, and automatic
same-session rule context from per-rule `SessionStart` hook stdout.

This avoids three wrong solutions:

- custom agents as a substitute for Loom's rule corpus
- monolithic full-corpus hook output that Claude exposes only as a preview
- plugin settings that pretend to register arbitrary always-on instructions

## Expected Properties

- plugin validation passes with `claude plugin validate .`
- plugin skills remain `SKILL.md` directories from canonical `skills/`
- command wrappers remain optional invocation surfaces from canonical `commands/`
- the `SessionStart` hook emits the canonical top-level `rules/*.md` files as
  seven source-marked stdout outputs, one file per command
- same-session startup probes can see all seven rule files without Claude's
  persisted-output preview/truncation behavior
- each current rule file remains below Claude's documented 10,000-character
  hook-output context cap
- ordering is treated as best effort; source markers, not strict order, are the
  stable attribution mechanism

## Limitations

- Claude plugin docs do not currently describe an install-time script hook or a
  plugin manifest field for arbitrary always-on rules.
- Rule context emits when a plugin-enabled session starts, not during the literal
  `claude plugin install` command.
- `${CLAUDE_PLUGIN_ROOT}` is the plugin installation/cache directory. Claude docs
  do not describe `${CLAUDE_PLUGIN_ROOT}/rules` as a loaded instruction surface.
- This adapter depends on Claude adding `SessionStart` hook stdout to same-session
  context and on each per-rule output remaining below Claude's documented
  10,000-character cap.
- Claude runs matching hooks concurrently, so increasing sleep delays make numeric
  ordering likely but do not guarantee it.
- Runtime validation covers local `--plugin-dir` startup with project-only
  settings, no tools, and an empty temporary project. Installed marketplace mode,
  Windows shell behavior, and headless `clear`/`compact` runtime events remain
  unproven.
- Runtime skill and command-wrapper invocation remains outside this fixture's
  rule-loading proof.
- The marketplace currently uses source `./` for local/Git marketplace installs,
  which means the repository root is the plugin source. A release-packaged Claude
  plugin artifact should narrow this before broad distribution.

## Common Wrong Behavior

- calling a Claude plugin install complete when Loom rules were not installed
- relying on a plugin custom agent's prompt as the Loom operating layer
- concatenating all Loom rules into one hook output and accepting a truncated
  preview as full context
- assuming source-marked per-rule hook output preserves strict numeric order
- copying dogfooding `.loom/` records into the plugin package

## Cleanup

Use Claude's plugin manager to disable or uninstall the plugin. The adapter's
rule context is emitted from bundled plugin files at session start.
