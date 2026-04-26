# Installing Loom

Loom installs as a skills package.

The product surface is `skills/`. Native harness adapters may add metadata,
manifests, or preload hooks around that directory, but they do not add a second
Loom ontology and they do not replace the skills.

## Required Loading Model

Expose the frontmatter `name` and `description` from each `skills/*/SKILL.md`.

The `loom-bootstrap` skill is mandatory. Agents should use it before starting any
work unless the same ordered bootstrap doctrine is already loaded in the current
context by a native adapter.

`loom-bootstrap` reads these references in order:

1. `skills/loom-bootstrap/references/01-core-identity.md`
2. `skills/loom-bootstrap/references/02-truth-and-authority.md`
3. `skills/loom-bootstrap/references/03-outer-loop.md`
4. `skills/loom-bootstrap/references/04-ralph-inner-loop.md`
5. `skills/loom-bootstrap/references/05-critique-and-wiki.md`
6. `skills/loom-bootstrap/references/06-filesystem-and-tooling.md`
7. `skills/loom-bootstrap/references/07-validation-and-honesty.md`

Harnesses may preload those references as always-on context. That is an adapter
optimization over the same skill package, not a separate doctrine source.

## Native Harness Installs

Use the native package system for each harness.

| Harness | Native path | Loom surface |
| --- | --- | --- |
| Claude Code | Claude plugin manifest and marketplace metadata | `skills/`, plus optional `SessionStart` preload from `loom-bootstrap` references |
| Codex | Codex plugin manifest and marketplace metadata | `skills/` with `loom-bootstrap` as the required entry skill |
| OpenCode | `open-loom` plugin | `skills/`, plus OpenCode `instructions` preload from `loom-bootstrap` references |
| Cursor | Cursor plugin/skill package | `skills/` with `loom-bootstrap` as the required entry skill |
| Gemini CLI | Gemini extension/skill package | `skills/` with `loom-bootstrap` as the required entry skill |

There is no supported Makefile, shell installer, or cross-harness fallback copy
script. Older generated installs should be treated as legacy local state and
cleaned up manually if they are still present.

## Quick Install Commands

Use the harness-native command for your environment:

| Harness | Command |
| --- | --- |
| Claude Code | `claude plugin marketplace add z3z1ma/agent-loom && claude plugin install loom@agent-loom --scope user` |
| OpenCode | `opencode plugin open-loom --global` |
| Codex | `codex plugin marketplace add z3z1ma/agent-loom` |
| Cursor | `mkdir -p ~/.cursor/plugins/local && git clone https://github.com/z3z1ma/agent-loom.git ~/.cursor/plugins/local/agent-loom` |
| Gemini CLI | `gemini extensions install https://github.com/z3z1ma/agent-loom` |

Codex currently requires opening `/plugins` after marketplace registration to
install or enable `loom`. Cursor's command above uses Cursor's native local plugin
directory until `agent-loom` is listed in Cursor Marketplace; after listing, the
Cursor Agent chat command should be `/add-plugin agent-loom`.

## Minimal Harness Instruction

