# AGENTS.md

## What This Repo Is

This repository develops a distributable product. The product is the entire `src/` directory. End users copy the contents of `src/` into their own projects (typically into `.opencode/` or a similar harness-specific location). The product is Markdown-first with bundled Python helpers -- not a normal app, service, or library.

There is no `package.json`, `pyproject.toml`, `Makefile`, test runner, or CI pipeline.

## Agent and Script Boundary

The agent is the primary operator in a Loom workspace. Scripts are narrow mechanical utilities that serve the agent at specific structural points.

**Scripts are justified when they provide determinism the agent cannot reliably provide on its own:**

- structural record validation (schema, required sections, status invariants)
- frontmatter parsing, creation, and scaffolding
- cross-record link integrity checking
- workspace diagnostics and scope resolution
- record listing and frontmatter-aware querying

**Everything else is agent work with standard tools:**

- reading and understanding records
- populating record content
- searching and navigating the workspace
- editing records and artifacts
- orchestrating workflow steps (Ralph execution, critique, docs follow-through)
- reconciling outcomes into the ticket ledger
- deciding what to do next

Workflow steps like Ralph execution, critique, and docs work are agent actions -- the agent launches a fresh context with a compiled packet, not a custom orchestration script. Do not wrap agent work in scripts. Do not add a script for something the agent already handles well with its own capabilities and standard tools. When in doubt, the agent does the work directly and invokes a script only for the mechanical structural check afterward.

## Repo Structure

There are two clearly separated concerns: **product source** and **build tooling**.

### Product source: `src/`

Everything a user receives lives here. Three subdirectories:

- `src/rules/` -- always-on doctrine files (Markdown + `appendices/`)
- `src/skills/` -- 16 self-contained skill directories, each with `SKILL.md`, `references/`, and `scripts/`
- `src/commands/` -- slash-command definitions (Markdown files that define prompt-based commands)

**Isolation rule**: nothing inside `src/` may reference anything outside `src/`. No `build/` paths, no `.loom/` paths, no repo-root paths. When `src/` is copied to a user's machine, only `src/`-internal paths exist. Skills reference their own scripts as `scripts/...` and their own docs as `references/...`.

### Build tooling: `build/`

Maintainer-only assembly and shared code:

- `build/assemble-skills.py` -- copies shared scripts into each skill's `scripts/` directory
- `build/shared/_loom_lib/` -- shared Python library (`core.py`, `records.py`, `cli.py`, `memory.py`)
- `build/shared/scripts/` -- shared CLI scripts distributed to skills by the assembly step

### Dogfooding artifacts: `.opencode/` and `.loom/`

This repo uses its own product. `.opencode/rules`, `.opencode/skills`, and `.opencode/commands` are symlinks pointing back into `src/`, so the development environment consumes the product in the same way an end user would. `.loom/` contains Loom records (tickets, specs, plans, etc.) created by using the product on this repo.

Neither `.opencode/` nor `.loom/` is a maintained source surface. They are consumption artifacts. Do not treat them as source of truth for how the product works -- look at `src/` and `build/` instead.

## Commands

### Assembly (the only routine build command)

```bash
python3 build/assemble-skills.py
```

Copies shared scripts from `build/shared/scripts/` and `build/shared/_loom_lib/` into each skill's `scripts/` directory. Validates SKILL.md frontmatter. Produces `build/manifest.json`.

### Linting

```bash
uvx ruff check build/ src/            # lint all Python
uvx ruff check path/to/file.py        # lint a single file
uvx ruff format --check build/ src/   # verify formatting (all files currently pass)
uvx ruff format path/to/file.py       # auto-format a single file
```

No ruff config file exists; default settings apply.
Known suppressions: `# noqa: E402` on imports after `sys.path.insert` in CLI scripts.

### Validation scripts (run from workspace root)

```bash
python3 build/shared/scripts/validate_record.py                     # validate all Loom records
python3 build/shared/scripts/validate_record.py .loom/tickets/x.md  # validate one record
python3 build/shared/scripts/check_links.py                         # check cross-record link integrity
python3 build/shared/scripts/diagnose_workspace.py                  # workspace health report
python3 build/shared/scripts/diagnose_workspace.py --json           # machine-readable output
```

### Testing

