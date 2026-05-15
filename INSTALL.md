# Installing Loom

Install Core first. Add Playbooks if you want workflow routes.

| Package | Required | Provides |
| --- | --- | --- |
| `loom-core` | yes | `using-loom`, record skills, templates, references, optional preload hooks |
| `loom-playbooks` | no | workflow routes for debugging, TDD, review, migration, UI work, shipping, and similar tasks |

Every install method exposes the same Markdown skills. Native manifests and hooks
only help the harness find or preload them.

## One Rule

Before Loom work, the agent needs `using-loom` and its ordered references. Some
adapters preload them. If your harness does not, ask for them:

```text
Use using-loom. Then route this work through the smallest Loom surface that makes it recoverable.
```

Do not copy the doctrine into another project file. Point the harness at Core.
Activation is part of the doctrine: when Loom may apply, the agent should check
the relevant Loom skill before responding, asking clarifying questions, inspecting,
editing, creating tickets, or launching Ralph.

## Named Agents

Core also ships optional explicit Loom personas:

| Agent | Use |
| --- | --- |
| `loom-weaver` | Outer-loop shaping: challenge ideas, present options with recommendations, and create or update `.loom/` records before implementation. Loom Weaver writes only under `.loom/` and does not create Ralph packets. |
| `loom-driver` | Inner-loop coordination: compile Ralph packets, coordinate workers, reconcile outputs, preserve evidence, route audit, and update ticket state. Source-changing work runs through packet-bounded workers; direction-setting Loom records remain read-only during Driver coordination. |

| Harness | Invocation |
| --- | --- |
| OpenCode | Switch to the `loom-weaver` or `loom-driver` primary agent with the agent switcher. If using one as a subagent, invoke `@loom-weaver` or `@loom-driver` where OpenCode subagent mentions are available. |
| Claude Code | Use `/agents` to confirm installed plugin-scoped names. For a main session, use `claude --agent loom-core:loom-weaver` or `claude --agent loom-core:loom-driver` when that is the listed name; for one-shot use, invoke the listed agent with Claude's agent mention/typeahead. |
| Codex | Install and enable the Core plugin, then install the optional custom agent TOML files into `~/.codex/agents/`. Ask in natural language such as `Use the loom-weaver custom agent to shape this before implementation` or `Use the loom-driver custom agent to coordinate this ticket through packets`. Codex docs do not document `@<agent>` custom-agent invocation. |
| Cursor | Invoke the Core plugin subagent as `/loom-weaver` or `/loom-driver`, or ask Cursor to use the named subagent in natural language. Do not use `@loom-weaver` or `@loom-driver` as custom-agent claims; Cursor documents `@` for rules/context, not subagent invocation. |
| Gemini CLI | Core bundles `agents/loom-weaver.md` and `agents/loom-driver.md`; invoke `@loom-weaver <task>` or `@loom-driver <task>` to force the subagent. This is a delegated subagent call, not a primary-agent prompt switch. |

## Generic Local Setup

Clone the repo:

```bash
git clone https://github.com/z3z1ma/agent-loom.git
```

Expose Core to your harness:

```text
/absolute/path/to/agent-loom/loom-core
/absolute/path/to/agent-loom/loom-core/skills
```

Expose Playbooks only if you want them:

```text
/absolute/path/to/agent-loom/loom-playbooks
/absolute/path/to/agent-loom/loom-playbooks/skills
```

If your harness has `AGENTS.md`, user rules, or a similar instruction file, keep
the pointer short:

```md
Loom is active here. Use `using-loom` before Loom work unless the same doctrine is
already preloaded. Route durable facts through Loom records. Optional workflow
skills add routes without changing the owning surfaces.
```

## OpenCode

Install Core globally:

```bash
opencode plugin @z3z1ma/open-loom-core --global
```

Install Core plus Playbooks:

```bash
opencode plugin @z3z1ma/open-loom-core --global
opencode plugin @z3z1ma/open-loom-playbooks --global
```

Project config can name the packages directly:

```json
{
  "plugin": [
    "@z3z1ma/open-loom-core",
    "@z3z1ma/open-loom-playbooks"
  ]
}
```

For a local clone, point at the package entrypoints:

```json
{
  "plugin": [
    "file:///absolute/path/to/agent-loom/loom-core/loom-core.mjs",
    "file:///absolute/path/to/agent-loom/loom-playbooks/loom-playbooks.mjs"
  ]
}
```

`@z3z1ma/open-loom-core` registers record skills through `config.skills.paths` and
injects stripped `using-loom` doctrine plus ordered references into the first user
message with `experimental.chat.messages.transform`. `@z3z1ma/open-loom-playbooks`
adds optional workflow-specific skills and expects the operating doctrine to be
available.

OpenCode package engines currently require `>=1.14.22 <2`.

## Claude Code

Remote marketplace install:

```bash
claude plugin marketplace add z3z1ma/agent-loom
claude plugin install loom-core@agent-loom --scope user
claude plugin install loom-playbooks@agent-loom --scope user
```

Install `loom-core` before `loom-playbooks`.

Local development from a clone:

```bash
claude --plugin-dir /absolute/path/to/agent-loom/loom-core
claude --plugin-dir /absolute/path/to/agent-loom/loom-playbooks
```

Local marketplace testing:

```bash
claude plugin marketplace add /absolute/path/to/agent-loom
claude plugin install loom-core@agent-loom --scope project
claude plugin install loom-playbooks@agent-loom --scope project
```

