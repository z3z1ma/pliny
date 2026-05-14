# Direct Interactive Agent Surfaces

ID: research:20260514-direct-interactive-agent-surfaces
Type: Research
Status: completed
Created: 2026-05-14
Updated: 2026-05-14

## Summary

Agent Loom's supported harnesses do not use one common "agent" abstraction. OpenCode and Claude Code have the strongest directly interactable system-prompt-switching surfaces; Gemini can replace the main system prompt through `GEMINI_SYSTEM_MD` but does not expose a first-class named primary-agent catalog; Cursor mainly exposes custom agents as subagents plus rules for main-Agent behavior; Codex custom agents are documented as TOML files under `~/.codex/agents/` or `.codex/agents/`, while Codex plugins do not currently package custom agents or profiles.

## Question

How do Agent Loom's supported coding harnesses let a package or user add an "agent" when the desired product shape is a directly interactable system-prompt/persona switch rather than a proxy-only subagent?

## Scope

Covered harnesses are the support surfaces present in this repository: OpenCode, Claude Code, Codex, Cursor, and Gemini CLI.

Covered mechanisms include native agent definitions, subagents when relevant, plugin/extension distribution, rule or context systems that alter the main assistant, and system-prompt/profile switching.

Excluded:

- Live validation inside each harness.
- Designing or implementing new Agent Loom package contents.
- Non-supported coding harnesses.

## Method And Sources

- Project support matrix: `AGENTS.md`, `INSTALL.md`, `CLAUDE.md`, `loom-core/loom-core.mjs`, `loom-playbooks/loom-playbooks.mjs`, `loom-core/hooks/hooks.json`, `loom-core/hooks/hooks-cursor.json`, `loom-core/gemini-bootstrap.md`, `loom-*/.claude-plugin/plugin.json`, `loom-*/.cursor-plugin/plugin.json`, `loom-*/.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, `.claude-plugin/marketplace.json`, and `.cursor-plugin/marketplace.json`.
- OpenCode official docs, `https://opencode.ai/docs/agents/#primary-agents`, accessed 2026-05-14.
- Claude Code official docs, `https://docs.anthropic.com/en/docs/claude-code/sub-agents`, `https://docs.anthropic.com/en/docs/claude-code/plugins`, and `https://docs.anthropic.com/en/docs/claude-code/plugins-reference`, accessed 2026-05-14.
- Cursor official docs, `https://cursor.com/docs/subagents`, `https://cursor.com/docs/rules`, `https://cursor.com/docs/plugins`, and `https://cursor.com/docs/agent/overview`, accessed 2026-05-14. The `cursor.com` pages were retrieved through a reader proxy after direct `docs.cursor.com` fetches returned only the dynamic documentation shell.
- Codex official docs, `https://developers.openai.com/codex/subagents`, `https://developers.openai.com/codex/concepts/subagents`, `https://developers.openai.com/codex/config-reference`, `https://developers.openai.com/codex/config-advanced`, `https://developers.openai.com/codex/cli/reference`, `https://developers.openai.com/codex/plugins`, and `https://developers.openai.com/codex/plugins/build`, accessed 2026-05-14 and rechecked 2026-05-14 after the Codex custom-agent install decision.
- Gemini CLI official repository docs, `https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/core/subagents.md`, `docs/core/remote-agents.md`, `docs/cli/skills.md`, `docs/cli/system-prompt.md`, `docs/cli/gemini-md.md`, `docs/extensions/index.md`, and `docs/reference/configuration.md`, accessed 2026-05-14.
- Existing Loom research: `research:20260513-superpowers-skill-activation` for prior adapter/bootstrap context.

## Findings

### Project Support Surfaces

Agent Loom currently supports these harnesses:

| Harness | Current repository surface |
| --- | --- |
| OpenCode | `loom-core/loom-core.mjs` and `loom-playbooks/loom-playbooks.mjs` register skills; Core injects `using-loom` and ordered references into the first user message. |
| Claude Code | `.claude-plugin` manifests expose skills; Core hook config can preload `using-loom` where hooks are available. |
| Codex | `.codex-plugin` manifests expose skills, hooks, and install-surface prompts; `.agents/plugins/marketplace.json` exposes package catalogs. |
| Cursor | `.cursor-plugin` manifests expose skills and Core hook preload where supported. |
| Gemini CLI | `gemini-extension.json` files expose Core context through `gemini-bootstrap.md`; Playbooks depend on Core and do not duplicate the bootstrap. |

### OpenCode

OpenCode has the cleanest native fit for directly interactable agents.

