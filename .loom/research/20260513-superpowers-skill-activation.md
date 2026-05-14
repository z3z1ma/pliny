# Superpowers Skill Activation

ID: research:20260513-superpowers-skill-activation
Type: Research
Status: completed
Created: 2026-05-13
Updated: 2026-05-13

## Summary

Superpowers gets skill usage by combining adapter-level bootstrap injection with deliberately forceful `using-superpowers` doctrine, trigger-only skill descriptions, and behavioral tests that verify agents invoke skills before acting. The strongest transferable idea for Loom is not just preloading doctrine, but making the first loaded doctrine an explicit skill-selection loop with anti-rationalization language and tests for naive and pressure prompts.

## Question

How does `github.com/obra/superpowers` make agents use its skills and workflows automatically, and which mechanisms should Loom consider when strengthening `using-loom` activation?

## Scope

Covered:

- `obra/superpowers` cloned on 2026-05-13 at commit `f2cbfbefebbfef77321e4c9abc9e949826bea9d7`.
- Bootstrap and adapter surfaces for Claude Code, OpenCode, Cursor, Gemini, Codex, and Copilot-facing docs or mappings present in the repository.
- `skills/using-superpowers/SKILL.md`, representative workflow skills, `skills/writing-skills/SKILL.md`, and skill-triggering tests.
- Local comparison points in Agent Loom Core: `loom-core/loom-core.mjs`, `loom-core/skills/using-loom/SKILL.md`, `loom-core/hooks/hooks.json`, and `loom-core/gemini-bootstrap.md`.

Excluded:

- Running Claude/OpenCode integration tests against live harnesses.
- Inspecting external marketplaces beyond repository manifests.
- Deciding Loom product behavior; research only recommends consuming surfaces.

## Method And Sources

