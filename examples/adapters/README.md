# Adapter Fixtures

These fixtures describe expected adapter surfaces for common harnesses.

They are not runtime tests and not protocol truth. They exist to make native
adapter drift easier to review.

Adapter fixtures should check:

- `loom-bootstrap` is discoverable, and its references are visible where the
  harness reads always-on instructions when the adapter preloads context
- skills are discoverable without making every skill always-on
- generated native adapter files remain thin pointers to `skills/`
- disable or uninstall follows the harness-native plugin or skill-package UX

Protocol semantics still live in `skills/`, `loom-bootstrap` references,
templates, and owner records.

Current fixtures:

- `claude-plugin-install/` - Claude native plugin with optional bootstrap preload
- `codex-plugin-install/` - Codex native plugin / marketplace shape
- `open-loom-install/` - OpenCode npm/local plugin package behavior
- `cursor-install/` - Cursor native skill-package target notes
- `gemini-extension-install/` - Gemini CLI native extension with bootstrap preload
