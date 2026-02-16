---
"id": "al-aee1"
"status": "closed"
"deps": []
"links": []
"created": "2026-02-16T05:31:53Z"
"type": "task"
"priority": 1
"assignee": "z3z1ma"
"parent": "al-1696"
"tags":
- "team"
- "refactor"
- "modularity"
- "sprint:Modular-refinement"
"external": {}
---
# Team core: extract objective+sprint state domain

Objective alignment:
Current objective prioritizes modularity and organization quality. Objective/sprint state mutations are currently embedded in `team/core.py`, increasing coupling and making planning behavior harder to reason about.

Scope:
- Introduce a dedicated domain module for objective/sprint state orchestration (for example `src/agent_loom/team/objective_state.py` or equivalent).
- Move pure state helpers and mutation flow currently in `src/agent_loom/team/core.py` into the new module, including objective read/mutate helpers and sprint state normalization helpers.
- Keep CLI/API behavior stable by delegating from existing public core entrypoints (`objective_show`, `objective_set`, `objective_append`, `sprint_show`, `sprint_set`, `sprint_clear`, `prep_sprint`).
- Update focused tests in `tests/test_team_sprint.py` and objective-related coverage impacted by extraction.

Non-goals:
- No command surface changes.
- No tmux lifecycle behavior changes.
- No ticket model redesign.

Implementation plan:
1) Identify objective/sprint helper functions in `team/core.py` and group by read-only vs mutating responsibilities.
2) Add new domain module with explicit function contracts and minimal dependencies (run state + models + errors only where needed).
3) Replace in-core logic with thin delegations while preserving return models and error codes.
4) Update tests to lock behavioral parity (messages, tags, parenting behavior from prep path).
5) Remove now-unused imports/helpers from `team/core.py`.

Verification:
- uv run pytest tests/test_team_sprint.py tests/test_ticket_sprint_context.py tests/test_team_cli_ux.py
- uv run ruff check .
- uv run basedpyright

Risks/edge cases:
- Sprint tag precedence can regress if helper ordering changes; verify env vs run-state precedence via tests.
- Prep-sprint side effects (ticket metadata) can drift if mutation helpers are partially moved; assert exact required metadata.
- Circular imports between `team/core.py` and the new module are likely if contracts are not kept narrow.

## Acceptance Criteria

- Objective/sprint flows are implemented in a dedicated domain module and `team/core.py` delegates to it.
- Existing CLI-observable behavior for objective/sprint commands remains unchanged.
- Targeted team sprint/objective tests pass and no dead helper code remains in core.

## Notes

**2026-02-16T06:06:34Z**

Unblocked after permissions fix. Acked manager nudges, confirmed spawn_persona sprint import fix in place, and proceeding to finalize commit + review handoff.

**2026-02-16T06:06:57Z**

Completed extraction and committed as f856764.

What changed:
- Added dedicated domain module: src/agent_loom/team/objective_state.py
- Moved objective input/read/show + mutation logic and sprint state normalization/mutation helpers into domain module.
- Updated src/agent_loom/team/core.py objective/sprint entrypoints to delegate to domain helpers while preserving CLI-visible behavior.
- Updated spawn_persona path to consume sprint_state from objective_state (fixes runtime import break from removed core helper).
- Expanded tests/test_team_sprint.py coverage for sprint_set default-tag behavior and sprint_clear rev increments under delegated flow.

Verification run:
- UV_CACHE_DIR=/tmp/uv-cache uv run --no-sync ruff check .
- UV_CACHE_DIR=/tmp/uv-cache uv run --no-sync basedpyright
- UV_CACHE_DIR=/tmp/uv-cache uv run --no-sync pytest tests/test_team_sprint.py tests/test_ticket_sprint_context.py tests/test_team_cli_ux.py

Results: all pass.
