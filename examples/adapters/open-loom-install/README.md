# open-loom Install

## Transport Surface

- `open-loom.mjs` is the OpenCode plugin entrypoint at the package root.
- The plugin reads top-level `rules/*.md` from the package or cloned repository using module-relative file reads.
- It uses OpenCode's `config(config)` plugin hook to add ordered rule files to `config.instructions`.
- It adds the bundled skill root to `config.skills.paths`.
- It registers bundled command wrappers through `config.command`.

## Expected Plugin Entries

Normal npm-package users should use the package entry after `open-loom` is published:

```json
{
  "plugin": ["open-loom"]
}
```

`open-loom` requires OpenCode `>=1.14.22 <2`.

Cloned-repository users should use a local file/path entry that points at the plugin file:

```json
{
  "plugin": ["file:///absolute/path/to/agent-loom/open-loom.mjs"]
}
```

Relative or absolute local path specs may also be usable when they are resolved by OpenCode from the expected config location, but the `file://` form is the most explicit local clone recommendation.

Git URL plugin specs are not recommended. Source-level handling may mention git-like specs, but current operator validation found Git URL plugin installs unsupported in practice; use npm publication or a local file/path entry instead.

OpenCode `1.14.22` cold-cache npm plugin loading can log `NpmInstallFailedError` on the first config-file run while still caching the package. A second run in the same OpenCode cache resolved `open-loom@0.1.0` and exposed the Loom surfaces in validation.

## Surface Disposition

- Rules: registered through `config.instructions` with one absolute path per ordered rule file.
- Skills: registered through `config.skills.paths` using the bundled `skills/` root.
- Commands: registered through `config.command` using the bundled Markdown wrappers as templates.

## Structural Smoke Check

Run from the repository root:

```bash
node open-loom.mjs --smoke
```

The smoke output should list ordered rule files from `rules/`, confirm the resolved instruction paths, and report skill/command registration counts. `opencode debug config` and `opencode debug skill` can validate OpenCode's resolved config and skill discovery without making a model request.

## Common Wrong Behavior

- treating generated plugin output as canonical Loom semantics
- recommending Git URL plugin specs as the normal install path
- publishing before `opencode debug config`, `opencode debug skill`, and package dry-run checks pass
