---
id: evidence:cursor-plugin-install-validation
kind: evidence
status: recorded
created_at: 2026-04-26T07:53:38Z
updated_at: 2026-04-26T07:53:38Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:1c0lb4uu
  decision:
    - decision:0006
external_refs:
  cursor_docs:
    - https://cursor.com/docs/plugins#creating-plugins
    - https://cursor.com/docs/reference/plugins
  superpowers:
    - https://github.com/obra/superpowers/blob/main/.cursor-plugin/plugin.json
---

# Summary

Validation evidence for adding a skills-only Cursor plugin manifest and native
install command documentation.

# Procedure

- Checked Cursor plugin docs for `.cursor-plugin/plugin.json`, `skills/` plugin
  structure, `~/.cursor/plugins/local/<plugin-name>` local install/reload flow,
  and `hooks` manifest field support.
- Checked Superpowers' Cursor manifest shape at
  `obra/superpowers/.cursor-plugin/plugin.json`.
- Added `.cursor-plugin/plugin.json` with `skills: "./skills/"` and inline empty
  `hooks: {}` so Cursor does not auto-discover the repository's Claude-specific
  `hooks/hooks.json`.
- Validated present JSON manifests with `python3 -m json.tool`.
- Ran `node open-loom.mjs --smoke`.
- Ran `claude plugin validate /Users/alexanderbutler/code_projects/personal/agent-loom`.
- Ran `npm pack --dry-run`.
- Ran `git diff --check`.

# Observed Results

- JSON validation passed.
- OpenCode smoke reported seven bootstrap references and 21 skills.
- Claude plugin validation passed.
- npm dry run still packages `open-loom.mjs`, public docs, and `skills/` for the
  OpenCode npm package; it does not include removed fallback surfaces.
- Diff whitespace check passed.

# Supports Claims

- `ticket:1c0lb4uu` claim: Cursor has a native plugin manifest exposing `skills/`.
- `ticket:1c0lb4uu` claim: Cursor manifest avoids loading Claude-specific root
  hooks.
- `ticket:1c0lb4uu` claim: install docs include concise native install or
  registration commands with Codex/Cursor caveats.

# Challenges Claims

- None.

# Limitations

- Cursor runtime plugin loading was not executed locally.
- Cursor Marketplace listing for `agent-loom` does not exist yet; `/add-plugin
  agent-loom` is documented as the future post-listing path.
- Codex installed Git-backed plugin skill discovery remains unvalidated and owned
  by `ticket:lx9nnztk`.