Validate package roots after manifest changes:

```bash
claude plugin validate /absolute/path/to/agent-loom/loom-core
claude plugin validate /absolute/path/to/agent-loom/loom-playbooks
```

Claude reads skills from each package's `skills/` directory. If hook preload is
unavailable in your environment, start with `using-loom`.

## Codex

Register the marketplace catalog:

```bash
codex plugin marketplace add z3z1ma/agent-loom
```

The Codex catalog lives at `.agents/plugins/marketplace.json`. Package manifests
live at:

```text
loom-core/.codex-plugin/plugin.json
loom-playbooks/.codex-plugin/plugin.json
```

Core declares `loom-core/hooks/hooks.json` for `using-loom` preload where Codex
supports plugin hooks. Validate preload behavior in the target Codex environment.
If it is unavailable, ask for `using-loom` before Loom work.

Install the optional Loom Weaver and Loom Driver Codex custom agents:

```bash
mkdir -p ~/.codex/agents
curl -fsSL https://raw.githubusercontent.com/z3z1ma/agent-loom/main/loom-core/codex/agents/loom-weaver.toml -o ~/.codex/agents/loom-weaver.toml
curl -fsSL https://raw.githubusercontent.com/z3z1ma/agent-loom/main/loom-core/codex/agents/loom-driver.toml -o ~/.codex/agents/loom-driver.toml
```

For a local clone, copy the same file instead:

```bash
mkdir -p ~/.codex/agents
cp /absolute/path/to/agent-loom/loom-core/codex/agents/loom-weaver.toml ~/.codex/agents/loom-weaver.toml
cp /absolute/path/to/agent-loom/loom-core/codex/agents/loom-driver.toml ~/.codex/agents/loom-driver.toml
```

After installing the files, start a new Codex session and ask Codex to use the
`loom-weaver` or `loom-driver` custom agent in natural language. Use `/agent` in
the CLI to inspect or switch active spawned agent threads. This is custom-agent
installation, not a plugin-shipped profile and not `@<agent>` invocation.

## Cursor

Until `agent-loom` is listed in Cursor Marketplace, install from the Git repo as a
local plugin source:

```bash
mkdir -p ~/.cursor/plugins/local
git clone https://github.com/z3z1ma/agent-loom.git ~/.cursor/plugins/local/agent-loom
```

Restart Cursor or run `Developer: Reload Window`.

The Cursor catalog lives at `.cursor-plugin/marketplace.json`. Package manifests
live at:

```text
loom-core/.cursor-plugin/plugin.json
loom-playbooks/.cursor-plugin/plugin.json
```

Enable Core before Playbooks. Core points at `loom-core/hooks/hooks-cursor.json`
for `using-loom` preload where Cursor supports hooks. If native plugin discovery
or hooks are unavailable, expose the two `skills/` directories and start with
`using-loom`.

## Gemini CLI

Full local install from a clone:

```bash
git clone https://github.com/z3z1ma/agent-loom
cd agent-loom
gemini extensions link "$PWD/loom-core"
gemini extensions link "$PWD/loom-playbooks"
```

Core-only install from a clone:

```bash
gemini extensions link /absolute/path/to/agent-loom/loom-core
```

The repository root also has a Gemini-only Core shim:

```bash
gemini extensions install https://github.com/z3z1ma/agent-loom
```

The root shim installs Core only because Gemini tooling looks for
`gemini-extension.json` at the repo root. Link `loom-playbooks` separately if you
want playbooks.

Validate extension structures after manifest changes:

```bash
gemini extensions validate /absolute/path/to/agent-loom
gemini extensions validate /absolute/path/to/agent-loom/loom-core
gemini extensions validate /absolute/path/to/agent-loom/loom-playbooks
```

Gemini loads `loom-core/gemini-bootstrap.md`, which imports `using-loom` and the
ordered references with native context import syntax.

## Bootstrap Files

Core loads these files in order:

1. `loom-core/skills/using-loom/SKILL.md`
2. `loom-core/skills/using-loom/references/how-loom-thinks.md`
3. `loom-core/skills/using-loom/references/activation-discipline.md`
4. `loom-core/skills/using-loom/references/directory-structure.md`
5. `loom-core/skills/using-loom/references/shaping-with-humans.md`
6. `loom-core/skills/using-loom/references/delegating-to-workers.md`
7. `loom-core/skills/using-loom/references/proving-the-work.md`
8. `loom-core/skills/using-loom/references/staying-safe.md`

If an adapter preloads those files, the agent can route into Loom work. If it does
not, use `using-loom` explicitly.

## First Prompts

Start a workspace:

```text
Use using-loom. Inspect this repository and create only the Loom records needed so current state is clear.
```

Start a task:

```text
Use using-loom. I want to work on: <goal>. Shape the next move with me if needed, then route durable facts through Loom records.
```

Delegate a bounded implementation pass:

```text
Use using-loom and loom-ralph. Compile one Ralph packet with mission, context, read scope, write scope, stop conditions, verification posture, and output contract.
```

## Verify Package Changes

Run package checks from a local clone:

```bash
npm --prefix loom-core run smoke
npm --prefix loom-playbooks run smoke
npm --prefix loom-core run pack:check
npm --prefix loom-playbooks run pack:check
```

For Markdown-only edits, also run:

```bash
git diff --check
```