- OpenCode distinguishes `primary` agents from `subagent` agents.
- Primary agents are the assistants users interact with directly and can switch with Tab or the configured `switch_agent` keybind.
- Custom agents can be defined in `opencode.json` under `agent.<name>` or as Markdown files under global `~/.config/opencode/agents/` or project `.opencode/agents/`.
- A Markdown agent's filename becomes the agent name. Frontmatter and body configure description, mode, model, temperature, permissions, and the system prompt.
- `mode` can be `primary`, `subagent`, or `all`; `primary` is the shape that matches a user-selectable system-prompt switch.
- OpenCode also supports `opencode agent create` to generate an agent file interactively.
- Subagents can be manually `@` mentioned and navigated as child sessions. If explicit one-shot invocation is acceptable, OpenCode supports both `@<subagent>` invocation and superior primary-agent switching via Tab/keybind.

### Claude Code

Claude Code calls the reusable definition a subagent, but it can run one as the main session agent.

- Custom subagents are Markdown files with YAML frontmatter and a prompt body.
- Definitions can live in managed settings, a `--agents` CLI JSON payload, project `.claude/agents/`, user `~/.claude/agents/`, or a plugin `agents/` directory.
- Plugin agents appear in `/agents`, can be invoked automatically, and can be manually invoked by users.
- The user can start the whole Claude Code session with `claude --agent <name>`, including plugin-scoped names such as `claude --agent <plugin-name>:<agent-name>`.
- The `agent` setting in `.claude/settings.json` can make a given agent the project default.
- When run as the main session agent, the subagent's system prompt replaces the default Claude Code system prompt in the same way as `--system-prompt`; `CLAUDE.md` and project memory still load through the normal message flow.
- Plugin `settings.json` currently supports the `agent` key, letting a plugin activate one of its shipped agents as the main thread when enabled.
- Plugin-shipped agents do not support `hooks`, `mcpServers`, or `permissionMode` frontmatter for security, but they do support model, effort, tools, disallowed tools, skills, memory, background, and worktree isolation fields.
- For one-shot explicit invocation, Claude Code supports `@` mentions such as `@agent-<name>` or a typeahead form like `@"<name> (agent)"`. This guarantees the named agent runs for that task, but the user's full message still goes to Claude, which writes the subagent task prompt.

### Cursor

Cursor's documented custom agents are subagents, not selectable primary-agent personas.

- Cursor Agent itself is the directly interactable assistant. It is built from instructions, tools, and the selected model.
- Cursor supports custom subagents in project `.cursor/agents/`, `.claude/agents/`, `.codex/agents/` and user `~/.cursor/agents/`, `~/.claude/agents/`, `~/.codex/agents/`.
- `.cursor/` definitions take precedence over `.claude/` and `.codex/` definitions when names conflict.
- Cursor custom subagents are Markdown files with YAML frontmatter and a prompt body. Fields include `name`, `description`, `model`, `readonly`, and `is_background`.
- Cursor Agent can delegate automatically based on subagent descriptions. Users can explicitly request one with `/name` syntax or natural language such as "Use the verifier subagent".
- The subagent still receives a task prompt from the parent Agent and returns a result to the parent. This is not the same as switching the main interactive assistant's system prompt.
- Cursor rules are the direct main-Agent instruction surface. Rules live in `.cursor/rules` and can be Always Apply, Apply Intelligently, file-scoped, or manual by `@` mention.
- Cursor also supports `AGENTS.md` in the project root and subdirectories as a simpler instruction source for Agent.
- Cursor plugins can package rules, skills, agents, commands, MCP servers, and hooks. For direct main-Agent behavior, rules or `AGENTS.md` are a better fit than subagents; for named specialist workers, plugin agents/subagents are available but proxy-mediated.
- Cursor's documented explicit subagent syntax is `/name`, not `@name`. Cursor uses `@` mentions for rules and context, while custom subagents use slash syntax or natural-language requests.

### Codex

Codex custom agents are currently subagent role definitions, while direct main-session prompt switching is handled through profiles and instruction configuration.

