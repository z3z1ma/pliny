# Installing Loom

Loom installs as a skills package.

The canonical surface is `skills/`. Native harness adapters may add metadata, manifests, or preload hooks around `skills/`, but they do not add a second Loom ontology and they do not replace the skills.

## Install model

The intended install pattern:

1. Install or expose `skills/` as the Loom package.
2. Keep skill names and descriptions from `skills/*/SKILL.md` visible to the harness.
3. Use `loom-bootstrap` first unless the same ordered doctrine is already loaded by an adapter.
4. Hydrate the task-specific skill when that skill owns the next truth change.
5. Let the model read templates and references from that skill as needed.

`loom-bootstrap` is mandatory. It is the entry skill that loads Loom's ordered doctrine and routes the agent into the right owner skill.

When a harness has an `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, user rules, or a similar instruction surface, point it at the skill rather than copying doctrine:

```md
Loom is active in this workspace. Before any work, use the `loom-bootstrap` skill unless Loom's ordered bootstrap doctrine is already loaded in the current context. After bootstrap, route work through the Loom skill that owns the next truth change.
```

That instruction is a pointer, not a new source of truth.

## Generic install

Loom has zero runtime dependencies at the protocol layer. Clone or download the repository and expose `skills/` wherever your harness expects skills.

```bash
git clone https://github.com/z3z1ma/agent-loom.git
```

Then configure your harness to see:

```text
/path/to/agent-loom/skills
```

Start every Loom session with:

```text
Use the loom-bootstrap skill. Then route the work through the Loom skill that owns the next truth change.
```

## Claude Code

Remote install:

```bash
claude plugin marketplace add z3z1ma/agent-loom
claude plugin install loom@agent-loom --scope user
```

Local development:

```bash
claude --plugin-dir /absolute/path/to/agent-loom
```

Local marketplace testing:

```bash
claude plugin marketplace add /absolute/path/to/agent-loom
claude plugin install loom@agent-loom --scope project
```

Validate the local plugin structure:

```bash
claude plugin validate /absolute/path/to/agent-loom
```

The repository includes a Claude Code plugin manifest at `.claude-plugin/plugin.json` and a local marketplace catalog at `.claude-plugin/marketplace.json`.

The plugin exposes canonical `skills/` directly from the repository root and declares `claude-hooks/hooks.json` as its Claude hook config. Loom uses that hook surface to emit the ordered `loom-bootstrap` references as same-session `SessionStart` hook stdout.

The hook preload is a convenience. The canonical surface remains `skills/`, especially `skills/loom-bootstrap`.

## OpenCode

Normal install:

```bash
opencode plugin open-loom --global
```

Equivalent package plugin entry:

```json
{
  "plugin": ["open-loom"]
}
```

For a cloned repository, point OpenCode at the local plugin file:

```json
{
  "plugin": ["file:///absolute/path/to/agent-loom/open-loom.mjs"]
}
```

For a local structural check that does not require a model request:

```bash
node open-loom.mjs --smoke
```

This repository includes the `open-loom` OpenCode plugin at `open-loom.mjs`. It requires OpenCode `>=1.14.22 <2`.

`open-loom` registers the bundled skill root with `config.skills.paths` and adds ordered `loom-bootstrap` references to `config.instructions`.

## Codex

Marketplace registration:

```bash
codex plugin marketplace add z3z1ma/agent-loom
```

Codex currently requires opening `/plugins` after marketplace registration to install or enable `loom`.

This repository includes a Codex plugin manifest at `.codex-plugin/plugin.json` and a marketplace catalog at `.agents/plugins/marketplace.json`. The plugin exposes canonical `skills/` directly from the repository root and is shaped for a Git-backed remote marketplace entry.

Current evidence still needs installed plugin skill-discovery validation for `loom-bootstrap`, so this is not yet a broadly accepted Codex release path. The repository `.codex/` hook fixture proves optional trusted project preload of bootstrap references. It is not the product install path.

## Cursor

Until `agent-loom` is listed in Cursor Marketplace, install from the Git repository as a local native Cursor plugin:

```bash
mkdir -p ~/.cursor/plugins/local
git clone https://github.com/z3z1ma/agent-loom.git ~/.cursor/plugins/local/agent-loom
```

Restart Cursor or run Developer: Reload Window after cloning.

Once the Marketplace listing exists, install from Cursor Agent chat with:

```text
/add-plugin agent-loom
```

This repository includes a Cursor plugin manifest at `.cursor-plugin/plugin.json`. The manifest follows Cursor's native plugin format and exposes canonical `skills/` with:

```json
{
  "skills": "./skills/"
}
```

## Gemini CLI

Install from the Git repository:

```bash
gemini extensions install https://github.com/z3z1ma/agent-loom
```

Local development can link the repository instead:

```bash
gemini extensions link /absolute/path/to/agent-loom
```

Validate the local extension structure:

```bash
gemini extensions validate /absolute/path/to/agent-loom
```

This repository includes a Gemini CLI extension manifest at `gemini-extension.json`.

The extension exposes canonical `skills/` and uses `contextFileName` to load `gemini-bootstrap.md`, which imports the ordered `skills/loom-bootstrap/references/*.md` files with Gemini's native context import syntax.

The context preload is a convenience. The canonical surface remains `skills/`, especially `skills/loom-bootstrap`.

## Bootstrap references

`loom-bootstrap` reads these references in order:

1. `skills/loom-bootstrap/references/01-core-identity.md`
2. `skills/loom-bootstrap/references/02-truth-and-authority.md`
3. `skills/loom-bootstrap/references/03-outer-loop.md`
4. `skills/loom-bootstrap/references/04-ralph-inner-loop.md`
5. `skills/loom-bootstrap/references/05-critique-and-wiki.md`
6. `skills/loom-bootstrap/references/06-filesystem-and-tooling.md`
7. `skills/loom-bootstrap/references/07-validation-and-honesty.md`

If a native adapter preloads those references, the agent can proceed directly into Loom routing. Otherwise, use `loom-bootstrap` before work starts.

## First workspace prompt

After installing Loom in a project, start with a small initialization request:

```text
Use loom-bootstrap. Then inspect this repository with loom-workspace and create the minimum Loom records needed to track the current work honestly.
```

For a specific project goal:

```text
Use loom-bootstrap. I want to work on: <goal>. Route through the Loom owner layer that should change first, and do not create extra records unless the graph needs them.
```

For implementation work that already has a ticket:

```text
Use loom-bootstrap and loom-tickets. Compile a Ralph packet for the next bounded implementation step. Include the upstream records the worker needs, the write scope, stop conditions, and the output contract.
```
