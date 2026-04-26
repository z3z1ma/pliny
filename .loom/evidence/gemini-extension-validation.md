---
id: evidence:gemini-extension-validation
kind: evidence
status: recorded
created_at: 2026-04-26T08:10:04Z
updated_at: 2026-04-26T08:26:59Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:7ex8w32y
  decision:
    - decision:0006
external_refs:
  gemini_docs:
    - https://geminicli.com/docs/extensions/
    - https://geminicli.com/docs/extensions/writing-extensions/
    - https://geminicli.com/docs/cli/gemini-md/
---

# Summary

Validation evidence for adding a native Gemini CLI extension surface for Loom.

# Procedure

- Checked Gemini CLI extension docs for `gemini-extension.json`, `contextFileName`,
  extension-bundled Agent Skills under `skills/`, and `gemini extensions install`.
- Checked Gemini context docs for `@file.md` imports with relative paths.
- Added `gemini-extension.json` with:
  - `contextFileName: "gemini-bootstrap.md"`
- Added `gemini-bootstrap.md`, which imports the seven ordered
  `skills/loom-bootstrap/references/*.md` files.
- Moved Claude hooks under `claude-hooks/`, leaving no root `hooks/hooks.json` for
  Gemini to auto-discover.
- Ran `python3 -m json.tool` over Gemini and other package manifests.
- Ran `gemini extensions validate /Users/alexanderbutler/code_projects/personal/agent-loom`.
- Ran `HOME=<temp> gemini extensions link ... --consent` followed by
  `HOME=<temp> gemini extensions list`.
- Ran `HOME=<temp> gemini extensions disable agent-loom` followed by
  `HOME=<temp> gemini extensions list`.
- Ran `node open-loom.mjs --smoke`.
- Ran `claude plugin validate /Users/alexanderbutler/code_projects/personal/agent-loom`.
- Ran `git diff --check`.

# Observed Results

- JSON validation passed.
- Gemini extension validation returned:

```text
Extension /Users/alexanderbutler/code_projects/personal/agent-loom has been successfully validated.
```

- Temp-home Gemini link/list showed extension `agent-loom (0.1.1)` enabled, with
  context file `/Users/alexanderbutler/code_projects/personal/agent-loom/gemini-bootstrap.md`
  and all 21 Loom skills, including `loom-bootstrap`.
- Temp-home Gemini disable/list returned `Extension "agent-loom" successfully
  disabled for scope "User"` and list showed `Enabled (User): false`.
- The initial temp-home link preview before Claude hooks were moved out of root
  `hooks/` warned that the extension contained hooks. After the Claude hook config
  moved to `claude-hooks/hooks.json`, the link/list output did not show that hook
  warning.
- OpenCode smoke reported seven bootstrap references and 21 skills.
- Claude plugin validation passed.
- Diff whitespace check passed.

# Supports Claims

- `ticket:7ex8w32y` claim: Gemini extension can expose canonical Loom skills.
- `ticket:7ex8w32y` claim: Gemini extension can preload ordered bootstrap
  references via `contextFileName` and `@file.md` imports.
- `ticket:7ex8w32y` claim: Gemini extension avoids auto-loading Claude-specific
  hooks from root `hooks/`.

# Challenges Claims

- None.

# Limitations

- Runtime model-context expansion of the `@./skills/...` imports was not directly
  inspected; validation proves extension structure and link/list discovery, not
  full model prompt contents.
- Temp-home `gemini extensions link` emitted a project-registry warning when using
  a synthetic empty HOME, but still linked and listed the extension successfully.
- Remote `gemini extensions install https://github.com/z3z1ma/agent-loom` was not
  run because it depends on pushed repository state.
