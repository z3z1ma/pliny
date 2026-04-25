---
id: evidence:open-loom-smoke
kind: evidence
status: recorded
created_at: 2026-04-25T20:01:52Z
updated_at: 2026-04-25T22:07:56Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:6uy1rx20
  packet:
    - packet:ralph-ticket-6uy1rx20-20260425T195559Z
  research:
    - research:loom-install-distribution-methods
external_refs:
  opencode_source:
    - https://github.com/anomalyco/opencode/tree/v1.14.22
    - https://opencode.ai/docs/plugins/
    - https://opencode.ai/docs/config/
    - https://opencode.ai/docs/skills/
    - https://opencode.ai/docs/commands/
---

# Summary

Validation evidence for `open-loom`, the OpenCode plugin.

The current implementation uses OpenCode's server plugin `config(config)` hook to
mutate the resolved OpenCode config. It registers Loom's bundled surfaces as:

- ordered rule files -> `config.instructions`
- bundled skill root -> `config.skills.paths`
- bundled command wrappers -> `config.command`

# Procedure

1. Inspected OpenCode `v1.14.22` source from
   `https://github.com/anomalyco/opencode/tree/v1.14.22`.
2. Confirmed plugin module shape in `packages/opencode/src/plugin/shared.ts` and
   `packages/opencode/src/plugin/index.ts`: path plugins need `id`, server
   plugins default-export an object with `server()`, and loaded hooks receive a
   `config(config)` callback after plugin loading.
3. Confirmed OpenCode config/skills/commands integration points:
   `config.instructions`, `config.skills.paths`, and `config.command`.
4. Replaced the earlier chat-transform-only plugin shape with `config(config)`
   registration.
5. Ran `node open-loom.mjs --smoke`.
6. Ran an import-based config-hook check:

   ```bash
   node --input-type=module -e 'import plugin, { server, configureOpenCode, inspectLoomBundle } from "./open-loom.mjs"; if (plugin.id !== "open-loom" || typeof plugin.server !== "function") throw new Error("default plugin object invalid"); const hooks = await server({}, {}); const config = {}; hooks.config(config); const before = config.instructions.length; hooks.config(config); if (config.instructions.length !== before) throw new Error("instructions not deduped"); if (!config.instructions[0].endsWith("rules/01-core-identity.md")) throw new Error("first rule order wrong"); if (!config.instructions.at(-1).endsWith("rules/07-validation-and-honesty.md")) throw new Error("last rule order wrong"); if (!config.skills?.paths?.[0]?.endsWith("/skills")) throw new Error("skills path missing"); if (!config.command?.["loom-plan"]?.template?.includes("# /loom-plan")) throw new Error("loom-plan command missing"); const bundle = inspectLoomBundle(); console.log(JSON.stringify({defaultId: plugin.id, instructionCount: config.instructions.length, firstInstruction: config.instructions[0], lastInstruction: config.instructions.at(-1), skillCount: bundle.skills.items.length, commandCount: bundle.commands.items.length, hasLoomPlan: Boolean(config.command["loom-plan"])}, null, 2));'
   ```

7. Ran an optional-surface check showing missing `commands/` does not break
   registration.
8. Ran OpenCode runtime config validation in an isolated temporary project and
   temporary `HOME`:

   ```bash
   HOME="/var/folders/1b/6mg4g2fs2zx99h46b9j5r7mh0000gp/T/tmp.Vkb5kq4VtY/home" XDG_CONFIG_HOME="/var/folders/1b/6mg4g2fs2zx99h46b9j5r7mh0000gp/T/tmp.Vkb5kq4VtY/home/.config" OPENCODE_CONFIG_CONTENT='{"plugin":["file:///Users/alexanderbutler/code_projects/personal/agent-loom/open-loom.mjs"]}' opencode debug config
   ```

9. Ran OpenCode skill discovery validation in the same isolated environment:

   ```bash
   HOME="$tmp/home" XDG_CONFIG_HOME="$tmp/home/.config" OPENCODE_CONFIG_CONTENT='{"plugin":["file:///Users/alexanderbutler/code_projects/personal/agent-loom/open-loom.mjs"]}' opencode debug skill --print-logs --log-level INFO >/dev/null
   ```

10. Ran OpenCode package-root plugin validation with the local repository root as
    the plugin entry:

    ```bash
    OPENCODE_CONFIG_CONTENT='{"plugin":["file:///Users/alexanderbutler/code_projects/personal/agent-loom"]}' opencode debug config
    ```

11. Ran package validation after adding `engines.opencode`, `license`, and
    `examples/` to the package file list:

    ```bash
    npm run pack:check
    git diff --check
    ```

12. Ran final non-publishing npm checks:

    ```bash
    npm whoami
    npm publish --dry-run --access public
    npm view open-loom name version --json
    ```

13. Operator attempted real publication and npm rejected the request at the
    registry security gate because publish requires either a current 2FA OTP or a
    granular access token with bypass-2FA enabled.
14. Operator retried with the required npm security path and reported successful
    publication.
15. Verified published registry metadata:

    ```bash
    npm view open-loom name version dist-tags engines license --json
    ```