- Codex supports subagent workflows with built-in agents `default`, `worker`, and `explorer`.
- Codex only spawns subagents when the user explicitly asks it to use subagents or parallel agent work.
- Custom agents are standalone TOML files under `~/.codex/agents/` or `.codex/agents/`.
- Each custom agent file defines one spawned-session configuration layer and must include `name`, `description`, and `developer_instructions`.
- Custom agent files can also set normal Codex config keys such as `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, and `skills.config`.
- `agents.<name>.config_file` in `config.toml` can point a role at a TOML config layer.
- The CLI has `/agent` to switch between active agent threads and inspect ongoing work, but these are still spawned agent threads, not the initial primary conversation persona.
- The CLI reference did not show a `--agent` flag analogous to Claude Code. It does support `--profile` and one-off config overrides.
- For direct system-prompt/persona switching, Codex's better fit is a profile that sets `developer_instructions` or `model_instructions_file`, invoked with `codex --profile <name>`. Profiles are documented as experimental and not supported in the Codex IDE extension.
- Codex plugins currently bundle skills, apps, MCP servers, and hooks. The plugin docs say more capabilities are coming; they do not currently document plugin-shipped custom agents.
- Codex does not document an `@<agent-name>` custom-agent invocation path. Users ask Codex to spawn named agents in natural language, and `/agent` switches among already-active agent threads. Codex plugin docs do describe `@` invocation for plugins or bundled skills, not custom agents.
- The operator rejected the bundled-skill route for Loom Weaver. The supported Codex route is to ship a ready custom-agent TOML file and document installing it under `~/.codex/agents/loom-weaver.toml`, for example by curling the raw GitHub file. Plugin docs still do not document a manifest field for plugin-shipped profiles, `agents/`, or `.codex/agents` files, so this remains an explicit custom-agent install step rather than plugin-automatic installation.

### Gemini CLI

Gemini CLI has local and remote subagents, plus a separate full system-prompt override for the main session.

- Local custom subagents are Markdown files under project `.gemini/agents/*.md` or user `~/.gemini/agents/*.md`.
- The Markdown body becomes the subagent system prompt. Frontmatter includes `name`, `description`, `kind`, `tools`, `mcpServers`, `model`, `temperature`, `max_turns`, and `timeout_mins`.
- Subagents are exposed to the main Gemini agent as tools. The main agent can delegate automatically, or the user can force a subagent with `@name` at the start of a prompt.
- The `@` syntax injects a system note nudging the primary model to call that subagent immediately; it does not directly make that subagent the main chat agent.
- Gemini subagents run in isolated context and cannot call other subagents.
- Remote subagents use the A2A protocol and are also defined as Markdown files under `.gemini/agents` or `~/.gemini/agents`, with `kind: remote` and agent-card/auth fields.
- Gemini extensions can package prompts, MCP servers, custom commands, themes, hooks, sub-agents, and agent skills.
- For direct main-session system-prompt switching, Gemini exposes `GEMINI_SYSTEM_MD`. When set, it completely replaces the built-in system prompt with a Markdown file such as project `.gemini/system.md` or a custom path.
- The system prompt override supports substitutions such as `${AgentSkills}`, `${SubAgents}`, `${AvailableTools}`, and individual tool-name variables. This is powerful but high-authority because it replaces, rather than merges with, the built-in system prompt.

## Tradeoffs

| Harness | Directly interactable named agent fit | Best direct route | Main weakness |
| --- | --- | --- | --- |
| OpenCode | Strong | `mode: primary` custom agent | Need to keep skill registration/bootstrap separate from the primary-agent prompt. |
| Claude Code | Strong | Plugin or standalone agent plus `claude --agent` or `agent` setting | The object is still called a subagent, and default activation through plugin `settings.json` is consequential. |
| Cursor | Weak to medium | Rules or `AGENTS.md` for main Agent behavior; subagent only for explicit delegated specialists | Custom agents are subagents invoked by the parent Agent, not primary personas. |
| Codex | Weak to medium | Manual custom-agent TOML install under `~/.codex/agents/` followed by natural-language agent use; `--profile` remains a separate user configuration mechanism | Current plugin docs do not package profiles or custom agents, so custom-agent installation is explicit rather than plugin-automatic. |
| Gemini CLI | Medium | `GEMINI_SYSTEM_MD` for direct main prompt; `.gemini/agents` only for subagents | System override is not a named first-class agent picker and replaces core prompt wholesale. |

| Harness | Explicit one-shot agent invocation | Notes |
| --- | --- | --- |
| OpenCode | Yes: `@<subagent>` | Also supports better primary-agent switching with Tab/keybind for `mode: primary`. |
| Claude Code | Yes: `@agent-<name>` or typeahead `@"<name> (agent)"` | One-shot path still lets Claude write the subagent task prompt; `claude --agent` is the main-session alternative. |
| Gemini CLI | Yes: `@<name>` at the start of the prompt | This nudges the primary model to call the subagent tool immediately; it is not a primary-agent switch. |
| Cursor | No documented `@<agent>` subagent syntax; yes via `/name` | `@` is documented for rules/context. Subagents are explicitly invoked with slash syntax or natural language. |
| Codex | No documented `@<agent>` custom-agent syntax | Natural-language spawning and `/agent` thread switching are documented. `@` applies to plugins/skills, not custom agents. |

For Agent Loom, "agent equals system-prompt switch" favors OpenCode primary agents and Claude Code main-session agents first. Gemini can satisfy the prompt-switch requirement through `GEMINI_SYSTEM_MD` but would likely need a wrapper or explicit operator command. Cursor and Codex should not be treated as first-class direct-agent surfaces unless we accept rules or skills as the equivalent of an agent for those harnesses.

## Rejected Paths And Null Results

- Treating all harness "agent" directories as equivalent is rejected. OpenCode primary agents and Claude Code `--agent` main sessions are user-interactive primary contexts; Cursor, Codex, and Gemini agent directories are primarily delegated subagents.
- Treating explicit subagent invocation as direct interaction is rejected for the user's stated preference. `/name`, `@name`, or natural-language subagent invocation still usually routes through a parent agent that creates the actual task prompt.
- Treating explicit subagent invocation as equivalent to primary-agent switching remains rejected. However, if product requirements accept one-shot explicit invocation, OpenCode, Claude Code, and Gemini satisfy that with `@` syntax, Cursor satisfies it with `/name`, and Codex satisfies it only through natural-language spawning/thread management rather than `@`.
- Treating skills as primary agents is rejected. Skills can change behavior on demand but are not named main assistants. For Codex specifically, Loom Weaver should remain a custom agent TOML rather than a Core skill.
- Treating project rules, `AGENTS.md`, or `GEMINI.md` as agents is only partially valid. They can change the primary model's instructions, but they are not selectable named personas in most harnesses.

## Conclusions

- OpenCode should be the reference implementation for first-class direct agents: define a `primary` agent with a dedicated prompt, while continuing to register Loom skills separately.
- Claude Code can provide a comparable direct experience by shipping an agent definition and documenting `claude --agent <plugin-scoped-name>` or, more aggressively, shipping plugin `settings.json` with `agent` to activate it by default.
- Cursor should use rules or `AGENTS.md` for direct main-Agent instruction changes. Cursor custom agents can be packaged and explicitly invoked with `/name`, but they remain subagents and are not ideal for the stricter direct-primary-agent product goal.
- Codex should use a ready `loom-weaver.toml` custom-agent definition installed under `~/.codex/agents/`. Profiles or instruction-file overrides remain the direct main-session persona mechanism, but current plugin docs do not package them, so they should not be presented as the default Loom Weaver path.
- Gemini CLI should use `GEMINI_SYSTEM_MD` when a true main-agent prompt replacement is required. Extension-packaged subagents are available but proxy-mediated.

## Recommendations

- If Agent Loom adds an "agent" product surface, define the canonical content once as a prompt fragment and adapt it per harness rather than forcing every harness to use a subagent directory.
- Prioritize OpenCode `mode: primary` and Claude Code plugin `agents/` plus `--agent` documentation as the high-confidence direct-agent paths.
- If one-shot explicit invocation is acceptable, document OpenCode `@<subagent>`, Claude `@agent-<name>`, Gemini `@<name>`, Cursor `/name`, and Codex natural-language plugin or skill use separately rather than claiming all harnesses support the same `@` pattern.
- For Cursor, package both a rule for direct Agent behavior and an optional subagent only if a delegated verifier/reviewer persona is useful; document `/name`, not `@name`, as the explicit subagent path.
- For Codex, ship a ready `loom-core/codex/agents/loom-weaver.toml` and document installing it with `mkdir -p ~/.codex/agents` plus `curl` from GitHub raw content or local copy. Do not claim plugin-provided `--profile` support unless Codex adds documented plugin-shipped profiles; do not rely on `@<agent>` because current docs only show `@` for plugins/skills.
- For Gemini, document `GEMINI_SYSTEM_MD` as the direct persona switch and keep extension subagents for delegated specialist work.
- Before implementation, create a spec or ticket that decides whether "agent" in Agent Loom means only first-class named primary sessions or also includes profile/rule/system-prompt override equivalents.

## Open Questions

- Should Agent Loom ship direct-agent surfaces that can become default automatically, or only optional named agents that users explicitly select?
- Should Cursor and Codex be considered supported for an "agent" feature if the closest direct mechanism is rules or explicit custom-agent installation rather than native primary agents?
- Should Gemini's full system-prompt override be avoided because it replaces core CLI prompt behavior, or is that acceptable for an explicit Loom persona mode?

## Related Records

- `research:20260513-superpowers-skill-activation` - prior research on adapter bootstrap and skill activation across several harnesses.
- `INSTALL.md` - current human-facing install matrix for supported harnesses.
- `CLAUDE.md` - current harness integration acceptance posture.
