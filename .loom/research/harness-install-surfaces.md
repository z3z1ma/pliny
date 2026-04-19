---
id: research:harness-install-surfaces
kind: research
status: active
created_at: 2026-04-18T03:03:47Z
updated_at: 2026-04-19T21:59:26Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:ffg8elkb
  research:
    - research:codex-command-skill-installation
---

# Question

What user-level install surfaces do OpenCode, Claude Code, Codex, and Gemini CLI
expect for always-on instructions, skills, and reusable commands, and what
translation is required to install Loom's shipped `rules/`, `skills/`, and
`commands/` directories into those harnesses?

# Why This Matters

The repository wants a simple global install path from the canonical shipped
bundle, not from dogfooding `.loom/` or `.opencode/` state.

If the harness surfaces differ, the installer needs to map Loom truthfully
instead of pretending every harness uses the same directory structure or file
format.

# Scope

- inspect only the canonical product surfaces: top-level `rules/`, `skills/`,
  and optional `commands/`
- identify user-level install paths for OpenCode, Claude Code, Codex, and
  Gemini CLI
- note where a harness supports direct copies versus where translation is
  required
- inspect local home-directory state only to confirm currently used config
  locations

# Method

Read official harness docs for user-level config, instruction, skill, and
command locations.

Cross-check those findings against the local filesystem under
`~/.config/opencode/`, `~/.claude/`, `~/.codex/`, and `~/.gemini/`.

# Sources

- OpenCode config docs: `https://opencode.ai/docs/en/config/`
- Claude Code `.claude` directory docs:
  `https://code.claude.com/docs/en/claude-directory.md`
- Codex AGENTS docs:
  `https://developers.openai.com/codex/guides/agents-md`
- Codex skills docs: `https://developers.openai.com/codex/skills`
- Gemini CLI configuration docs:
  `https://google-gemini.github.io/gemini-cli/docs/get-started/configuration.html`
- Gemini CLI custom commands docs:
  `https://google-gemini.github.io/gemini-cli/docs/cli/custom-commands.html`
- Gemini CLI command reference snippets documenting `~/.gemini/agents` and
  `~/.gemini/commands`
- local files: `~/.claude/settings.json`, `~/.codex/config.toml`,
  `~/.gemini/settings.json`, `~/.config/opencode/`

# Evidence

- OpenCode user config lives in `~/.config/opencode/`; global commands and
  skills live in plural subdirectories there, while always-on rules are best
  wired through `~/.config/opencode/opencode.json` via the `instructions` array.
- Claude Code reads global instructions and extensions from `~/.claude/`,
  including `~/.claude/rules/`, `~/.claude/skills/`, and
  `~/.claude/commands/`.
- Codex uses a split global surface:
  `~/.codex/AGENTS.md` for always-on instructions,
  `$HOME/.agents/skills` for global skills, and skills as the current reusable
  workflow surface.
- Codex skills support explicit `$skill` invocation and can disable implicit
  invocation with `agents/openai.yaml` policy `allow_implicit_invocation: false`.
- Codex's `~/.codex/rules/` is a shell-exec policy surface, not an equivalent
  home for Loom Markdown rules, so Loom rules should not be copied there.
- Gemini CLI uses `~/.gemini/settings.json` plus hierarchical context from
  `~/.gemini/GEMINI.md`; custom commands live in `~/.gemini/commands/` and use
  TOML, not Markdown.
- Gemini CLI supports user-level subagents in `~/.gemini/agents/` and supports
  skill discovery with `.agents/skills` / `~/.agents/skills` as the generic
  cross-tool skill location.
- The local machine already has user config roots at `~/.claude/`, `~/.codex/`,
  `~/.gemini/`, and `~/.config/opencode/`, matching the documented locations.

# Conclusions

- Claude Code can accept a near-direct copy of Loom's canonical bundle into
  matching global directories.
- OpenCode can also accept direct copies for `skills/` and `commands/`, but its
  always-on rules need a small config update so the installed rule files are
  loaded.
- Codex and Gemini CLI both need translation for at least one surface:
  Codex needs Loom rules aggregated into `~/.codex/AGENTS.md` and Loom commands
  adapted into explicit-only skill directories; Gemini commands need
  Markdown-to-TOML conversion.
- `~/.agents/skills` is the most interoperable global skill destination for
  both Codex and Gemini CLI.

# Recommendations

- Add a Makefile with `install` and `uninstall` targets driven by
  `harness=<name>`.
- Support `opencode`, `claude`, `codex`, `gemini`, and `all` harness values.
- Keep direct directory copies where the harness supports them.
- Use small inline Python only for the format-translation cases:
  updating OpenCode `opencode.json`, aggregating Codex `AGENTS.md`, adapting
  Codex command Markdown files into skills, and converting Gemini command
  Markdown files to TOML.
- Keep installs namespaced under a Loom-owned marker or header where a single
  file must be generated so uninstall can cleanly reverse only Loom-managed
  content.

# Open Questions

- Whether Gemini CLI should receive Loom commands as top-level `/name` commands
  or under a namespaced subtree such as `/loom:name` for collision safety.
- Whether future Codex UI behavior should show the generated command adapter
  skill name or the original slash-command-style display name more prominently.

# Linked Work

- `ticket:ffg8elkb`
