# Gemini Command Adaptation

## Transport Surface

- skills are copied into the Gemini-readable skill surface
- command wrappers are translated into `~/.gemini/commands/*.toml`
- rules are mirrored into a Loom-managed block in `~/.gemini/GEMINI.md`

## Expected Properties

- translated commands are adapter prompts, not protocol owners
- managed blocks are bracketed so uninstall can remove only Loom content
- rules remain the always-on doctrine
- skills remain the subsystem behavior source

## Common Wrong Behavior

- letting TOML command files define behavior not present in skills
- overwriting non-Loom user Gemini instructions
- installing optional utilities as if they were kernel skills