16. Validated the published package from repo-root `opencode.json` containing
    `"plugin": ["open-loom@0.1.0"]` by running OpenCode debug commands from the
    repository root.
17. Checked cold-cache behavior in an isolated temporary `HOME`. The first
    config-file run can report `NpmInstallFailedError` while leaving the package
    installed in OpenCode's cache; a second run in the same `HOME` resolves the
    cached package and exposes instructions, skills, and commands.

# Artifacts

`node open-loom.mjs --smoke` output:

```json
{
  "ok": true,
  "pluginId": "open-loom",
  "ruleCount": 7,
  "firstRule": "rules/01-core-identity.md",
  "lastRule": "rules/07-validation-and-honesty.md",
  "instructionCount": 7,
  "instructionsAreDeduped": true,
  "firstInstruction": "/Users/alexanderbutler/code_projects/personal/agent-loom/rules/01-core-identity.md",
  "lastInstruction": "/Users/alexanderbutler/code_projects/personal/agent-loom/rules/07-validation-and-honesty.md",
  "skillCount": 20,
  "skillPath": "/Users/alexanderbutler/code_projects/personal/agent-loom/skills",
  "commandCount": 19,
  "hasLoomPlanCommand": true,
  "rulesResult": "registered through config.instructions",
  "skillsResult": "registered through config.skills.paths",
  "commandsResult": "registered through config.command"
}
```

Import-based config-hook validation output:

```json
{
  "defaultId": "open-loom",
  "instructionCount": 7,
  "firstInstruction": "/Users/alexanderbutler/code_projects/personal/agent-loom/rules/01-core-identity.md",
  "lastInstruction": "/Users/alexanderbutler/code_projects/personal/agent-loom/rules/07-validation-and-honesty.md",
  "skillCount": 20,
  "commandCount": 19,
  "hasLoomPlan": true
}
```

Optional missing-commands validation output:

```json
{
  "instructions": 1,
  "skills": 1,
  "commands": 0
}
```

OpenCode `debug config` validation excerpt:

```json
{
  "plugin": [
    "file:///Users/alexanderbutler/code_projects/personal/agent-loom/open-loom.mjs"
  ],
  "command": {
    "loom-plan": {
      "template": "# /loom-plan\n\nYou are running **Loom Plan**...",
      "description": "Turn a raw request into governed Loom work by creating or updating the minimal correct outer-loop chain: initiative, research/spec when needed, plan, and ready tickets."
    }
  },
  "instructions": [
    "/Users/alexanderbutler/code_projects/personal/agent-loom/rules/01-core-identity.md",
    "/Users/alexanderbutler/code_projects/personal/agent-loom/rules/02-truth-and-authority.md",
    "/Users/alexanderbutler/code_projects/personal/agent-loom/rules/03-outer-loop.md",
    "/Users/alexanderbutler/code_projects/personal/agent-loom/rules/04-ralph-inner-loop.md",
    "/Users/alexanderbutler/code_projects/personal/agent-loom/rules/05-critique-and-wiki.md",
    "/Users/alexanderbutler/code_projects/personal/agent-loom/rules/06-filesystem-and-tooling.md",
    "/Users/alexanderbutler/code_projects/personal/agent-loom/rules/07-validation-and-honesty.md"
  ],
  "skills": {
    "paths": [
      "/Users/alexanderbutler/code_projects/personal/agent-loom/skills"
    ]
  }
}
```

OpenCode package-root `debug config` validation output:

```json
{
  "ok": true,
  "plugin": [
    "file:///Users/alexanderbutler/code_projects/personal/agent-loom"
  ],
  "instructionCount": 7,
  "skillPath": "/Users/alexanderbutler/code_projects/personal/agent-loom/skills",
  "commandCount": 19,
  "hasLoomPlan": true
}
```

OpenCode `debug skill --print-logs` validation excerpt from a clean temporary
project:

```text
INFO service=plugin path=file:///Users/alexanderbutler/code_projects/personal/agent-loom/open-loom.mjs loading plugin
INFO service=skill count=20 init
```

`npm run pack:check` result after package metadata fixes:

```text
open-loom@0.1.0 smoke:open-loom -> ok
npm pack --dry-run -> open-loom-0.1.0.tgz
tarball total files: 214
tarball includes examples/adapters/open-loom-install/README.md
```

`git diff --check`: no output.

Final npm pre-publish checks:

```text
npm whoami -> z3z1ma
npm publish --dry-run --access public -> + open-loom@0.1.0
npm view open-loom name version --json -> E404 Not Found
```

Real publish attempt result:

```text
npm notice Publishing to https://registry.npmjs.org/ with tag latest and public access
npm error code E403
npm error 403 403 Forbidden - PUT https://registry.npmjs.org/open-loom - Two-factor authentication or granular access token with bypass 2fa enabled is required to publish packages.
npm error A complete log of this run can be found in: /Users/alexanderbutler/.npm/_logs/2026-04-25T21_49_54_840Z-debug-0.log
```

Published registry metadata:

