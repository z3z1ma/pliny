# Claude Plugin Install

## Transport Surface

- `.claude-plugin/plugin.json` makes the repository root loadable as a Claude Code
  plugin during local development.
- `.claude-plugin/marketplace.json` makes the repository root a local Claude Code
  marketplace named `agent-loom` with one plugin named `loom`.
- the plugin exposes canonical `skills/` directly from the repository root.
- `.claude-plugin/plugin.json` declares `claude-hooks/hooks.json` as the Claude
  hook config so other harnesses do not auto-discover Claude hooks from root
  `hooks/`.
- `claude-hooks/hooks.json` registers one `SessionStart` hook group with matcher
  `startup|clear|compact`.
- that hook group has one command per `loom-bootstrap` reference; each command
  prints a `===== LOOM_BOOTSTRAP_REFERENCE <filename> =====` source marker and
  cats exactly one
  `${CLAUDE_PLUGIN_ROOT}/skills/loom-bootstrap/references/<filename>` file to stdout.
- the hook commands use small increasing sleep delays so numeric rule order is
  likely in practice, especially `01-core-identity.md` first, but Claude hook
  ordering is not guaranteed.

## Chosen Hook-Context Shape

Use the Claude plugin for discoverable skills and automatic same-session
bootstrap context from per-reference `SessionStart` hook stdout.

This avoids three wrong solutions:

- custom agents as a substitute for `loom-bootstrap`
- monolithic full-corpus hook output that Claude exposes only as a preview
- plugin settings that pretend to register arbitrary always-on instructions

## Expected Properties

- plugin validation passes with `claude plugin validate .`
- plugin skills remain `SKILL.md` directories from canonical `skills/`
- the `SessionStart` hook emits the ordered `loom-bootstrap` references as seven
  source-marked stdout outputs, one file per command
- same-session startup probes can see all seven bootstrap references without Claude's
  persisted-output preview/truncation behavior
- each current bootstrap reference remains below Claude's documented 10,000-character
  hook-output context cap
- ordering is treated as best effort; source markers, not strict order, are the
  stable attribution mechanism

## Limitations

- Claude plugin docs do not currently describe an install-time script hook or a
  plugin manifest field for arbitrary always-on instructions.
- Bootstrap context emits when a plugin-enabled session starts, not during the
  literal `claude plugin install` command.
- `${CLAUDE_PLUGIN_ROOT}` is the plugin installation/cache directory. Claude docs
  do not describe `${CLAUDE_PLUGIN_ROOT}/skills/loom-bootstrap/references` as a
  loaded instruction surface without the hook.
- This adapter depends on Claude adding `SessionStart` hook stdout to same-session
  context and on each per-reference output remaining below Claude's documented
  10,000-character cap.
- Claude runs matching hooks concurrently, so increasing sleep delays make numeric
  ordering likely but do not guarantee it.
- Runtime validation covers local `--plugin-dir` startup with project-only
  settings, no tools, and an empty temporary project. Installed marketplace mode,
  Windows shell behavior, and headless `clear`/`compact` runtime events remain
  unproven.
- Runtime installed marketplace skill invocation remains outside this fixture's
  bootstrap-loading proof.
- The marketplace currently uses source `./` for local/Git marketplace installs,
  which means the repository root is the plugin source. A release-packaged Claude
  plugin artifact should narrow this before broad distribution.

## Common Wrong Behavior

- calling a Claude plugin install complete when `loom-bootstrap` is not discoverable
- relying on a plugin custom agent's prompt as the Loom operating layer
- concatenating all Loom bootstrap references into one hook output and accepting a
  truncated preview as full context
- assuming source-marked per-rule hook output preserves strict numeric order
- copying dogfooding `.loom/` records into the plugin package

## Cleanup

Use Claude's plugin manager to disable or uninstall the plugin. The adapter's
bootstrap context is emitted from bundled plugin files at session start.
