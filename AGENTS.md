# AGENTS.md

## What This Repo Is

This repository develops a distributable product. The product is the top-level `rules/`, `skills/`, and `commands/` directories plus the standalone skill-local `scripts/*.py` CLIs committed directly in each skill. End users copy those directories into their own projects (typically into `.opencode/` or a similar harness-specific location). The product is Markdown-first with bundled Python helpers -- not a normal app, service, or library.

There is no app runtime, build pipeline, or test suite. Each `skills/*/scripts/*.py` file is both the shipped artifact and the only source of truth for that skill's CLI behavior.

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

The repository is flat at the top level. Each CLI-backed skill owns one standalone `scripts/*.py` file directly.

### Product source

Everything a user receives lives here:

- `rules/` -- always-on doctrine files (Markdown + `appendices/`)
- `skills/` -- self-contained skill directories, each with `SKILL.md` and optional `references/` / `scripts/` surfaces when that skill ships them
- `commands/` -- slash-command definitions (Markdown files that define prompt-based commands)

**Isolation rule**: nothing inside `rules/`, `skills/`, or `commands/` may reference anything outside those product directories. No `.loom/` paths, no repo-root paths. Skills reference their own scripts as `scripts/...` and their own docs as `references/...`. Each skill ships its own standalone `scripts/*.py` file.

### Dogfooding artifacts: `.opencode/` and `.loom/`

This repo uses its own product. `.opencode/rules`, `.opencode/skills`, and `.opencode/commands` are symlinks pointing back into the top-level product directories, so the development environment consumes the product in the same way an end user would. `.loom/` contains Loom records (tickets, specs, plans, etc.) created by using the product on this repo.

Neither `.opencode/` nor `.loom/` is a maintained source surface. They are consumption artifacts. Do not treat them as source of truth for how the product works -- look at `rules/`, `skills/`, and `commands/` instead.

## Commands

### Linting

```bash
uvx ruff check skills/*/scripts/*.py           # lint shipped CLIs
uvx ruff check path/to/file.py        # lint a single file
uvx ruff format --check skills/*/scripts/*.py
uvx ruff format path/to/file.py       # auto-format a single file
```

### Validation commands

```bash
skills/loom-tickets/scripts/tickets.py create ticket
```

### Testing

There is no test suite. Verification is structural: run `ruff check` and the skill-local validation commands above.

## Python Style

Match the existing style in committed `skills/*/scripts/*.py` files.

### File structure

- First import: `from __future__ import annotations`
- Standalone skill scripts remain standard-library only
- One file should contain the whole behavior for that skill's CLI

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
- Keep files readable top-to-bottom; there should be one obvious place to edit behavior

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
- Group: stdlib first, then blank line, then local definitions in the same file
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
- Required sections and valid statuses per record kind are defined locally inside each `skills/*/scripts/*.py`
- SKILL.md frontmatter must include `name` (matching directory) and `description` (must contain "Use when" and "Not for")
- Command files in `commands/` are pure Markdown prompt definitions with no script dependencies

## Editing Guidance

- Prefer the smallest correct change
- Content inside `rules/`, `skills/`, and `commands/` must be self-contained -- no references to `.loom/` or repo-root paths
- When changing a skill-local CLI, edit `skills/*/scripts/*.py` directly
- When changing a rule, check related skills, references, and helper scripts
- Do not add dependencies, scaffolding, or invent a monolithic CLI without explicit need

### Cross-surface review checklist

If a change touches multiple surfaces, verify:
- `rules/` doctrine wording
- `skills/*/SKILL.md` instructions
- `skills/*/references/` docs
- `skills/*/scripts/*.py`
- `commands/` command definitions

## Key Architecture Facts

- each `skills/*/scripts/*.py` owns that skill's CLI behavior directly
- each skill-local CLI should stay self-contained, even if that means duplicating helper code
- there is no separate generator or hidden authoring layer for shipped CLIs