When a harness has an `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, user rules, or a
similar instruction surface, point it at the skill rather than copying doctrine:

```md
Loom is active in this workspace. Before any work, use the `loom-bootstrap` skill
unless Loom's ordered bootstrap doctrine is already loaded in the current context.
After bootstrap, route work through the Loom skill that owns the next truth
change.
```

That instruction is a pointer, not a new source of truth.

## Claude Code

This repository includes a Claude Code plugin manifest at
`.claude-plugin/plugin.json` and a local marketplace catalog at
`.claude-plugin/marketplace.json`.

The plugin exposes canonical `skills/` directly from the repository root and
declares `claude-hooks/hooks.json` as its Claude hook config. Loom uses that hook
surface to emit the ordered `loom-bootstrap` references as same-session
`SessionStart` hook stdout.

Local development:

```bash
claude --plugin-dir /absolute/path/to/agent-loom
```

Local marketplace testing:

```bash
claude plugin marketplace add /absolute/path/to/agent-loom
claude plugin install loom@agent-loom --scope project
```

Remote install:

```bash
claude plugin marketplace add z3z1ma/agent-loom && claude plugin install loom@agent-loom --scope user
```

Validate the local plugin structure with:

```bash
claude plugin validate /absolute/path/to/agent-loom
```

The hook preload is a bonus. The canonical surface remains `skills/`, especially
`skills/loom-bootstrap`.

## Codex

This repository includes a Codex plugin manifest at `.codex-plugin/plugin.json`
and a marketplace catalog at `.agents/plugins/marketplace.json`. The plugin
exposes canonical `skills/` directly from the repository root and is shaped for a
Git-backed remote marketplace entry.

The target native remote path is Codex marketplace registration with the
repository URL:

```bash
codex plugin marketplace add z3z1ma/agent-loom
```

Once installed plugin skill discovery is validated, users should be able to open
Codex's `/plugins` browser and install or enable `loom` from the `agent-loom`
marketplace.

Current evidence still needs installed plugin skill-discovery validation for
`loom-bootstrap`, so this is not yet a broadly accepted Codex release path. The
repository `.codex/` hook fixture proves optional trusted project preload of
bootstrap references; it is not the product install path.

## OpenCode

This repository includes the `open-loom` OpenCode plugin at `open-loom.mjs`.
`open-loom` requires OpenCode `>=1.14.22 <2`.

Normal users can install the OpenCode plugin and update global config with:

```bash
opencode plugin open-loom --global
```

Equivalent package plugin entry:

```json
{
  "plugin": ["open-loom"]
}
```

Users working from a cloned repository should point OpenCode at the local plugin
file instead:

```json
{
  "plugin": ["file:///absolute/path/to/agent-loom/open-loom.mjs"]
}
```

`open-loom` registers the bundled skill root with `config.skills.paths` and adds
ordered `loom-bootstrap` references to `config.instructions`.

For a local structural check that does not require a model request, run:

```bash
node open-loom.mjs --smoke
```

## Cursor

This repository includes a Cursor plugin manifest at `.cursor-plugin/plugin.json`.
The manifest follows Cursor's native plugin format and exposes canonical `skills/`
with `"skills": "./skills/"`.

Until `agent-loom` is listed in Cursor Marketplace, install from the Git repository
as a local native Cursor plugin:

```bash
mkdir -p ~/.cursor/plugins/local && git clone https://github.com/z3z1ma/agent-loom.git ~/.cursor/plugins/local/agent-loom
```

Restart Cursor or run Developer: Reload Window after cloning. Once the Marketplace
listing exists, install from Cursor Agent chat with:

```text
/add-plugin agent-loom
```

## Gemini CLI

This repository includes a Gemini CLI extension manifest at
`gemini-extension.json`. The extension exposes canonical `skills/` and uses
`contextFileName` to load `gemini-bootstrap.md`, which imports the ordered
`skills/loom-bootstrap/references/*.md` files with Gemini's native context import
syntax.

Install from the Git repository with:

```bash
gemini extensions install https://github.com/z3z1ma/agent-loom
```

Local development can link the repository instead:

```bash
gemini extensions link /absolute/path/to/agent-loom
```

Validate the local extension structure with:

```bash
gemini extensions validate /absolute/path/to/agent-loom
```

The context preload is a bonus. The canonical surface remains `skills/`,
especially `skills/loom-bootstrap`.

## Workspace Bootstrap

Loom does not create a runtime database. In a project that uses Loom, the agent
creates and edits `.loom/` records directly using the relevant skills and
templates.

The common workspace tree is:

```text
.loom/
├── constitution/
├── initiatives/
├── research/
├── specs/
├── plans/
├── tickets/
├── evidence/
├── critique/
├── wiki/
├── packets/
└── memory/
```

Use `skills/loom-workspace`, `skills/loom-constitution`, and
`skills/loom-tickets` for the first records.
