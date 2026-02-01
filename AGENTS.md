# Loom

## Preferences

This project is greenfield and deployed nowhere. Do not make assumptions about existing systems or workflows.
Do not build in backwards compatibility for existing tools or processes.

We use uv for everything. No exceptions.
Use uv run to run python commands.

Never take shortcuts. Never take the easy way out. Always do the right thing, even if it's more work.
Do not be bound by existing code or tests. Do it the right way if you know there is a right way or the
users intention is clear.

ALWAYS address LSP issues. Always run the linter. And address warnings. No exceptions. NEVER be lazy.

Do not use lsp_diagnostics, use uv run basedpyright at most

## Context

Python package name: agent-loom

An **agent-native development substrate** with four layers:

1. **State primitives (Git-backed, agent-legible)**

   * **ticket**: structured, dependency-aware intent and work state
   * **memory**: associative, scoped, graph-based memory
     These are not tools. They are *persistent cognitive organs*.

2. **Spatial primitives**

   * **workspace**: topology, isolation, lifecycle, and coordination across repos and worktrees
     This is the physical world the agents live in.

3. **Execution & governance**

   * **team**: orchestration, supervision, escalation, merge authority, eventing
     This is management, not automation.

4. **Learning & self-modification**

   * **Compound engineering plugin**: skill extraction, institutional memory, progressive disclosure
     This is how the system gets *better over time instead of worse*.

That's the bundle. Everything else is implementation detail.

The CLI must reflect this reality above.

---

# The unifying concept

At a conceptual level, this system does exactly one thing:

> It turns a codebase into a *place* where multiple agents can work, remember, learn, coordinate, and govern themselves over long horizons.

Key ideas that keep showing up

* **Persistence** (Git as memory, not storage)
* **Multiplicity** (many agents, many timelines)
* **Governance** (manager, escalation, merge authority)
* **Self-improvement** (skills, constitution, learning loop)
* **Embodiment** (worktrees, repos, terminals, tmux panes)

This is not simply "AI tooling."
This is **infrastructure for synthetic collaborators**.

## Compound (OpenCode)

These blocks are maintained by the Loom compound OpenCode plugin.
Do not edit inside the BEGIN/END fences.

<!-- BEGIN:compound:agents-ai-behavior -->
# Compound Engineering Baseline

This block is maintained by the compound plugin.

**Core loop:** Plan → Work → Review → Compound → Repeat.

**Memory model:**
- **Observations** are logged automatically from tool calls and session events.
- **Instincts** are small heuristics extracted from observations.
- **Skills** are durable procedural memory (directory + SKILL.md) and are the primary compounding mechanism.

**Non-negotiables:**
- Keep skills small, specific, and triggerable from the `description`.
- Prefer updating an existing skill over creating a near-duplicate.
- Never put secrets into skills, memos, or observations.
- The plugin may auto-create/update skills. Humans should occasionally prune duplicates.

**Where things live:**
- Skills: `.opencode/skills/<name>/SKILL.md`
- Instincts: `.opencode/memory/instincts.json` (index at `.opencode/memory/INSTINCTS.md`)
- Observations: `.opencode/memory/observations.jsonl` (gitignored by default)
 - Constitution: `LOOM_PROJECT.md`
 - Direction: `LOOM_ROADMAP.md`
<!-- END:compound:agents-ai-behavior -->

<!-- BEGIN:compound:workflow-commands -->
- `/workflows:plan` - Create tickets + plan (uses memory recall)
- `/workflows:work` - Create/manage worktree (workspace) and implement
- `/workflows:review` - Review changes and update tickets
- `/workflows:compound` - Extract learnings into skills + memory + docs
<!-- END:compound:workflow-commands -->

<!-- BEGIN:compound:loom-core-context -->
- Greenfield: prioritize clarity and determinism; no backwards compatibility.
- Tooling: use `uv run ...` for all Python commands; gate is basedpyright → ruff → targeted pytest.
- Contracts: CLI output and prompts are deterministic and locked by focused contract tests.
- Compound: Plan → Work → Review → Compound; extract durable procedure into skills.
<!-- END:compound:loom-core-context -->

<!-- BEGIN:compound:instincts-index -->
- **compound-learning-output-is-compoundspec-v2-json-only** (100%)
  - Trigger: When responding to a background autolearn prompt
  - Action: Output only valid JSON matching CompoundSpec v2; no commentary, no code fences, no product-code edits.
- **team-core-changes-require-targeted-tests** (100%)
  - Trigger: When editing src/agent_loom/team/core.py, src/agent_loom/team/prompts.py, or src/agent_loom/team/cli.py
  - Action: Update/add focused tests covering the changed behavior (especially prompt contracts) and run `uv run pytest` for the relevant test module(s) plus `uv run ruff check .` before calling the work done.
- **cli-output-is-a-contract** (100%)
  - Trigger: When changing any CLI/user-facing output formatting (especially ticket/team UX)
  - Action: Make output deterministic (explicit ordering, stable formatting) and add a focused pytest contract test for the rendered text.
- **prompt-changes-require-prompt-tests** (99%)
  - Trigger: When editing agent prompts or prompt assembly code
  - Action: Update/add focused tests covering the prompt contract and run the prompt test suite.
- **plan-mode-readonly-no-edits** (97%)
  - Trigger: System reminder says Plan Mode ACTIVE / READ-ONLY phase
  - Action: Do not edit/create/delete files or run write-capable commands; only inspect/read/search and produce an execution plan or required JSON payload.
- **workspace-cli-output-is-a-contract** (90%)
  - Trigger: When changing user-visible output/flags/formatting in src/agent_loom/workspace/cli.py
  - Action: Make output deterministic (explicit ordering; no timestamps/randomness/absolute paths). Add/update a focused contract test (prefer tests/test_workspace_cli_ux.py). Verify with: uv run basedpyright, uv…
