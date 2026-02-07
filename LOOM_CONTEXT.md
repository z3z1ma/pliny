# LOOM_CONTEXT

This file is included in the agent's context. It should be committed.

It is intentionally **derived and frequently updated** by Loom compound.
Do not edit inside the BEGIN/END fences.

<!-- BEGIN:compound:agents-ai-behavior -->
# Compound Engineering Baseline

This block is maintained by the compound system.

**Core loop:** Plan -> Work -> Review -> Compound -> Repeat.

**Memory model:**
- **Observations** are logged automatically from tool calls and session events.
- **Instincts** are small heuristics extracted from observations.
- **Skills** are durable procedural memory (directory + SKILL.md) and are the primary compounding mechanism.
- **Episodes** are immutable evidence capsules. If a patch is too large to inline, the full patch is stored as a blob.
- **Decisions** are append-only records of normalized ops applied to instincts/skills (governance; replayable).

**Non-negotiables:**
- Keep skills small, specific, and triggerable from the `description`.
- Prefer updating an existing skill over creating a near-duplicate.
- Never put secrets into skills, memos, or observations.

**Where things live:**
- Skills: `.opencode/skills/<name>/SKILL.md`
- Instincts: `.opencode/memory/instincts.json` (index at `.opencode/memory/INSTINCTS.md`)
- Observations: `.opencode/memory/observations.jsonl` (gitignored by default)
- Episodes: `.loom/compound/episodes/YYYY/MM/<episode_id>.json` (committed evidence)
- Blobs: `.loom/compound/blobs/<sha256>.<ext>` (full patches, raw proposals, prompt snapshots)
- Decisions: `.loom/compound/decisions/YYYY/MM/<decision_id>.json` (append-only ops log)

**Core docs:**
- `AGENTS.md` (stable human-owned overview)
- `LOOM_CONTEXT.md` (derived always-on context + instincts summary)
- `LOOM_ROADMAP.md` (direction + backlog + changelog)
<!-- END:compound:agents-ai-behavior -->

<!-- BEGIN:compound:workflow-commands -->
- `/workflows:plan` - Create tickets + plan (uses `loom memory recall`)
- `/workflows:work` - Work in a worktree and implement
- `/workflows:review` - Review changes before merge
- `/workflows:compound` - Extract learnings into skills + memos + docs
<!-- END:compound:workflow-commands -->

<!-- BEGIN:compound:loom-core-context -->
# Loom always-on context (second-order compression)

This block is intentionally *small and stable*. Only update it when a principle has proven durable.

- First-order: observations -> instincts -> skills.
- Second-order: compress patterns into a few fundamentals that are always-on.
- Prefer agent-native primitives: ticket, memory, workspace, team.
- Governance loop: Plan -> Work -> Review -> Compound -> Repeat.

@LOOM_ROADMAP.md
<!-- END:compound:loom-core-context -->

<!-- BEGIN:compound:instincts-index -->
- **prompt-changes-require-prompt-tests** (100%)
  - Trigger: When editing agent prompts or prompt assembly code
  - Action: Update/add focused tests covering the prompt contract and run the prompt test suite.
- **team-core-changes-require-targeted-tests** (100%)
  - Trigger: When editing src/agent_loom/team/core.py, src/agent_loom/team/prompts.py, or src/agent_loom/team/cli.py
  - Action: Update/add focused tests covering the changed behavior (especially prompt contracts) and run `uv run pytest` for the relevant test module(s) plus `uv run ruff check .` before calling the work done.
- **cli-output-is-a-contract** (100%)
  - Trigger: When changing any CLI/user-facing output formatting (especially ticket/team UX)
  - Action: Make output deterministic (explicit ordering, stable formatting) and add a focused pytest contract test for the rendered text.
- **plan-mode-readonly-no-edits** (100%)
  - Trigger: System reminder says Plan Mode ACTIVE / READ-ONLY phase
  - Action: Do not edit/create/delete files or run write-capable commands; only inspect/read/search and produce an execution plan or required JSON payload.
- **server-template-output-is-a-contract** (100%)
  - Trigger: When changing src/agent_loom/server/templates/*.html (especially large refactors like dashboard.html).
  - Action: Treat rendered HTML as a deterministic UX contract: ensure stable ordering/no nondeterministic values, add/update a focused pytest contract test for required markers/sections, then run `uv run basedpy...
- **dashboard-template-changes-require-server-contract-test** (100%)
  - Trigger: You change src/agent_loom/server/templates/dashboard.html (especially large refactors or section reshuffles).
  - Action: Update/add request-level invariants in tests/test_server_api_contract.py (stable markers/sections + deterministic ordering; avoid full-HTML snapshots) and verify with: uv run basedpyright; uv run ruff...
- **workspace-cli-output-is-a-contract** (98%)
  - Trigger: When changing user-visible output/flags/formatting in src/agent_loom/workspace/cli.py
  - Action: Make output deterministic (explicit ordering; no timestamps/randomness/absolute paths). Add/update a focused contract test (prefer tests/test_workspace_cli_ux.py). Verify with: uv run basedpyright, uv...
- **compound-template-mirror-must-stay-in-sync** (97%)
  - Trigger: When editing Compound plugin/skill/docs behavior that is shipped via a template (for example .opencode/plugins/compound_engineering.ts or .opencode/skills/*) and the repo contains a scaffold copy unde...
  - Action: Update both the repo-root .opencode/* sources and the scaffolded template under src/agent_loom/compound/opencode/.opencode/* to keep installation output deterministic; add/adjust tests/test_compound_i...
- **large-template-refactor-diff-hygiene** (96%)
  - Trigger: You are about to make a large refactor in src/agent_loom/server/templates/*.html (especially dashboard.html) that could produce a huge diff.
  - Action: Minimize formatting-only churn, preserve/introduce stable data-* anchors, and update tests/test_server_api_contract.py in the same change to assert invariant markers/sections (avoid full HTML snapshot...
- **ticket-changes-require-ticket-ux-contract-test** (95%)
  - Trigger: You edit ticket runtime/UX code (src/agent_loom/ticket/*.py or src/agent_loom/ui/ticket_ui.*) or anything that changes rendered ticket text/sections.
  - Action: Treat ticket UX as a contract: make ordering deterministic, update/add focused assertions in tests/test_ticket_ux.py for required sections/lines (avoid nondeterministic values), then verify via `uv ru...
- **team-prompts-need-section-level-contracts** (94%)
  - Trigger: When adding or restructuring sections in src/agent_loom/team/prompts.py (or prompt assembly in src/agent_loom/team/core.py).
  - Action: Make prompt rendering deterministic (explicit ordering, stable headings) and add/expand section-level contract tests in tests/test_team_prompts.py that assert required sections/ordering without relyin...
- **server-html-changes-require-api-contract-test** (94%)
  - Trigger: When changing server-rendered HTML behavior (templates or the route that serves them), especially large refactors in src/agent_loom/server/templates/*.html
  - Action: Add/update a request-level contract test (prefer tests/test_server_api_contract.py) that asserts stable markers/sections and deterministic ordering; avoid brittle full-HTML snapshots; verify via uv ru...
<!-- END:compound:instincts-index -->

<!-- BEGIN:compound:rules-index -->
- memory.md: .opencode/rules/memory.md
- team.md: .opencode/rules/team.md
- ticket.md: .opencode/rules/ticket.md
- workspace.md: .opencode/rules/workspace.md
<!-- END:compound:rules-index -->