```json
{
  "name": "open-loom",
  "version": "0.1.0",
  "dist-tags": {
    "latest": "0.1.0"
  },
  "engines": {
    "opencode": ">=1.14.22 <2"
  },
  "license": "UNLICENSED"
}
```

Repo-root `opencode.json` used for package validation:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["open-loom@0.1.0"]
}
```

Observed OpenCode package-cache registration from normal repo-root config-file
loading:

```text
plugin origin: open-loom@0.1.0 from /Users/alexanderbutler/code_projects/personal/agent-loom/opencode.json
skills path: /Users/alexanderbutler/.cache/opencode/packages/open-loom@0.1.0/node_modules/open-loom/skills
commands include: loom-plan
skill locations include: /Users/alexanderbutler/.cache/opencode/packages/open-loom@0.1.0/node_modules/open-loom/skills/loom-tickets/SKILL.md
```

Isolated cold-cache first/second run check:

```json
{
  "firstFailed": true,
  "firstHasLoomInstructions": false,
  "secondFailed": false,
  "secondHasLoomInstructions": true,
  "secondHasSkillsPath": true,
  "secondHasLoomPlan": true
}
```

# Supports Claims

- `ticket:6uy1rx20` bundled file-read acceptance: `open-loom` reads ordered rule
  files from the package/clone layout.
- `ticket:6uy1rx20` ordered rule acceptance: `open-loom` registers each ordered
  rule file as an absolute `config.instructions` entry.
- `ticket:6uy1rx20` skill exposure acceptance: `open-loom` registers the bundled
  `skills/` root through `config.skills.paths`, and `opencode debug skill` finds
  Loom skills from that path.
- `ticket:6uy1rx20` command exposure acceptance: `open-loom` converts bundled
  command Markdown wrappers into `config.command` entries; `opencode debug config`
  shows `loom-plan` and other command entries.
- `ticket:6uy1rx20` local file/path plugin acceptance: the plugin can be loaded
  through a local `file://.../open-loom.mjs` entry.
- `ticket:6uy1rx20` package-root local plugin acceptance: OpenCode resolves the
  local package root through `package.json` and applies the same instructions,
  skill path, and command config.
- `ticket:6uy1rx20` package-readiness acceptance: `package.json` now declares
  `engines.opencode: >=1.14.22 <2`, `license: UNLICENSED`, and includes
  `examples/` in the npm file list; `npm run pack:check` succeeds.
- `ticket:6uy1rx20` npm pre-publish acceptance: npm authentication is present as
  user `z3z1ma`, `npm publish --dry-run --access public` succeeds, and
  `open-loom` remains unpublished immediately before real publication.
- `ticket:6uy1rx20` publish blocker: the real publish attempt reached npm but was
  rejected by the registry because the publish request lacked a valid 2FA OTP or
  bypass-2FA granular token.
- `ticket:6uy1rx20` npm publication acceptance: `open-loom@0.1.0` is published on
  npm with `latest` pointing at `0.1.0`.
- `ticket:6uy1rx20` normal package config acceptance: a repo-root `opencode.json`
  with `plugin: ["open-loom@0.1.0"]` loads the published package from OpenCode's
  package cache and exposes the package skills and command wrappers.

# Challenges Claims

- Challenges the earlier assumption that `experimental.chat.system.transform` is
  the best OpenCode route for Loom rules. `config.instructions` is the supported
  OpenCode config surface for instruction files and now carries the rule files.
- Challenges an overbroad claim that every cold-cache OpenCode npm-plugin path is
  clean on first execution. In isolated `HOME` validation, the first config-file
  run can log `NpmInstallFailedError`; the second run resolves the cached package
  and exposes Loom surfaces.

# Environment

Commit: `b9bdc32c15aa166194a202a221c524cef7c81049`

Branch: `main`

Runtime: Node `v22.22.1`; OpenCode CLI `1.14.22`

OS: macOS / Darwin

# Validity

Valid for: OpenCode `1.14.22` plugin config-hook behavior, package/clone layout,
local package-root plugin resolution, resolved config, command registration
through `config.command`, and skill discovery through `config.skills.paths`.

Recheck when: OpenCode plugin APIs change, package publication changes the bundle
layout, Loom command frontmatter changes, or `open-loom` is updated.

# Limitations

This evidence does not make a paid model request or open an interactive TUI
session. It validates OpenCode's resolved config and skill discovery paths using
OpenCode debug commands, plus source inspection for how those config surfaces are
consumed.

Npm registry publication is validated. A cold-cache first-run OpenCode npm-plugin
install quirk remains: OpenCode `1.14.22` can log `NpmInstallFailedError` on the
first config-file run while still caching the package; a second run in the same
OpenCode cache succeeds.

# Result

`open-loom@0.1.0` is published and works through a normal repo-root OpenCode
config file after OpenCode resolves the package from its cache. The remaining
risk is OpenCode's cold-cache first-run npm-plugin install behavior.

# Related Records

- `ticket:6uy1rx20`
- `packet:ralph-ticket-6uy1rx20-20260425T195559Z`
- `research:loom-install-distribution-methods`