- **team-prompts-need-section-level-contracts** (86%)
  - Trigger: When adding or restructuring sections in src/agent_loom/team/prompts.py (or prompt assembly in src/agent_loom/team/core.py).
  - Action: Make prompt rendering deterministic (explicit ordering, stable headings) and add/expand section-level contract tests in tests/test_team_prompts.py that assert required sections/ordering without relyin…
- **compound-template-mirror-must-stay-in-sync** (83%)
  - Trigger: When editing Compound plugin/skill/docs behavior that is shipped via a template (for example .opencode/plugins/compound_engineering.ts or .opencode/skills/*) and the repo contains a scaffold copy unde…
  - Action: Update both the repo-root .opencode/* sources and the scaffolded template under src/agent_loom/compound/opencode/.opencode/* to keep installation output deterministic; add/adjust tests/test_compound_i…
- **team-mounts-changes-require-contract-test** (83%)
  - Trigger: When editing team mount behavior (notably src/agent_loom/team/core.py) or adding/changing mounts-related logic and outputs.
  - Action: Lock the behavior with deterministic invariants and update/add coverage in tests/test_team_mounts.py; then run uv run basedpyright, uv run ruff check ., and uv run pytest tests/test_team_mounts.py.
- **python-commands-use-uv-run** (80%)
  - Trigger: When about to run any Python command (tests, linters, scripts, REPL)
  - Action: Use `uv run ...` (never `python`, `pip`, or bare tool binaries). Prefer `uv run pytest`, `uv run ruff check .`, etc.
- **prefer-basedpyright-over-lsp-diagnostics** (78%)
  - Trigger: When about to check Python types/diagnostics (or an existing checklist says to run lsp_diagnostics)
  - Action: Run `uv run basedpyright` and fix findings before `uv run ruff check .` and targeted `uv run pytest ...`.
- **team-spawn-integrator-changes-require-contract-test** (77%)
  - Trigger: When changing team spawn/integrator wiring (typically in src/agent_loom/team/core.py or src/agent_loom/team/cli.py), especially anything that boots an integrator or mediates agent process startup.
  - Action: Add/update a focused contract test in tests/test_team_spawn_integrator.py that asserts deterministic invariants (what starts, with what args/env, and what is persisted/returned), then run lsp_diagnost…
- **compound-install-changes-require-install-contract-test** (77%)
  - Trigger: When changing src/agent_loom/compound/install.py or src/agent_loom/compound/cli.py (or any behavior that affects generated .opencode/* files).
  - Action: Update/add assertions in tests/test_compound_install.py for deterministic outputs; then run uv run basedpyright, uv run ruff check ., and uv run pytest tests/test_compound_install.py before calling th…
- **skills-canonical-location-is-opencode** (74%)
  - Trigger: When editing/creating skills and there are multiple skill directories (for example .opencode/skills and .claude/skills)
  - Action: Only propose skill changes under .opencode/skills/<name>/SKILL.md and rely on docs/index sync; avoid duplicating or manually maintaining mirror copies elsewhere.
- **workspace-core-changes-require-targeted-tests** (74%)
  - Trigger: When editing src/agent_loom/workspace/core.py, src/agent_loom/workspace/models.py, src/agent_loom/workspace/state.py, src/agent_loom/workspace/repo_ops.py, src/agent_loom/workspace/git_ops.py, src/age…
  - Action: Treat workspace as public API: add/adjust targeted pytest coverage for the behavior/contract being changed (CLI text, model serialization, ordering, guard failures). Run: uv run basedpyright, uv run r…
- **loom-init-cli-changes-require-ux-contract-test** (74%)
  - Trigger: When editing user-visible output/flags/formatting in src/agent_loom/init/cli.py (or init CLI output pathways).
  - Action: Make output deterministic (stable ordering; no nondeterministic/machine-specific values) and add/update a focused pytest contract test (prefer tests/test_loom_init_cli_ux.py). Verify with: uv run base…
- **team-expansion-requires-contract-tests-and-ruff** (73%)
  - Trigger: When adding or significantly expanding team runtime (new CLI entrypoints, inbox loop, or new team modules like inbox/models/constants)
  - Action: Treat it like a public API: add/adjust prompt-contract tests, run `uv run ruff check .`, run targeted `uv run pytest` for the changed surface area, and clear LSP diagnostics on touched files before ca…
- **team-disband-changes-require-disband-tests** (72%)
  - Trigger: When changing team shutdown/disband behavior (especially in src/agent_loom/team/core.py) or introducing a new disband pathway
  - Action: Add/adjust focused tests covering disband semantics in tests/test_team_disband.py; keep teardown deterministic; run uv run pytest tests/test_team_disband.py and uv run ruff check . before calling work…
- **core-cli-changes-require-ux-contract-test** (72%)
  - Trigger: When editing user-visible output/flags/formatting in src/agent_loom/cli.py
  - Action: Make output deterministic and lock it with a focused pytest contract test (prefer tests/test_cli_ux.py or the existing CLI test module). Verify via: uv run basedpyright, uv run ruff check ., uv run py…
- **core-docs-are-contracts** (68%)
  - Trigger: When proposing or making changes to AGENTS.md, LOOM_PROJECT.md, or LOOM_ROADMAP.md (especially deletions or restructures)
  - Action: Treat these files as contracts: avoid large deletions without replacement; keep always-on blocks short/stable; update AI-managed blocks via CompoundSpec v2 (docs.blocks.upsert + docs.sync); keep paths…
<!-- END:compound:instincts-index -->

<!-- BEGIN:compound:rules-index -->
- _(none)_
<!-- END:compound:rules-index -->