There is no test suite. Verification is structural: run `ruff check`, assembly, and the validation scripts above.

## Python Style

Match the existing style in `build/assemble-skills.py` and `build/shared/`.

### File structure

- Shebang: `#!/usr/bin/env python3`
- First import: `from __future__ import annotations`
- Standard-library imports only (no third-party dependencies)
- CLI scripts use the `sys.path.insert` pattern for `_loom_lib`, then `# noqa: E402` on those imports

### CLI entrypoint pattern

Every script follows this exact shape:

```python
def main() -> int:
    parser = argparse.ArgumentParser(description="...")
    # ... define args ...
    args = parser.parse_args()
    workspace = find_workspace_root()
    # ... do work ...
    return 0  # or 1 on failure

if __name__ == "__main__":
    raise SystemExit(main())
```

### Types and generics

- Add type hints to all function signatures and non-trivial locals
- Use modern built-in generics: `dict[str, str]`, `list[Path]`, `tuple[dict, str]`
- Use `X | None` union syntax, not `Optional[X]`
- Avoid `typing` imports except `Any` when needed for argparse

### Naming conventions

- Functions and variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE` (module-level)
- Skill directories: `loom-<name>` (kebab-case)
- Record IDs: `<kind>:<slug>` (e.g., `ticket:0004`, `constitution:main`, `spec:my-feature`)
- File slugs for records: lowercase kebab-case derived from title

### Formatting

- Ruff default formatting (88 char line length)
- 4-space indentation
- Double quotes for strings
- Trailing commas in multi-line structures
- JSON output: `json.dumps(..., indent=2, sort_keys=True)`
- Frontmatter: JSON between `---` fences (not YAML despite the fence syntax)

### Imports

- Standard-library only; never add third-party deps
- Group: stdlib first, then blank line, then `_loom_lib` imports
- Keep import lists alphabetical within groups
- `from pathlib import Path` is always present

### Error handling

- Use `raise SystemExit("clear message")` for user-facing failures in CLI tools
- Treat missing files, malformed frontmatter, and invalid statuses as hard failures
- Never silently widen scope, guess at ambiguous ownership, or skip validation
- Fail closed: stop and surface the problem rather than picking a likely path

### Functions

- Keep functions small, direct, and deterministic
- Prefer `pathlib.Path` for all path work
- Use `find_workspace_root()` at the start of every CLI entrypoint
- Use `relative_to_workspace(path, workspace)` for all printed paths

## Markdown Content Guidelines

- Records use JSON frontmatter between `---` fences
- Required sections per record kind are defined in `build/shared/_loom_lib/core.py` (`SECTIONS_BY_KIND`)
- Valid statuses per kind are in `STATUS_BY_KIND` in the same file
- SKILL.md frontmatter must include `name` (matching directory) and `description` (must contain "Use when" and "Not for")
- Command files in `src/commands/` are pure Markdown prompt definitions with no script dependencies

## Editing Guidance

- Prefer the smallest correct change
- Content inside `src/` must be self-contained -- no references to `build/`, `.loom/`, or repo-root paths
- After changing shared code in `build/shared/`, run `python3 build/assemble-skills.py` to propagate
- When changing a rule, check related skills, references, and helper scripts
- Do not add dependencies, scaffolding, or invent a monolithic CLI without explicit need

### Cross-surface review checklist

If a change touches multiple surfaces, verify:
- `src/rules/` doctrine wording
- `src/skills/*/SKILL.md` instructions
- `src/skills/*/references/` docs
- `src/commands/` command definitions
- `build/shared/scripts/` helper behavior
- `build/shared/_loom_lib/` library code
- `build/assemble-skills.py` assembly logic

## Key Architecture Facts

- `_loom_lib/core.py` (~1145 lines) is the shared library: frontmatter parsing, record CRUD, validation, scope resolution, packet compilation, workspace discovery
- `_loom_lib/records.py` has record mutation helpers (link management, section updates)
- `_loom_lib/cli.py` has argparse helpers (scope args, link/assignment parsing)
- `_loom_lib/memory.py` has `.loom/memories/` module validation and indexing
- Each skill gets a subset of shared scripts (defined in `SKILL_SCRIPTS` dict in `assemble-skills.py`)
- Skill-local create scripts (e.g., `create_critique.py`) are authored per-skill, not shared
