# Codex Command Adaptation

## Transport Surface

- rules are mirrored into a Loom-managed block in `~/.codex/AGENTS.md`
- protocol skills live under `~/.agents/skills/`
- command wrappers become explicit-only command adapter skills under
  `~/.agents/skills/loom-command-*`
- generated command adapter skills disable implicit invocation through
  `agents/openai.yaml`

## Expected Properties

- deleting generated command adapters removes invocation convenience only
- protocol behavior still exists in `rules/` and `skills/`
- Codex shell policy rules are not confused with Loom Markdown rules
- uninstall removes only Loom-managed generated surfaces

## Common Wrong Behavior

- treating `~/.codex/rules/` as the Markdown rule surface
- allowing command adapter skills to trigger implicitly
- making command adapter prompts more canonical than source skills
