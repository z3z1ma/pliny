# Gemini CLI Extension Install

## Transport Surface

- `gemini-extension.json` is the Gemini CLI extension manifest at the repository
  root.
- The extension exposes canonical `skills/` through Gemini CLI's extension-bundled
  Agent Skills discovery.
- `contextFileName` points at `gemini-bootstrap.md`, which imports the ordered
  `skills/loom-bootstrap/references/*.md` files with Gemini's native `@file.md`
  context import syntax.
- Claude-specific hooks live under `claude-hooks/`, so Gemini does not
  auto-discover them from root `hooks/`.

## Expected Properties

- `loom-bootstrap` remains a canonical skill under `skills/`.
- Bootstrap preload is an extension-native convenience, not a second doctrine
  source.
- The context file imports canonical bootstrap references instead of duplicating
  their content.
- Bootstrap preload uses `contextFileName`, not hooks.
- Disable, enable, update, and uninstall should use `gemini extensions ...`
  commands.

## Common Wrong Behavior

- copying bootstrap references into `~/.gemini/GEMINI.md` as the product install
  path
- generating Gemini command wrappers from removed top-level `commands/`
- treating `gemini-bootstrap.md` as more canonical than `skills/loom-bootstrap`