- Cloned `https://github.com/obra/superpowers.git` into `/var/folders/1b/6mg4g2fs2zx99h46b9j5r7mh0000gp/T/opencode/superpowers-analysis-20260513`.
- Recorded source commit with `git rev-parse HEAD`: `f2cbfbefebbfef77321e4c9abc9e949826bea9d7`.
- Inspected Superpowers bootstrap files: `.opencode/plugins/superpowers.js`, `hooks/session-start`, `hooks/hooks.json`, `hooks/hooks-cursor.json`, `GEMINI.md`, `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `.codex-plugin/plugin.json`, and `gemini-extension.json`.
- Inspected Superpowers skills: `skills/using-superpowers/SKILL.md`, `skills/brainstorming/SKILL.md`, `skills/writing-skills/SKILL.md`, `skills/test-driven-development/SKILL.md`, `skills/systematic-debugging/SKILL.md`, and other `SKILL.md` frontmatter.
- Inspected Superpowers tests: `tests/skill-triggering/*`, `tests/explicit-skill-requests/*`, and `tests/opencode/*`.
- Inspected Superpowers docs: `README.md`, `CLAUDE.md`, `.opencode/INSTALL.md`, and `docs/README.opencode.md`.
- Inspected Loom comparison surfaces listed in Scope.

## Findings

- Superpowers has a real `skills/using-superpowers/SKILL.md`. Its frontmatter says it is used when starting any conversation and requires Skill tool invocation before any response, including clarifying questions.
- The body of `using-superpowers` is intentionally coercive. It says that if there is even a 1% chance a skill applies, the agent must invoke it; if a skill applies, the agent has no choice; the rule is not optional or negotiable.
- The same skill defines authority order with user/project instructions above Superpowers skills and default system prompt below them. This reduces conflict while still making Superpowers stronger than ordinary model defaults.
- The bootstrap skill contains a concrete flowchart: user message received, decide whether any skill might apply, invoke the Skill tool if yes, announce the skill use, create todos for checklist items, follow the skill, then respond. The flow explicitly puts skill invocation before clarifying questions or exploration.
- It includes a red-flags table naming the exact rationalizations agents use to skip skills: simple question, need more context first, explore codebase first, quick file/git check, overkill, already know the skill, or just one thing first.
- OpenCode activation is not just skill registration. `.opencode/plugins/superpowers.js` registers `skills/` via `config.skills.paths`, then injects stripped `using-superpowers` content plus OpenCode tool mapping into the first user message through `experimental.chat.messages.transform`.
- The OpenCode plugin deliberately avoids reinvoking `using-superpowers` through the skill tool. It marks the content as already loaded and tells the agent not to load it again.
- The OpenCode plugin caches bootstrap content after the first read and guards against double injection by checking whether the first user message already contains `EXTREMELY_IMPORTANT`.
- Claude/Cursor-style activation uses a SessionStart hook. `hooks/session-start` reads `skills/using-superpowers/SKILL.md` and returns it as additional context. `hooks/hooks.json` registers the hook for `startup|clear|compact`; `hooks/hooks-cursor.json` registers Cursor `sessionStart`.
- Gemini activation is file-include based. `gemini-extension.json` names `GEMINI.md` as the context file, and `GEMINI.md` includes `@./skills/using-superpowers/SKILL.md` plus Gemini-specific tool mapping.
- Codex/Copilot support in the repo is more manifest/tool-mapping oriented. `.codex-plugin/plugin.json` declares `skills: ./skills/`; `skills/using-superpowers/references/codex-tools.md` says Codex skills load natively and tool names should be mapped.
- The workflow skills use aggressive trigger descriptions. `brainstorming` is the clearest: its description says the agent MUST use it before any creative work, creating features, adding functionality, or modifying behavior.
- Superpowers also uses intra-skill hard gates. `brainstorming` forbids implementation actions until design is presented and approved. `test-driven-development` says it applies before writing implementation code. `systematic-debugging` says it applies before proposing fixes.
- `skills/writing-skills/SKILL.md` explains their trigger design philosophy: descriptions should describe only when to use the skill, not summarize the workflow. Their testing found that workflow summaries in descriptions can cause agents to shortcut the body instead of reading the full skill.
- The same writing guidance treats skills as behavior-shaping code, not prose. It requires baseline failure tests, pressure scenarios, explicit counters to rationalizations, red-flags lists, and retesting until agents comply.
- Tests verify behavior rather than only packaging. `tests/skill-triggering/run-test.sh` sends naive prompts that do not mention the skill and checks stream JSON for Skill tool invocation. `tests/explicit-skill-requests/run-test.sh` checks explicit skill requests and detects premature non-Skill tool use before the Skill invocation.
- `CLAUDE.md` makes bootstrap auto-trigger an acceptance test for new harnesses: in a clean session, the prompt `Let's make a react todo list` must auto-trigger `brainstorming` before code is written. Integrations requiring per-session opt-in are rejected.
- There is a doc drift note: `docs/README.opencode.md` says OpenCode injects via `experimental.chat.system.transform`, but current `.opencode/plugins/superpowers.js` uses `experimental.chat.messages.transform`.
- Before `ticket:20260513-superpowers-style-activation-doctrine`, Loom Core preloaded stronger source material than Superpowers in OpenCode by registering the full `using-loom` skill plus ordered references through `config.instructions`, while also registering `skills/` through `config.skills.paths`.
- Loom's current local `using-loom` is more principled and less coercive. It teaches route order, surfaces, ambiguity shaping, Ralph packets, evidence, and audit, but it does not currently include a Superpowers-style 1% skill-check loop, rationalization table, or tests that assert the first action after a naive prompt is the right Loom skill.

## Tradeoffs

- Superpowers-style forceful language improves activation compliance, but it can be blunt and token-expensive if copied wholesale. Loom should preserve its own authority model and avoid turning every tiny action into heavy record work.
- Injecting bootstrap in the first user message, as Superpowers does for OpenCode, is useful when `config.instructions` is unavailable or repeated system messages are harmful. The transferable lesson is adapter bootstrap plus content and tests; later implementation work can choose the exact transport.
- Trigger-only descriptions help discovery and discourage shortcutting, but Loom descriptions sometimes need to name owning surfaces clearly. The safe adaptation is to keep descriptions focused on conditions and ownership, while putting procedure in the body and references.
- A mandatory skill-check loop would improve activation, but Loom has many record and workflow skills. Without priority rules and examples, agents may over-activate or choose workflow playbooks before Core surfaces.

## Rejected Paths And Null Results

- No separate `using-superpowers` daemon, database, or runtime orchestrator exists. The mechanism is adapter bootstrap plus Markdown skill prose plus native skill discovery.
- OpenCode Superpowers does not implement a custom `use_skill` tool in the current clone. It relies on OpenCode's native `skill` tool and `config.skills.paths`; older design docs proposed custom tools but current code is simpler.
- The repo does not rely only on skill metadata. The always-on behavior comes from full bootstrap injection of `using-superpowers`; metadata registration alone would make skills discoverable but not strongly used.
- The tests do not only check that files exist. Several tests inspect streamed tool calls to verify skill invocation and premature action behavior.

## Conclusions

- Superpowers gets strong activation through a three-layer system: adapter preload of `using-superpowers`, frontmatter and body text tuned for skill invocation, and tests that measure whether agents actually invoke skills under natural prompts.
- The `using-superpowers` skill is the behavioral center. Its most important properties are early invocation, 1% threshold, anti-rationalization red flags, explicit priority order, and a graph-like workflow that makes skill selection the first step.
- The skill corpus reinforces the bootstrap by using high-signal `Use when...` descriptions, hard gates in workflow skills, required sub-skill markers, and pressure-tested rationalization counters.
- For Loom, the most relevant improvement is likely a `using-loom` activation loop that says: load doctrine, inspect likely surface, invoke the relevant Loom skill before action when there is any material chance it applies, and do not rationalize around shaping, tickets, Ralph, evidence, or audit.
- Loom should not blindly copy Superpowers wording. Loom's stronger conceptual model is surfaces and truth ownership; Superpowers' stronger operational model is activation discipline and evals around first-tool behavior. The useful synthesis is Loom surface routing expressed with Superpowers-level anti-skip pressure.

## Recommendations

- Consider updating `loom-core/skills/using-loom/SKILL.md` with an explicit activation loop: after session doctrine load, check whether any Loom surface or workflow skill applies before responding, clarifying, exploring, or editing.
- Add a Loom-specific red-flags table for rationalizations such as `this is just a small change`, `I need to inspect first`, `I'll create the ticket after`, `I'll ask the worker directly`, `evidence can wait`, and `audit is overkill`.
- Keep Loom's authority posture: user and harness instructions remain higher authority; records constrain truth but are not arbitrary instructions; skills route work through owning surfaces.
- Review Loom skill frontmatter for trigger-only descriptions. Avoid descriptions that summarize procedure so agents do not treat frontmatter as enough to skip the full skill.
- Add activation tests modeled on Superpowers: naive prompt should trigger shaping/idea refinement before implementation, bug prompt should trigger debugging, ticket mention should trigger ticket skill, worker request should trigger Ralph packet workflow before `task`, completion claim should trigger evidence/audit posture.
- If OpenCode activation problems are observed, validate the first-user-message injection behavior in a live harness and compare against other preload transports with evidence.

## Open Questions

- Does Loom Core's OpenCode first-user-message injection produce the expected first-action skill invocation behavior in current models?
- Which Loom skills should be treated as process-priority skills analogous to Superpowers `brainstorming` and `systematic-debugging`?
- What is the minimum red-flags language that improves compliance without making Loom feel hostile or causing over-activation?

## Related Records

- `ticket:20260513-mandatory-shaping-doctrine` - recent closed ticket strengthening Loom ambiguity shaping doctrine.
- `research:20260510-loom-loop-failure-analysis` - prior analysis of Loom loop failures and premature execution.
- `loom-core/skills/using-loom/SKILL.md` - likely consuming surface for activation-loop changes.
- `loom-core/loom-core.mjs` - OpenCode preload and skill registration surface.
